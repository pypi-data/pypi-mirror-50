from mhelper import cache_helper


def main():
    class Next:
        def __init__( self ):
            self.value = 0
        
        
        def __call__( self ):
            self.value += 1
            print(self.value)
            return self.value
    
    
    next = Next()
    
    
    class MyClass( cache_helper.CacheEnabled ):
        @cache_helper.cached()
        def cached_method( self ):
            return next()
        
        @cache_helper.cached()
        def cached_method_2( self, _ ):
            return next()
        
        
        def not_cached_method( self ):
            return next()
        
    @cache_helper.cache_enabled()
    class MyClass2:
        @cache_helper.cached()
        def cached_method( self ):
            return next()
        
        @cache_helper.cached()
        def cached_method_2( self, _ ):
            return next()
        
        
        def not_cached_method( self ):
            return next()
        
    class MyBadClass:
        @cache_helper.cached()
        def cached_method( self ):
            return next()
    
    
    instance1 = MyClass()
    assert instance1.cached_method() == 1
    assert instance1.cached_method() == 1
    assert instance1.cached_method_2(0) == 2
    assert instance1.cached_method_2(0) == 2
    assert instance1.cached_method_2(1) == 3
    assert instance1.cached_method_2(1) == 3
    assert instance1.cached_method_2(2) == 4
    assert instance1.cached_method_2(2) == 4
    assert instance1.not_cached_method() == 5
    assert instance1.not_cached_method() == 6
    
    instance2 = MyClass2()
    assert instance2.cached_method() == 7
    assert instance2.cached_method() == 7
    assert instance2.cached_method_2(1) == 8
    assert instance2.cached_method_2(1) == 8
    assert instance2.not_cached_method() == 9
    assert instance2.not_cached_method() == 10
    
    assert instance1.cached_method() == 1
    assert instance2.cached_method() == 7
    assert instance1.cached_method_2(1) == 3
    assert instance1.cached_method_2(2) == 4
    assert instance2.cached_method_2(1) == 8
    assert instance2.cached_method_2(2) == 11
    
    instance3 = MyBadClass()
    try:
        instance3.cached_method()
        assert False
    except ReferenceError:
        assert True
    
    print("success")

if __name__ == "__main__":
    main()
