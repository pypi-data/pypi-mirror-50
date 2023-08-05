import re
from copy import deepcopy

__author__ = "Casper da Costa-Luis <casper.dcl@physics.org>"
__version__ = "0.0.0"


class Globber(object):
    def __init__(self, *parts):
        """
        parts  : (tuple(name, regex, glob), ...)
        """
        self.partsKeys = [i[0] for i in parts]
        self.partsRegs = [i[1] for i in parts]
        self.partsGlob = [i[2] for i in parts]
        self.val = self.parseRe()
        self.valRe = re.compile(self.val)
        self.glb = self.parseGlob()
        # glob all files
        self.files = self.glob(self.glb)
        # ensure files pass the regex
        self.files = self.filterRe()

        parts = map(self.split, self.files)
        self.partsVals = [sorted({p[i] for p in parts})
                          for i in range(len(parts[0]))]

    def filterGlob(self, **keys):
        """return self.files that match given key=glob pairs"""
        raise DeprecationWarning
        p = deepcopy(self.partsGlob)
        for k, v in keys.items():
            p[self[k]] = v
        return self.filterRe(self.glob(self.parseGlob(p)))

    def filterRe(self, escape=False, **keys):
        """return self.files that match given key=regex pairs"""
        p = deepcopy(self.partsRegs)
        for k, v in keys.items():
            p[self[k]] = self.escape(v) if escape else v
        r = re.compile(self.parseRe(p))
        return filter(r.match, self.files)

    def filterReUnlike(self, fname, escape=False, **keys):
        """return self.files that are like `fname` but with given key=regex pairs

        Use `None` for regex for default (all)"""
        p = self.split(fname, escape=True)
        for k, v in keys.items():
            i = self[k]
            p[i] = self.partsRegs[i] if v is None \
                else self.escape(v) if escape else v
        r = re.compile(self.parseRe(p))
        return filter(r.match, self.files)

    def filterReLike(self, fname, *keys):
        """return self.files that are like `fname`'s `key`s"""
        p = self.split(fname, escape=True)
        d = {k: p[self[k]] for k in keys}
        return self.filterRe(**d)

    def index(self, key):
        return self.partsKeys.index(key)

    def __getitem__(self, key):
        return self.index(key)

    def parseGlob(self, parts=None):
        return ''.join(self.partsGlob if parts is None else parts)

    def parseRe(self, parts=None):
        return '(' + ')('.join(self.partsRegs if parts is None else parts) + ')'

    def split(self, fname, escape=False):
        """decompose `fname` into its parts"""
        parts = self.valRe.findall(fname)[0]
        return map(self.escape, parts) if escape else list(parts)

    @classmethod
    def glob(cls, *a, **k):
        """sorted version of glob.glob"""
        from glob import glob as g
        return sorted(g(*a, **k))

    @classmethod
    def escape(cls, s):
        """escape filename characters which are valid regex"""
        for c in ".+[]{}()^$":
            s = s.replace(c, '\\' + c)
        return s


def glob(*a, **k):
    return Globber.glob(*a, **k)
