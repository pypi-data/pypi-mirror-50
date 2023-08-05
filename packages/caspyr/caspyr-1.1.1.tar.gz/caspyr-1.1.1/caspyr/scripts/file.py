#!/usr/bin/env python
"""file v%s

Prints info about given files.

Usage:
  file [options] <files>...

Options:
  --log LEVEL  : (FAT|CRITIC)AL|ERROR|WARN(ING)|[default: INFO]|DEBUG|NOTSET

Arguments:
  <files>  : Files to test.

%s
"""
import sys
from io import open as io_open
import logging
from argopt import argopt
import re
__all__ = ["main", "run"]
__version__ = "0.1.0"
__author__ = "Casper da Costa-Luis <casper.dcl@physics.org>"

RE_PARTS = re.compile(r"[[\]:]")
TEXT_EXT = "txt md rst py cpp cfg ini yml yaml xml csv tsv".split()

def run(args):
  """@param args: RunArgs"""
  log = logging.getLogger(__name__)

  info = dict((f, None) for f in args.files)
  for f in info:
    parts = filter(None, RE_PARTS.split(f))
    fn = parts[0]
    ext = fn.rsplit('.')[-1]
    if ext == fn:
      ext = ""
    inds = [i.decode('U8') for i in parts[1:]]
    inds = [eval(i) if i.isnumeric() else i for i in inds]
    if ext == "mat":
      from caspyr.utils import H5Reader
      log.debug("hdf5 file")
      data = H5Reader(fn, prefix=inds[0] if len(inds) else None)
      for i in inds[1:]:
        data = data[i] if isinstance(i, int) else getattr(data, i)
    elif ext in TEXT_EXT:
      with io_open(fn) as fd:
        data = fd.read()
      if inds:
        # line
        data = data.split('\n')[inds[0] - 1]
        if inds[1:]:
          # char / cell
          i = inds[1] - 1
          if ext == "csv":
            data = data.split(',')[i]
          elif ext == "tsv":
            data = data.split('\t')[i]
          else:
            data = data[i]
          if inds[2:]:
            log.warn("ignoring:%r" % inds[2:])
    else:
      log.warn("unknown extension:%s:%s" % (ext, fn))
      data = None
    info[f] = data
  if log.getEffectiveLevel() <= logging.INFO:
    print('\n'.join("{:>20} : {}".format(f[:20], d) for f, d in info.items()))
  return info


def main(argv=None):
  """argv  : list, optional (default: sys.argv[1:])"""
  args = argopt(__doc__ % (__version__, __author__),
                version=__version__).parse_args(args=argv)
  logging.basicConfig(level=getattr(logging, args.log, logging.INFO))
  log = logging.getLogger(__name__)
  log.debug(args)
  return run(args) or 0


if __name__ == "__main__":
  main()
