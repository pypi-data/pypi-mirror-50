from ._memoise import memoise, memo_db, load_db, save_db, hashForce
from ._profile import cprof, lprof
from ._term import sh, TqdmStream, stripEnd, inputPrompt
from ._globber import Globber, glob
from ._table import table
from ._logging import getLoggerLevel

from ..io._h5reader import H5Reader as H
class H5Reader(H):
    def __init__(self, *a,**k):
        raise DeprecationWarning("`H5Reader` moved to `caspyr.io` from `caspyr.utils`")
        super(H5Reader, self).__init__(*a, **k)

__all__ = ["memoise", "memo_db", "load_db", "save_db", "hashForce",
           "cprof", "lprof", "H5Reader", "sh", "TqdmStream", "stripEnd",
           "inputPrompt", "Globber", "glob", "table", "getLoggerLevel"]
