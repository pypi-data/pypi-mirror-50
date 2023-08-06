from mhelper import ansi


def run_ansi_tests():
    for x in dir( ansi ):
        if x.startswith("_"):
            continue
            
        v = getattr( ansi, x )
        
        if isinstance( v, str ):
            print( "{} = {}TEST{}".format( x, v, ansi.RESET ) )


if __name__ == "__main__":
    run_ansi_tests()
