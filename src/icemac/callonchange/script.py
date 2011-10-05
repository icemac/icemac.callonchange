# -*- coding: utf-8 -*-
# Copyright (c) 2010-2011 Michael Howitz
# See also LICENSE.txt

import sys
import time
import icemac.callonchange.observer


def callonchange(*args):
    """Handler for entry point which can handle default and sys.argv parameters."""
    # Combine function arguments which sys.argv arguments:
    path, params, options = icemac.callonchange.observer.mangle_call_args(
        args, sys.argv[1:])
    if path is None:
        # mangle_call_args obviously printed a usage message, so we
        # can quit here.
        return
    observer = icemac.callonchange.observer.Observer(path, params, **options)
    observer.start()
    try:
        try:
            while True:
                # Sleep, waiting for keyboard interrupts does not cost too
                # much resources. The observer runs in a different thread.
                time.sleep(1)
        except KeyboardInterrupt:
            # allow to stop the observer by pressing ^C, this ends the
            # while True loop.
            pass
    finally:
        observer.stop()
