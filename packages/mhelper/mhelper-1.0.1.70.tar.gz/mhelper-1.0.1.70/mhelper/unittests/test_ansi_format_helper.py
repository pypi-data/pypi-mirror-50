from mhelper import ansi_format_helper


def test_ansi_format_helper():
    try:
        raise ValueError( "Something didn't actually go wrong." )
    except Exception as ex:
        ansi_format_helper.print_traceback( ex )


if __name__ == "__main__":
    test_ansi_format_helper()
