#!/usr/bin/env python
"""duplicate v%s

A python file (which generates itself) to get you started on new scripts.

Usage:
  duplicate [options] [<output>]

Options:
  -f, --force  : Force overwriting files.
  --log LEVEL  : (FAT|CRITIC)AL|ERROR|WARN(ING)|[default: INFO]|DEBUG|NOTSET

Arguments:
  [<output>]  : Output duplicate file name (default: self~).
                Use '-' for stdout.

%s
"""
import sys
from io import open as io_open
from os import path
import logging
from argopt import argopt
from ..utils import inputPrompt, stripEnd
__all__ = ["main", "run"]
__version__ = "0.0.0"
__author__ = "Casper da Costa-Luis <casper.dcl@physics.org>"


def run(args):
  """@param args: RunArgs"""
  log = logging.getLogger(__name__)

  this_file_raw = __file__
  for ext in ('c', 'o', ''):
    this_file_raw = stripEnd(this_file_raw, ".py" + ext)

  with io_open(this_file_raw + ".py") as fd:
    this_file_raw = fd.read()

  if path.isfile(args.output):
    log.warn("file %s exists." % args.output)
    if not (args.force or inputPrompt("Overwrite")):
      return -1
    log.info("Overwriting " + args.output)

  with (sys.stdout if args.output == '-' else io_open(args.output, 'w')) as fd:
    fd.write(this_file_raw)


def main(argv=None):
  """argv  : list, optional (default: sys.argv[1:])"""
  args = argopt(__doc__ % (__version__, __author__),
                version=__version__).parse_args(args=argv)
  logging.basicConfig(level=getattr(logging, args.log, logging.INFO))
  log = logging.getLogger(__name__)
  if args.output is None:
    args.output = sys.argv[0] + '~'
  log.debug(args)
  return run(args) or 0


if __name__ == "__main__":
  main()
