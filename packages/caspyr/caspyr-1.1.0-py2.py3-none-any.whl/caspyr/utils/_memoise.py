try:
  import cPickle as pickle
except ImportError:
  import pickle

import logging

__author__ = "Casper da Costa-Luis <casper.dcl@physics.org>"
__version__ = "0.3.0"


def memoise(ignore_kwargs=None, ignore_args=None):
  if ignore_kwargs is None:
    ignore_kwargs = []
  if ignore_args is None:
    ignore_args = []
  db = {}
  log = logging.getLogger(__name__)

  def wrapper(fn):
    def inner(*a, **kw):
      vs = tuple(str(v) for v in a if v not in ignore_args)
      ks = sorted(
          (str(k), str(v)) for k, v in kw.items() if k not in ignore_kwargs)
      key = vs + tuple(ks)
      res = db.get(key, None)
      if res is None:
        log.info("miss:" + fn.__name__)
        log.info("key:" + str(key))
        db[key] = res = fn(*a, **kw)
      else:
        log.info("hit:" + fn.__name__)
      return res
    return inner
  return wrapper


def load_db(shmDB):
  from io import open
  fname = "/dev/shm/" + shmDB
  db = {}
  try:
    db = pickle.load(open(fname, "rb"))
  except IOError as e:
    if "no such file" not in str(e).lower():
      log = logging.getLogger(__name__)
      log.warn("Could not load db. Possibly first time?")
      log.warn(str(e))
  return db


def save_db(shmDB, db):
  from io import open
  fname = "/dev/shm/" + shmDB
  pickle.dump(db, open(fname, "wb"), -1)


def hashForce(i):
  """returns hash(str(i)) if hash(i) fails"""
  try:
    return hash(i)
  except TypeError:
    return hash(str(i))


def memo_db(shmDB, ignore_kwargs=None, ignore_args=None):
  """memoise to /dev/shm/"""
  if ignore_kwargs is None:
    ignore_kwargs = []
  if ignore_args is None:
    ignore_args = []
  db = load_db(shmDB)
  log = logging.getLogger(__name__)

  def wrapper(fn):
    def inner(*a, **kw):
      vs = tuple(str(v) for v in a if v not in ignore_args)
      ks = sorted(
          (str(k), str(v)) for k, v in kw.items() if k not in ignore_kwargs)
      key = vs + tuple(ks)
      res = db.get(key, None)
      if res is None:
        log.info("miss:" + fn.__name__)
        log.info("key:" + str(key))
        db[key] = res = fn(*a, **kw)
        save_db(shmDB, db)
      else:
        log.info("hit:" + fn.__name__)
      return res
    return inner
  return wrapper
