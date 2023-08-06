from threading import Thread
from time import sleep
from typing import List, Optional, Union


class ThreadedDispatcher:
    """
    Asynchronous message queue.
    
    This loops querying a `handler` for tasks. New threads are then spawned to
    perform the tasks.
    
    This queue works across process boundaries, if a new task is available
    then the `ThreadedDispatcher.Notifier` class may be used to inform the
    process running the `ThreadedDispatcher` that it should query the `handler`
    for new tasks. Alternatively, the `ThreadedDispatcher` will periodically
    poll the `handler` for tasks.
    
    All fields should be considered immutable externally. 
    
    :ivar handler:              ITaskHandler instance
    :ivar __threads:              List of active threads
    :ivar __thread_index:         Arbitrary incrementer used to name new threads
    :ivar max_num_threads:      Maximum number of active threads
    :ivar poll_frequency:       Timeout on the SYSTEM_EVENT
    :ivar __shutting_down:        When set, indicates the queue is waiting for tasks to finish before it exits its main loop.
    :ivar __shut_down:            When set, indicates that all tasks are finished and the queue is exiting/exited its main loop.
    :ivar __notifier:             A `ThreadedDispatcher.Notifier` instance that is used to construct the system events.
    """
    __slots__ = "__handler", "__thread_index", "threads_lock", "__threads", "__max_num_threads", "__poll_frequency", "__shutting_down", "__shut_down", "__notifier"
    
    
    def __init__( self,
                  handler: "ThreadedDispatcher.IHandler",
                  notifier: Union["ThreadedDispatcher.Notifier", str],
                  max_num_threads: int,
                  poll_frequency: float ):
        super().__init__()
        self.__handler = handler
        self.__threads: List[Thread] = []
        self.__thread_index = 0
        self.__max_num_threads = max_num_threads
        self.__poll_frequency = poll_frequency
        self.__shutting_down = False
        self.__shut_down = False
        self.__notifier = self.Notifier( notifier ) if isinstance( notifier, str ) else notifier
        self.__handler.log( "Threaded task queue created. {} maximum threads, {} second poll interval.", max_num_threads, poll_frequency )
    
    
    class IHandler:
        """
        Designates a class capable of providing tasks for a `ThreadedDispatcher`.
        """
        
        
        def acquire_task( self ) -> Optional[object]:
            """
            The implementing class should return an object identifying the task to
            perform, or `None` if no tasks are available. This function is
            guaranteed to always be called from the dispatcher's main thread.
            """
            raise NotImplementedError( "abstract" )
        
        
        def run_task( self, task: object ) -> None:
            """
            The implementing class should run the specified task. This function is
            called from the dispatcher's worker thread.
            
            .. note::
            
                Due to the GIL the `ITaskHandler` itself may wish to spawn a new
                process to run CPU-bound tasks, rather than relying on the worker
                thread to alleviate load.
            """
            raise NotImplementedError( "abstract" )
        
        
        def send_heartbeat( self ) -> bool:
            """
            This is called when the dispatcher is notified or polls. The
            implementing class should perform any periodic actions and return
            whether the dispatcher should continue running. Returning `False` shuts
            down the dispatcher gracefully.
            """
            raise NotImplementedError( "abstract" )
        
        
        def log( self, *args, **kwargs ) -> None:
            """
            Called by the dispatcher to issue logging messages.
            """
    
    
    class Notifier:
        """
        Used by a client to notify a `ThreadedDispatcher` that it should
        acquire tasks and send its heartbeat.
        
        This class is also used by the `ThreadedDispatcher` itself to instantiate
        the system events in the same manner on the server.
        
        :ivar system_event:         Notifies the dispatcher that new tasks are
                                    available, or that it should send its
                                    heartbeat, rather than waiting for the next
                                    poll.
        :ivar system_event_pong:    Set by the dispatcher in response to a
                                    `system_event` or poll. Clients may unset
                                    this and wait to check the dispatcher's
                                    status (see `notify`). 
        """
        
        
        def __init__( self, queue_name: str ):
            try:
                # noinspection PyPackageRequirements
                from SystemEvent import SystemEvent
            except ImportError as ex:
                raise RuntimeError( "The `ThreadedDispatcher` requires the `SystemEvent` python package but this is not installed." ) from ex
            
            self.system_event = SystemEvent( "{}".format( queue_name ) )
            self.system_event_pong = SystemEvent( "{}_pong".format( queue_name ) )
        
        
        def notify( self, wait: float = None ) -> bool:
            """
            Sets the `system_event`, telling the (remote) `ThreadedDispatcher`
            to try and dispatch tasks.
            
            If `wait` is set, then the function waits for a maximum of `wait`
            seconds and returns whether the dispatcher acknowledged the
            `system_event` via its `system_event_pong` during this time. If wait
            is not set, then this function always returns `False`.
            """
            self.system_event_pong.clear()
            self.system_event.set()
            
            if wait is not None:
                return self.system_event_pong.wait( wait )
            else:
                return False
    
    
    def run_dispatcher( self ) -> None:
        """
        Runs the main dispatcher loop.
        
        This repeatedly calls `__dispatch` until there is nothing more to
        dispatch (because there are no more jobs or no more available threads),
        and then waits on either the poll-time to expire or the SYSTEM_EVENT 
        to be flagged. Then it starts dispatching again.
        
        .. note::
        
            If the dispatcher appears to be already running, this will exit
            immediately.
        """
        
        # See if we are already running
        if self.__notifier.notify( 5 ):
            self.__handler.log( "The dispatcher is already running." )
            return
        
        self.__dispatch_all( "created" )
        
        while not self.__shut_down:
            is_set = self.__notifier.system_event.wait( self.__poll_frequency )
            self.__notifier.system_event.clear()
            self.__notifier.system_event_pong.set()
            
            # Send our heartbeat to anyone who cares
            if not self.__handler.send_heartbeat():
                self.__handler.log( "I have received the shutdown signal from the heartbeat function." )
                self.__shutting_down = True
            
            self.__dispatch_all( "released" if is_set else "polling" )
    
    
    def __dispatch_all( self, debug_message: str ) -> None:
        """
        This repeatedly calls `__dispatch` until there is nothing more to
        dispatch (because there are no more jobs or no more available threads).
        """
        while self.__dispatch( debug_message ):
            debug_message = "iterating"
            pass
    
    
    def __dispatch( self, debug_message ) -> bool:
        """
        Obtains a task from the queue and spawns a thread to process it.
        
        Returns `False` if there are no more jobs or no more threads, this
        stops the master until a thread ends or a `SYSTEM_EVENT` is received. 
        """
        # Drop any dead threads
        for thread in list( self.__threads ):
            if not thread.is_alive():
                self.__handler.log( "THREAD #{} WITH TASK #{} HAS ENDED.", *getattr( thread, "TAG_x_args" ) )
                self.__threads.remove( thread )
        
        # Check we aren't at capacity
        num_threads = len( self.__threads )
        
        # If we are shutting down then don't spawn any more tasks...
        if self.__shutting_down:
            self.__handler.log( "WAITING FOR {} THREADS TO END BEFORE SHUT DOWN.", num_threads )
            
            # ...and if there are no more threads then exit
            if num_threads == 0:
                self.__shut_down = True
            
            return False
        
        if num_threads >= self.__max_num_threads:
            self.__handler.log( "Dispatcher[{}] {} - at capacity.", num_threads, debug_message )
            return False
        
        # Get a task
        task_id = self.__handler.acquire_task()
        
        if task_id is None:
            self.__handler.log( "Dispatcher[{}] {} - no task.", num_threads, debug_message )
            return False
        
        if debug_message == "polling":
            # Possible causes:
            # 1. Timing. The dispatcher was notified, but timed-out at the same time as it was
            #    notified. This is more likely if the poll interval is low.
            # 2. Notification. The dispatcher wasn't notified of the new task / free thread.
            # 3. Event. The dispatcher was notified, but something went wrong with the SystemEvent
            #    that should have passed that notification between processes.
            self.__handler.log( "WARNING: Dispatcher had to poll to receive the task. See comments in code.", UserWarning )
        
        # Create a thread for it
        self.__thread_index += 1
        self.__handler.log( "Dispatcher[{}] {} - dispatching task #{} to thread #{}.".format( num_threads, debug_message, task_id, self.__thread_index ) )
        thread = Thread( target = self.__thread_fn,
                         args = (self.__thread_index, task_id),
                         name = "mq_thread_{}".format( self.__thread_index ) )
        setattr( thread, "TAG_x_args", (self.__thread_index, task_id) )
        self.__threads.append( thread )
        thread.start()
        return True
    
    
    def __thread_fn( self, thread_id: int, task_id: int ) -> None:
        try:
            # Execute the task
            self.__handler.log( "Task #{} has been received on thread #{}.".format( task_id, thread_id ) )
            self.__handler.run_task( task_id )
            
            # Notify the dispatcher that they may start another thread
            # (Use the same process clients use to notify us)
            self.__notifier.notify()
        except Exception as ex:
            import mhelper.ansi_format_helper
            msg = mhelper.ansi_format_helper.format_traceback_ex( ex, message = "An unhandled error has occurred on the worker thread. The dispatcher will now try to exit." )
            self.__handler.log( msg )
            self.__shutting_down = True
