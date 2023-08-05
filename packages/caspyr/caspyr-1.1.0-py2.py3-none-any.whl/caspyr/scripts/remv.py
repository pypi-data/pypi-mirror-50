#!/usr/bin/env python
"""REgexMove v%s
Usage:
  remv [options] <ipattern> <opattern>

Options:
  -n, --dry_run  : only print commands
  -r, --recurse  : recurse into subdirectories
  --log=<lvl>    : CRITICAL|ERROR|WARN(ING)|[default: INFO]|DEBUG|NOTSET
%s
"""
from argopt import argopt
import logging
import re
from os import walk as os_walk
from os import path as os_path
from shutil import move as shutil_move
__author__ = "Casper da Costa-Luis <casper.dcl@physics.org>"
__all__ = ["main"]
__version__ = "0.1.2"


def run(args):
  log = logging.getLogger(__name__)
  if args.recurse:
    allFiles = [os_path.join(d, f) for (d, _, fs) in os_walk('.')
                for f in fs]
  else:
    allFiles = os_walk('.').next()[2]
  RE_IPAT = re.compile(args.ipattern)
  for f in allFiles:
    if RE_IPAT.search(f):
      dst = RE_IPAT.sub(args.opattern, f)
      log.info(' '.join(("mv", f, dst)))
      if not args.dry_run:
        shutil_move(f, dst)


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
