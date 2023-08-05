from __future__ import division
import pycuda.driver as cuda
import pycuda.autoinit  # NOQA
from pycuda.compiler import SourceModule
import pycuda.gpuarray as gpuarray
import numpy as np
import logging

__all__ = [
    "cuda", "gpuarray", "CudaFunc3D", "CudaFunc", "cu3D",
    "InC", "OutC", "ensureContiguousArray", "ctypestr"]
__author__ = "Casper da Costa-Luis <casper.dcl@physics.org>"
__version__ = "2.0.0"

In = cuda.In
Out = cuda.Out


def ensureContiguousArray(x):
    if not x.flags['C_CONTIGUOUS']:
        log = logging.getLogger(__name__)
        log.warn("making contiguous")
        x = np.ascontiguousarray(x)
    return x


def InC(x):
    """Convert a numpy array to a pinned contiguous const gpu array"""
    return x if isinstance(x, In) else In(ensureContiguousArray(x))


def OutC(x):
    """Convert a numpy array to a pinned contiguous gpu array"""
    if isinstance(x, Out):
        return x
    if not x.flags['C_CONTIGUOUS']:
        raise TypeError("Output is not contiguous")
    return Out(x)


def ctypestr(dtype):
    """Convert a Python data type to a ctype str"""
    res = np.ctypeslib.as_ctypes_type(dtype).__name__
    assert res[:2] == 'c_'
    return res[2:]


class CudaFunc3D(object):
  @classmethod
  def __getattr__(self, name):
    return dict(
        In=In, Out=Out,
        InC=InC, OutC=OutC,
        ensureContiguousArray=ensureContiguousArray,
        ctypestr=ctypestr,
    )[name]

  @property
  def size(self):
    return self.size_t(reduce(lambda x, y: x * y, self.shape))

  def __init__(self, shape, block_dim=None, grid_dim=None,
               dtype=np.float32, size_t=np.uint32, wrapper=None):
    r"""PyCUDA function wrapper.
    shape  : 3-tuple (x, y, z) of dimensions (used in grid dim calculation)
    block_dim  : 3-tuple (x, y, z) (default: (1024, 1, 1))
    grid_dim  : 3-tuple (x, y, z)
      (default: (shape + block_dim - 1) / block_dim)
    dtype  : (default: float32) for #define DTYPE
    size_t  : (default: uint32) for #define SIZE_T
    wrapper  : 2-tuple string added around `build` code
      (default:
        (
          'extern "C" { __global__ void func',
          '}\n'
        )
      )
    """
    self.start = cuda.Event()
    self.end = cuda.Event()
    self.size_t = getattr(size_t, 'type', size_t)
    self.dtype = getattr(dtype, 'type', dtype)
    self.shape = size_t(shape)

    if block_dim is None:
      self.block_dim = [1024] + [1] * (len(shape) - 1)
    else:
      self.block_dim = block_dim

    if grid_dim is None:
      self.grid_dim = [(n + b - 1) // b
                       for (n, b) in zip(shape, self.block_dim)]
    else:
      self.grid_dim = grid_dim

    if wrapper is None:
      self.wrapper = ['extern "C" { __global__ void func', "}\n"]
    else:
      self.wrapper = wrapper

  def build(self, code, no_extern_c=1, func='func', wrapper=None, **kwargs):
    """Compile module.
    kwargs  : passed to `SourceModule`.
    """
    log = logging.getLogger(__name__)

    define = dict(
        N_DIM_X=self.shape[0],
        N_DIM_Y=self.shape[1],
        N_DIM_Z=self.shape[2],
        N_DIM=sum(self.shape),
        B_DIM_X=self.block_dim[0],
        B_DIM_Y=self.block_dim[1],
        B_DIM_Z=self.block_dim[2],
        SIZE_T=ctypestr(self.size_t),
        DTYPE=ctypestr(self.dtype),
    )
    defs = '\n'.join(map(lambda kv: "#define %s %s" % kv, define.items()))

    code = "\n{d}\n{w[0]}{c}{w[1]}".format(
        d=defs, w=wrapper or self.wrapper, c=code)
    log.debug(code)
    self.func = SourceModule(
        code, no_extern_c=no_extern_c, **kwargs).get_function(func)

  def __call__(self, *args, **kwargs):
    """Launch kernel with given args.
    args  : passed to `self.func`
    kwargs  : passed to `self.func`.
    Optional override of launch paramters via `block` and `grid` kwargs.
    """
    self.start.record()
    k = dict(block=tuple(self.block_dim), grid=tuple(self.grid_dim))
    k.update(kwargs)
    res = self.func(*args, **k)
    self.end.record()
    return res

  def sync(self):
    return self.end.synchronize()

  def elapsed(self):
    return self.start.time_till(self.end) * 1e-3


class CudaFunc(CudaFunc3D):
  def __init__(self, size, block_dim=1024, **k):
    super(CudaFunc, self).__init__(
        (size, 1, 1),
        block_dim=(block_dim, 1, 1),
        grid_dim=((size + block_dim - 1) // block_dim, 1, 1),
        **k)


def cu3D(code, **kwargs):
    r"""
    kwargs  : passed to `CudaFunc3D.build`.

    >>> from caspyr.cuda import cu3D, InC, OutC
    >>> square = cu3D('''
        (       DTYPE dst[N_DIM_X][N_DIM_Y][N_DIM_Z]
        , const DTYPE src[N_DIM_X][N_DIM_Y][N_DIM_Z]
        ){
          SIZE_T x = blockIdx.x * B_DIM_X + threadIdx.x; if(x>=N_DIM_X) return;
          SIZE_T y = blockIdx.y * B_DIM_Y + threadIdx.y; if(y>=N_DIM_Y) return;
          SIZE_T z = blockIdx.z * B_DIM_Z + threadIdx.z; if(z>=N_DIM_Z) return;

          dst[x][y][z] = pow(src[x][y][z], 2);
        }
        ''')

    Now do
        square<<<...>>>(b, a)
    Where `*_DIM_*` is inferred from launch parameters <<<...>>>

    >>> import numpy as np
    >>> a = np.random.rand(512, 512, 512)
    >>> b = np.empty_like(a)
    >>> square(a.shape, [8, 8, 16])(OutC(b), InC(a))
    """
    def kernel(*a, **k):
        knl = CudaFunc3D(*a, **k)
        knl.build(code, **kwargs)
        return knl
    kernel.__doc__ = CudaFunc3D.__init__.__doc__
    return kernel
