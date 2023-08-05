import logging
import contextlib

__author__ = "Casper da Costa-Luis <casper.dcl@physics.org>"
__version__ = "0.0.0"


@contextlib.contextmanager
def getLoggerLevel(name=None, level=None):
    """
    Context yielding `getLogger(name)` with the specified effective `leve1`
    """
    log = logging.getLogger(name)
    old = log.getEffectiveLevel()
    try:
        if level is not None:
            log.setLevel(level)
        yield log
    finally:
        log.setLevel(old)
