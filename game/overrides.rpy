python early:
    def dummy(*args, **kwargs):
        """
        Dummy function. Does absolutely nothing
        """
        # XD
        return

    renpy.execution.check_infinite_loop = dummy
