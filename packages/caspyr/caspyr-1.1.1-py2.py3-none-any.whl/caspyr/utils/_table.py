__author__ = "Casper da Costa-Luis <casper.dcl@physics.org>"
__version__ = "0.0.0"


def table(data, ipy=True, fmt=str, md=False):
  """Data tabulator

  Parameters
  ----------
  data  : 2D iterable
  ipy  : attempt to display HTML object
  fmt  : format function for each cell
  md  : return markdown instead of html
  """
  raw = "<table>\n <tr>\n  <td>" + "</td>\n </tr><tr>\n  <td>".join(
      "</td><td>".join(map(fmt, i)) for i in data) + "</td>\n </tr>\n</table>"
  if ipy:
    try:
      from IPython.display import HTML, display
    except ImportError:
      pass
    else:
      display(HTML(raw))
  if md:
    raw = "\n".join("|".join(map(fmt, i)) for i in data)
  return raw
