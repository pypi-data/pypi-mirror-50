import time
from typing import Optional, Callable

from mhelper import string_helper


class ProgressMaker:
    def __init__( self,
                  title: str,
                  total: Optional[int] = None,
                  *,
                  issue: Callable[["Progress"], None],
                  period: float = 1.0,
                  item: str = "record",
                  text: Optional[str] = None ):
        """
        :param title:   Title of the progress bar 
        :param total:   Total number of jobs 
        :param issue:   Where to send progress updates 
        :param period:   Period between progress updates 
        :param item:    Title of type of jobs 
        :param text:    Format specifier for jobs.
                        This is optionally added to the progress bar text.
                        `{}` is the replaced with the current record or count processed. 
        """
        self.title = title or "(TASK)"
        self.total_jobs = total
        self.start_time = time.perf_counter()
        self.issue_function = issue
        self.issue_period = period
        self.issue_next = self.start_time + period
        self.num_processed = 0
        self.record_type_name = item
        self.job_format = text
    
    
    def increment( self, value = 1 ):
        """
        Calls `report` with `value` more processed jobs than last time.
        """
        self.report( self.num_processed + value )
    
    
    def report( self, num_processed = None, current_item = None ) -> None:
        """
        Reports a progress update if it is time.
        
        :param num_processed:   Number processed. 
        :param current_item:    Current item being processed. 
        :return:                 
        """
        if num_processed is not None:
            self.num_processed = num_processed
        
        now = time.perf_counter()
        
        if now < self.issue_next:
            return
        
        self.issue_next = now + self.issue_period
        p = Progress( self.title, self.record_type_name, self.total_jobs, self.num_processed, current_item, self.start_time, now, False, self.job_format )
        self.issue_function( p )
    
    
    def begin( self ):
        """
        Issues a progress update at 0%, always.
        """
        now = time.perf_counter()
        self.issue_next = now + self.issue_period
        
        p = Progress( self.title, self.record_type_name, self.total_jobs, self.num_processed, None, self.start_time, now, False, self.job_format )
        self.issue_function( p )
        return p
    
    
    def complete( self ):
        """
        Issues a progress update at 100%, with a completed flag, always.
        """
        now = time.perf_counter()
        self.issue_next = now + self.issue_period
        
        p = Progress( self.title, self.record_type_name, self.total_jobs, self.num_processed, None, self.start_time, now, True, self.job_format )
        self.issue_function( p )
        return p


_TIME = string_helper.timedelta_to_string
_FLOAT = lambda x: "{0:.2f}".format( x )
_PERCENT = lambda x: "{0:.0f}".format( x * 100 )
_INT = lambda x: "{:,}".format( x )


class Progress:
    
    
    def __init__( self,
                  task_title: str,
                  record_type_name: str,
                  num_jobs: Optional[int],
                  num_processed: int,
                  current_record: Optional[object],
                  start_time: float,
                  current_time: float,
                  is_complete: bool,
                  job_format: Optional[str] ):
        """
        :param num_jobs:       Total number of jobs 
        :param num_processed:   Number of jobs completed 
        :param start_time:       Start time 
        :param current_time:         Time now 
        """
        assert isinstance( task_title, str )
        assert isinstance( record_type_name, str )
        assert num_jobs is None or isinstance( num_jobs, int ), num_jobs
        assert isinstance( num_processed, int )
        assert isinstance( start_time, float )
        assert isinstance( current_time, float )
        assert isinstance( is_complete, bool )
        assert job_format is None or isinstance( job_format, str )
        
        self.task_title = task_title
        self.record_type_name = record_type_name
        self.num_processed = num_processed
        self.num_jobs = num_jobs
        self.start_time = start_time
        self.current_time = current_time
        self.is_complete = is_complete
        self.current_record = current_record
        self.job_format = job_format
        # self.elapsed_time = current_time - start_time
        # self.remaining_jobs = (self.total_jobs - self.processed_jobs) if self.total_jobs else 0
        # self.time_per_job = (self.elapsed_time / self.processed_jobs) if self.processed_jobs else 0
        # self.remaining_time = self.remaining_jobs * self.time_per_job
        # self.fraction_complete = (self.processed_jobs / self.total_jobs) if self.total_jobs else 0
        # self.percent_complete = self.fraction_complete * 100
    
    
    def __str__( self ):
        total_time = self.current_time - self.start_time
        time_per_record = (total_time / self.num_processed) if self.num_processed else 0
        records_per_second = round( self.num_processed / total_time )
        
        if self.is_complete:
            extra = " - complete"
        elif self.current_record is not None:
            extra = " " + (self.job_format or "{}").format( self.current_record )
        elif self.job_format:
            extra = " " + self.job_format.format( self.num_processed )
        else:
            extra = ""
        
        if self.num_jobs is not None:
            percent = (self.num_processed / self.num_jobs) if self.num_jobs else 1
            
            if self.num_processed:
                records_remaining = self.num_jobs - self.num_processed
                time_remaining = time_per_record * records_remaining
                
                return self.fmt( "[...] {}: {} of {} ({}%) - {} (~{} for {} remaining at {}r/s or {}/r)" + extra,
                                 self.task_title,
                                 _INT( self.num_processed ),
                                 _INT( self.num_jobs ),
                                 _PERCENT( percent ),
                                 _TIME( total_time ),
                                 _TIME( time_remaining ),
                                 _INT( records_remaining ),
                                 _INT( records_per_second ),
                                 _TIME( time_per_record )
                                 )
            else:
                return self.fmt( "[...] {}: {} of {} ({}%) - {}" + extra,
                                 self.task_title,
                                 _INT( self.num_processed ),
                                 _INT( self.num_jobs ),
                                 _PERCENT( percent ),
                                 _TIME( total_time )
                                 )
        else:
            if self.num_processed:
                return self.fmt( "[...] {}: {}... - {} ({}/{})" + extra,
                                 self.task_title,
                                 _INT( self.num_processed ) if self.num_processed else "",
                                 _TIME( total_time ),
                                 _TIME( time_per_record ),
                                 _INT( records_per_second )
                                 )
            else:
                return self.fmt( "[...] {}: {}... - {}" + extra,
                                 self.task_title,
                                 _INT( self.num_processed ) if self.num_processed else "",
                                 _TIME( total_time ),
                                 extra
                                 )
    
    
    def fmt( self, x, *args, **kwargs ):
        return x.format( *args, **kwargs )
