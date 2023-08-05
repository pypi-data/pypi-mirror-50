from subprocess import Popen, PIPE

__author__ = "Casper da Costa-Luis <casper.dcl@physics.org>"
__version__ = "0.2.0"


def sh(*cmd, **kwargs):
  return Popen(cmd, stdout=PIPE,
               **kwargs).communicate()[0].decode("utf-8")


class TqdmStream(object):
  @classmethod
  def write(cls, msg):
    from tqdm import tqdm
    tqdm.write(msg, end='')


def stripEnd(s, ext):
  """Usage:
  >>> stripEnd("some..ext", ".ext")
  "some."
  """
  return s[:-len(ext)] if s.endswith(ext) else s


def inputPrompt(msg="Continue", mid=' ',
                yes="yY", no="nN", end="? ", default=None):
  """
  @param yes  : str, characters to accept for returning `True`.
  @param no   : str, characters to accept for returning `False`.
  @param end  : str, terminating message.
  @param default  : bool or None, if [default: None] will loop until valid input.

  example format for defaults:
      `{msg}{mid}{yes}/{no}{end}`
  produces:
      `Continue yY/nN? `
  """

  if set(yes).intersection(no):
    raise ValueError("Yes/No options overlap")

  prompt = msg + mid
  prompt += "{}/{}".format(yes, no) if default is None else \
      "[{}]{}/{}".format(yes[0], yes[1:], no) if default else \
      "{}/[{}]{}".format(yes, no[0], no[1:])
  prompt += end

  while True:
    a = raw_input(prompt)
    if a in yes:
      return True
    if a in no:
      return False
    if default is not None:
      return default  # TODO: enforce bool?
