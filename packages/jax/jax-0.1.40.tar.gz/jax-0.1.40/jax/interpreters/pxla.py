# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import namedtuple
from contextlib import contextmanager
import itertools as it
import operator as op

import numpy as onp
import six
from six.moves import reduce

from .. import core
from .. import linear_util as lu
from ..abstract_arrays import ConcreteArray, ShapedArray, make_shaped_array
from ..util import partial, unzip2, concatenate, prod, memoize_unary
from ..lib import xla_bridge as xb
from .xla import xla_shape, xla_destructure, xla_shape_to_result_shape
from .partial_eval import trace_to_subjaxpr, merge_pvals, JaxprTrace, PartialVal
from .batching import dimsize, broadcast
from . import batching
from . import partial_eval as pe
from . import xla
from . import ad


### util

def identity(x): return x

# TODO(mattjj, phawkins): improve re-distribution not to copy to host
def shard_arg(device_ordinals, axis_size, arg):
  """Shard an argument data array arg along its leading axis.

  Args:
    device_ordinals: list of integers of length num_replicas mapping a logical
      replica index to a physical device number.
    axis_size: int, size of the axis to be sharded.
    arg: a JaxType representing an argument to be sharded along its leading axis
      (or the leading axis of its leaves in the tuple case) and placed on the
      devices indicated by `device_ordinals`.

  Returns:
    A list of device buffers with the same length as `device_ordinals` indexed
    by replica number, so that the nth element is the argument to be passed to
    the nth replica.
  """
  nrep = len(device_ordinals)
  assignments = assign_shards_to_replicas(nrep, axis_size)
  if (type(arg) in (ShardedDeviceArray, ShardedDeviceTuple)
      and nrep == len(arg.device_buffers)):
    _, ids = onp.unique(assignments, return_index=True)
    get_shard = memoize_unary(lambda i: arg.device_buffers[i].to_py())
    return [buf if buf.device() == device_ordinals[r]
            else xla.device_put(get_shard(i), device_ordinals[r])
            for r, (i, buf) in enumerate(zip(assignments, arg.device_buffers))]
  else:
    shards = [(_slice(arg, assignments[i]), device_ordinals[i])
              for i in range(len(assignments))]
    return [xla.device_put(v, device) for v, device in shards]

def _slice(x, i):
  """Return the ith slice of a JaxType (tuple or array)."""
  if isinstance(x, core.JaxTuple):
    return core.pack(_slice(elt, i) for elt in x)
  else:
    return x[i]


def xla_shard(c, sizes, x):
  def _xla_shard(shape, x):
    if shape.is_tuple():
      elts = map(_xla_shard, shape.tuple_shapes(), xla_destructure(c, x))
      return c.Tuple(*elts)
    else:
      return shard_array(shape, x)

  def shard_array(shape, x):
    dims = list(shape.dimensions())
    assert dims[0] == sizes[-1]
    start_indices = _xla_shard_start_indices(c, dims[0], len(dims))
    return c.Reshape(c.DynamicSlice(x, start_indices, [1] + dims[1:]),
                     None, dims[1:])

  return _xla_shard(c.GetShape(x), x)

# TODO(b/110096942): more efficient gather
def xla_unshard(c, replica_groups, x):
  def _xla_unshard(shape, x):
    if shape.is_tuple():
      elts = map(_xla_unshard, shape.tuple_shapes(), xla_destructure(c, x))
      return c.Tuple(*elts)
    else:
      return unshard_array(shape, x)

  def unshard_array(shape, x):
    axis_size = len(replica_groups[0])
    dims = list(shape.dimensions())
    start_indices = _xla_shard_start_indices(c, axis_size, len(dims) + 1)
    padded = c.Broadcast(c.Constant(onp.array(0, shape.numpy_dtype())),
                         [axis_size] + dims)
    padded = c.DynamicUpdateSlice(padded, c.Reshape(x, None, [1] + dims),
                                  start_indices)
    return c.CrossReplicaSum(padded, replica_groups)

  return _xla_unshard(c.GetShape(x), x)


# TODO(mattjj): plumb more ergonimic form of DynamicSlice / DynamicUpdateSlice
def _xla_shard_start_indices(c, axis_size, ndim):
  idx = c.Rem(c.ReplicaId(), c.Constant(onp.array(axis_size, onp.uint32)))
  zero = onp.zeros(ndim - 1, onp.uint32)
  return c.Concatenate([c.Reshape(idx, None, [1]), c.Constant(zero)], 0)


def sharded_result_handler(axis_size, aval):
  full_aval = add_axis_to_aval(axis_size, aval)
  if type(aval) is core.AbstractTuple:
    return partial(sharded_tuple_result_handler, axis_size, full_aval)
  elif isinstance(aval, ShapedArray):
    return partial(sharded_array_result_handler, full_aval)
  else:
    raise TypeError(type(aval))

def sharded_array_result_handler(aval, replica_results):
  t, = set(map(type, replica_results))
  if t is xla.DeviceArray:
    bufs = [r.device_buffer for r in replica_results]
    return ShardedDeviceArray(aval, bufs)
  else:
    assignments = assign_shards_to_replicas(len(replica_results), aval.shape[0])
    _, ids = onp.unique(assignments, return_index=True)
    return onp.stack([replica_results[i] for i in ids])

def sharded_tuple_result_handler(axis_size, aval, replica_results):
  t, = set(map(type, replica_results))
  if t is xla.DeviceTuple:
    bufs = [r.device_buffer for r in replica_results]
    return ShardedDeviceTuple(axis_size, aval, bufs)
  elif t is core.JaxTuple:
    # e.g. pmap(lambda x: core.pack((3, x)))(...)
    reduced_aval = remove_axis_from_aval(aval)
    all_results = zip(*replica_results)
    return core.pack([sharded_result_handler(axis_size, elt_aval)(results)
                      for elt_aval, results in zip(reduced_aval, all_results)])
  else:
    raise TypeError(t)


def add_axis_to_aval(n, aval):
  if type(aval) is core.AbstractTuple:
    return core.AbstractTuple(map(partial(add_axis_to_aval, n), aval))
  elif isinstance(aval, ShapedArray):
    return ShapedArray((n,) + aval.shape, aval.dtype)
  else:
    raise TypeError(type(aval))

def remove_axis_from_aval(aval):
  if type(aval) is core.AbstractTuple:
    return core.AbstractTuple(map(remove_axis_from_aval, aval))
  elif isinstance(aval, ShapedArray):
    return ShapedArray(aval.shape[1:], aval.dtype)
  else:
    raise TypeError(aval)


def assign_shards_to_replicas(nrep, size):
  """Produce a mapping from replica id to shard index.

  Args:
    nrep: int, number of replicas (a computation-dependent value).
    size: int, size of the data array axis being sharded.

  Returns:
    A tuple of integers of length nrep in which the elements take on values from
    0 to size-1. Replica n is assgined shard data_array[assignments[n]].
  """
  groupsize, ragged = divmod(nrep, size)
  assert not ragged
  indices = onp.tile(onp.arange(size)[:, None], (1, groupsize))
  return tuple(indices.ravel())

def replica_groups(nrep, mesh_spec, mesh_axes):
  """Compute XLA replica groups from a replica count and device mesh data.

  Args:
    nrep: int, number of replicas (a computation-dependent value).
    mesh_spec: tuple of integers, a specification of the logical device mesh,
      which depends on the lexical context of nested xla_pmaps. In particular,
      each xla_pmap effectively appends its mapped axis size to this tuple.
    mesh_axes: tuple of ints, logical device mesh axis indices indicating the
      axes along which collective operations are to be executed.

  Returns:
    replica_groups, a list of lists of ints encoding a partition of the set
      {0, 1, ..., nrep} into equally-sized replica groups (within which
      collectives are executed). XLA consumes this replica group specification.
  """
  trailing_size, ragged = divmod(nrep, prod(mesh_spec))
  assert not ragged
  full_spec = mesh_spec + [trailing_size]
  iota = onp.arange(prod(full_spec)).reshape(full_spec)
  groups = onp.reshape(
      onp.moveaxis(iota, mesh_axes, onp.arange(len(mesh_axes))),
      (prod(onp.take(full_spec, mesh_axes)), -1))
  return tuple(map(tuple, groups.T))


### the main pmap machinery lowers SPMD jaxprs to multi-replica XLA computations

def compile_replicated(jaxpr, axis_name, axis_size, consts, *abstract_args):
  num_replicas = axis_size * xla.jaxpr_replicas(jaxpr)
  if num_replicas > xb.device_count():
    msg = ("compiling computation that requires {} replicas, but only {} XLA "
           "devices are available")
    raise ValueError(msg.format(num_replicas, xb.device_count()))
  axis_env = xla.AxisEnv(num_replicas, [axis_name], [axis_size])
  arg_shapes = list(map(xla_shape, abstract_args))
  built_c = xla._jaxpr_computation(jaxpr, axis_env, consts, (), *arg_shapes)
  result_shape = xla_shape_to_result_shape(built_c.GetReturnValueShape())
  compiled = built_c.Compile(arg_shapes, xb.get_compile_options(num_replicas),
                             backend=xb.get_backend())
  return compiled, num_replicas, result_shape


### applying parallel primitives in op-by-op Python dispatch

# There are at least two cases where we might want to evaluate a parallel
# primitive dispatched from Python, rather than being staged out:
#   1. axis_size = psum(1, 'axis_name'),
#   2. to enable an implicit outermost pmap-like context for multi-host
#      multi-controller SPMD programs.
# In each case, we can't rely on any data dependence on a pmap trace; instead we
# need some dynamic context, basically modeling the axis name environment stack.
# To handle the former case, we don't need to communicate at all; we instead
# have a table of parallel_pure_rules. To handle the latter case, we'll have a
# globally-scoped root environment frame and compile and execute a single-op
# XLA collective.

class DynamicAxisEnvFrame(object):
  __slots__ = ["name", "pmap_trace", "hard_size", "soft_trace", "soft_size"]
  def __init__(self, name, pmap_trace, hard_size):
    self.name = name
    self.pmap_trace = pmap_trace
    self.hard_size = hard_size
    self.soft_trace = None
    self.soft_size = None

class DynamicAxisEnv(list):
  def __contains__(self, axis_name):
    return axis_name in (frame.name for frame in self)

  def __getitem__(self, axis_name):
    if axis_name not in self:
      raise NameError("unbound axis name: {}".format(axis_name))
    for frame in reversed(self):
      if frame.name == axis_name:
        return frame
    else:
      assert False
dynamic_axis_env = DynamicAxisEnv()

@contextmanager
def extend_dynamic_axis_env(axis_name, pmap_trace, hard_size):
  dynamic_axis_env.append(DynamicAxisEnvFrame(axis_name, pmap_trace, hard_size))
  yield
  dynamic_axis_env.pop()

def unmapped_device_count():
  mapped = prod(frame.hard_size for frame in dynamic_axis_env)
  unmapped, ragged = divmod(xb.device_count(), mapped)
  assert not ragged and unmapped > 0
  return unmapped

def apply_parallel_primitive(prim, *args, **params):
  # This is the op-by-op version of applying a collective primitive, like a psum
  # that doesn't have a data dependence on the argument of a pmap function. In
  # particular, this code gets hit when we write `axis_size = psum(1, 'i')`. We
  # look up information in the dynamic axis env.
  axis_name = params.pop('axis_name')
  logical_size = lambda frame: frame.hard_size * (frame.soft_size or 1)
  if isinstance(axis_name, (list, tuple)):
    shape = tuple(logical_size(dynamic_axis_env[name]) for name in axis_name)
  else:
    shape = (logical_size(dynamic_axis_env[axis_name]),)
  return parallel_pure_rules[prim](*args, shape=shape, **params)

parallel_pure_rules = {}


def axis_index(axis_name):
  frame = dynamic_axis_env[axis_name]
  dummy_arg = frame.pmap_trace.pure(core.unit)
  if frame.soft_trace:
    dummy_arg = frame.soft_trace.pure(dummy_arg)
  return axis_index_p.bind(dummy_arg, hard_size=frame.hard_size,
                           soft_size=frame.soft_size, axis_name=axis_name)

def _axis_index_partial_eval(trace, _, **params):
  # This partial_eval rule adds the axis_index primitive into the jaxpr formed
  # during pmap lowering. It is like the standard JaxprTrace.process_primitive
  # rule except that we don't attempt to lower out of the trace.
  out_aval = ShapedArray((), onp.uint32)
  eqn = pe.JaxprEqn([], None, axis_index_p, (), False, False, params)
  return pe.JaxprTracer(trace, pe.PartialVal((out_aval, core.unit)), eqn)

axis_index_p = core.Primitive('axis_index')
xla.translations[axis_index_p] = lambda c, hard_size, soft_size, axis_name: \
    c.Rem(c.ReplicaId(), c.Constant(onp.array(hard_size, onp.uint32)))
pe.custom_partial_eval_rules[axis_index_p] = _axis_index_partial_eval


### lazy device-memory persistence and result handling

class ShardedDeviceValue(xla.DeviceValue):
  def _check_if_deleted(self):
    if self.device_buffers is None:
      raise ValueError("ShardedDeviceValue has been deleted.")

  def block_until_ready(self):
    self._check_if_deleted()
    for buf in self.device_buffers:
      buf.block_host_until_ready()


class ShardedDeviceTuple(ShardedDeviceValue, xla.DeviceTuple):
  """A ShardedDeviceTuple is a JaxTuple sharded across devices.

  The purpose of a ShardedDeviceTuple is to reduce the number of transfers when
  executing replicated computations, by allowing results to persist on the
  devices that produced them. That way dispatching a similarly replicated
  computation that consumes the same sharded memory layout does not incur any
  transfers.

  A ShardedDeviceTuple represents one logical JaxTuple value, and simulates the
  behavior of a JaxTuple so that it can be treated by user code as a JaxTuple;
  that is, it is only an optimization to reduce transfers.

  The number of device buffers underlying a ShardedDeviceTuple instance is equal
  to the number of replicas of the computation that produced it. Each buffer
  represents a shard of the logical tuple value represented by the
  ShardedDeviceTuple, where a shard of an array is a slice along its leading
  axis, and a shard of a tuple is a tuple of corresponding shards of its
  elements. These component buffers reside on distinct devices, but need not
  represent distinct logical shards.
  """
  __slots__ = ["device_buffers", "axis_size", "aval"]

  def __init__(self, axis_size, aval, device_buffers):
    assert device_buffers
    self.device_buffers = device_buffers
    self.axis_size = axis_size
    self.aval = aval

  # To destructure, we destructure the constituent buffers on each device, then
  # logically concatenate those shards across devices producing one logically
  # concatenated result per element. The logical concatenation is performed with
  # the result handler logic applied to the elements.
  def __iter__(self):
    all_bufs = zip(*[buf.destructure() for buf in self.device_buffers])
    handlers = map(partial(tuple_element_handler, self.axis_size), self.aval)
    elts = [handler(bufs) for handler, bufs in zip(handlers, all_bufs)]
    return iter(elts)

  def __len__(self):
    return len(self.aval)

  def __repr__(self):
    return 'ShardedDeviceTuple(len={length})'.format(length=len(self))

def tuple_element_handler(axis_size, aval):
  t = type(aval)
  if t is core.AbstractTuple:
    return partial(ShardedDeviceTuple, axis_size, aval)
  elif t is ShapedArray:
    return partial(ShardedDeviceArray, aval)
  else:
    raise TypeError(t)


core.pytype_aval_mappings[ShardedDeviceTuple] = core.pytype_aval_mappings[core.JaxTuple]
xla.pytype_aval_mappings[ShardedDeviceTuple] = op.attrgetter('aval')
batching.pytype_aval_mappings[ShardedDeviceTuple] = op.attrgetter('aval')
xla.canonicalize_dtype_handlers[ShardedDeviceTuple] = \
    xla.canonicalize_dtype_handlers[xla.DeviceTuple]

xb.register_constant_handler(ShardedDeviceTuple, xla._device_tuple_constant_handler)


class ShardedDeviceArray(ShardedDeviceValue, xla.DeviceArray):
  """A ShardedDeviceArray is an ndarray sharded across devices.

  The purpose of a ShardedDeviceArray is to reduce the number of transfers when
  executing replicated computations, by allowing results to persist on the
  devices that produced them. That way dispatching a similarly replicated
  computation that consumes the same sharded memory layout does not incur any
  transfers.

  A ShardedDeviceArray represents one logical ndarray value, and simulates the
  behavior of an ndarray so that it can be treated by user code as an ndarray;
  that is, it is only an optimization to reduce transfers.

  The number of device buffers underlying a ShardedDeviceArray instance is equal
  to the number of replicas of the computation that produced it. Each buffer
  represents a shard of the original array, meaning a slice along its leading
  axis. These component buffers reside on distinct devices, but need not
  represent distinct logical shards. The correspondence can be computed with
  the assign_shards_to_replicas function.
  """
  __slots__ = ["device_buffers", "axis_size"]
  _collect = staticmethod(onp.stack)

  def __init__(self, aval, device_buffers):
    self.device_buffers = device_buffers
    self.shape, self.dtype = aval.shape, aval.dtype
    self.ndim, self.size = len(aval.shape), prod(aval.shape)
    self.axis_size = aval.shape[0]
    self._npy_value = None

  def _ids(self):
    num_bufs = len(self.device_buffers)
    assignments = assign_shards_to_replicas(num_bufs, self.axis_size)
    _, ids = onp.unique(assignments, return_index=True)
    return ids

  def copy_to_host_async(self):
    if self._npy_value is None:
      for buf in self.device_buffers:
        buf.copy_to_host_async()

  def delete(self):
    for buf in self.device_buffers:
      buf.delete()
    self.device_buffers = None
    self._npy_value = None

  @property
  def _value(self):
    if self._npy_value is None:
      ids = self._ids()
      self.copy_to_host_async()
      self._npy_value = self._collect([self.device_buffers[i].to_py() for i in ids])
    return self._npy_value

  def __getitem__(self, idx):
    if self._npy_value is None and type(idx) is int:
      ids = self._ids()
      device_buffer = self.device_buffers[ids[idx]]
      result_shape = xla_shape_to_result_shape(device_buffer.shape())
      handler = xla._device_persistent_result_handler(result_shape)
      return handler(device_buffer)
    else:
      return super(ShardedDeviceArray, self).__getitem__(idx)

core.pytype_aval_mappings[ShardedDeviceArray] = ConcreteArray
xla.pytype_aval_mappings[ShardedDeviceArray] = \
    xla.pytype_aval_mappings[xla.DeviceArray]
batching.pytype_aval_mappings[ShardedDeviceArray] = \
    batching.pytype_aval_mappings[xla.DeviceArray]
xla.canonicalize_dtype_handlers[ShardedDeviceArray] = \
    xla.canonicalize_dtype_handlers[xla.DeviceArray]

xb.register_constant_handler(ShardedDeviceArray,
                             xla._device_array_constant_handler)


class ChunkedDeviceArray(ShardedDeviceArray):
  __slots__ = []
  _collect = staticmethod(onp.concatenate)

  def __init__(self, axis_size, aval, device_buffers):
    super(ChunkedDeviceArray, self).__init__(aval, device_buffers)
    self.axis_size = axis_size

  def __getitem__(self, idx):
    return xla.DeviceArray.__getitem__(self, idx)

core.pytype_aval_mappings[ChunkedDeviceArray] = ConcreteArray
xla.pytype_aval_mappings[ChunkedDeviceArray] = \
    xla.pytype_aval_mappings[xla.DeviceArray]
batching.pytype_aval_mappings[ChunkedDeviceArray] = \
    batching.pytype_aval_mappings[xla.DeviceArray]
xla.canonicalize_dtype_handlers[ChunkedDeviceArray] = \
    xla.canonicalize_dtype_handlers[xla.DeviceArray]

xb.register_constant_handler(ChunkedDeviceArray,
                             xla._device_array_constant_handler)


### the xla_pmap primitive and its rules are comparable to xla_call in xla.py

def xla_pmap_impl(fun, *args, **params):
  axis_name = params.pop('axis_name')
  axis_size = params.pop('axis_size')
  assert not params
  abstract_args = map(partial(abstractify, axis_size), args)
  compiled_fun = parallel_callable(fun, axis_name, axis_size, *abstract_args)
  return compiled_fun(*args)

def abstractify(axis_size, x):
  return _shard_aval(axis_size, xla.abstractify(x))

def _shard_aval(axis_size, aval):
  if type(aval) is core.AbstractTuple:
    return core.AbstractTuple(map(partial(_shard_aval, axis_size), aval))
  elif type(aval) is ShapedArray:
    assert aval.shape[0] == axis_size
    return ShapedArray(aval.shape[1:], aval.dtype)
  else:
    raise TypeError(aval)

@lu.memoize
def parallel_callable(fun, axis_name, axis_size, *avals):
  pvals = [PartialVal((aval, core.unit)) for aval in avals]
  pval = PartialVal((core.AbstractTuple(()), core.unit))  # dummy value

  @lu.wrap_init
  def dynamic_fun(dummy, *args):
    with extend_dynamic_axis_env(axis_name, dummy.trace, axis_size):
      return fun.call_wrapped(*args)

  with core.new_master(JaxprTrace, True) as master:
    jaxpr, (out_pval, consts, env) = \
        trace_to_subjaxpr(dynamic_fun, master, False).call_wrapped([pval] + pvals)
    jaxpr.invars = jaxpr.invars[1:]  # ignore dummy
    assert not env
    del master
  out_pv, out_const = out_pval
  if out_pv is None:
    # When the output doesn't depend on the input we don't need to compile an
    # XLA computation at all; we handle this as a special case so we can stage
    # out multi-replica XLA computations regardless of the hardware available.
    result_handler = sharded_result_handler(axis_size, xla.abstractify(out_const))
    return lambda *args: result_handler([out_const] * axis_size)
  else:
    out = compile_replicated(jaxpr, axis_name, axis_size, consts, *avals)
    compiled, nrep, shard_result_shape = out
    handle_arg = partial(shard_arg, compiled.DeviceOrdinals(), axis_size)
    handle_replica_result = xla.result_handler(shard_result_shape)
    handle_full_result = sharded_result_handler(axis_size, merged_aval(out_pval))
    return partial(execute_replicated, compiled, out_pval, nrep,
                   handle_arg, handle_replica_result, handle_full_result)

def merged_aval(pval):
  pv, const = pval
  if isinstance(pv, core.AbstractValue):
    return pv
  elif isinstance(pv, pe.JaxprTracerTuple):
    return core.AbstractTuple(map(merged_aval, zip(pv, const)))
  elif pv is None:
    return xla.abstractify(const)
  else:
    raise TypeError(type(pv))

def execute_replicated(compiled, pval, nrep, handle_in,
                       handle_replica_result, handle_full_result, *args):
  if nrep > xb.device_count():
    msg = ("executing pmap computation that requires {} replicas, but only {} "
           "XLA devices are available")
    raise ValueError(msg.format(nrep, xb.device_count()))
  input_bufs = zip(*map(handle_in, args)) if args else [[]] * nrep
  out_bufs = compiled.ExecutePerReplica(list(input_bufs))
  results = [merge_pvals(handle_replica_result(buf), pval) for buf in out_bufs]
  return handle_full_result(results)


xla_pmap_p = core.Primitive('xla_pmap')
xla_pmap = partial(core.call_bind, xla_pmap_p)
xla_pmap_p.def_custom_bind(xla_pmap)
xla_pmap_p.def_impl(xla_pmap_impl)

def _xla_pmap_translation_rule(c, jaxpr, axis_env, env_nodes, in_nodes,
                               axis_name, axis_size):
  new_env = xla.extend_axis_env(axis_env, axis_name, axis_size)
  in_nodes_sharded = list(map(partial(xla_shard, c, new_env.sizes), in_nodes))
  subc = xla._jaxpr_computation(jaxpr, new_env, (),
                                tuple(map(c.GetShape, env_nodes)),
                                *map(c.GetShape, in_nodes_sharded))
  sharded_result = c.Call(subc, env_nodes + in_nodes_sharded)
  return xla_unshard(c, xla.axis_groups(new_env, axis_name), sharded_result)
xla.call_translations[xla_pmap_p] = _xla_pmap_translation_rule
ad.primitive_transposes[xla_pmap_p] = partial(ad.map_transpose, xla_pmap_p)
pe.map_primitives.add(xla_pmap_p)


### soft_pmap axis split transformation

# To allow pmap to map over logical axes larger than the number of XLA devices
# available, we use a transformation that effectively simulates having more
# devices in software. The strategy is to split the mapped axis into two axes,
# one to be hardware-mapped and the other to be software-mapped. Thus the
# transformation rewrites the function to be mapped so that it accepts a new
# leading axis (the software-mapped axis), and so that collectives in the
# original function correspond to both device-local operations and collective
# communication operations across hardware devices that implement the original
# logical semantics.

@lu.transformation
def split_axis(axis_name, chunk_size, *args):
  with core.new_master(SplitAxisTrace) as master:
    trace = SplitAxisTrace(master, core.cur_sublevel())
    in_tracers = map(partial(SplitAxisTracer, trace, axis_name), args)
    with add_chunk_to_axis_env(axis_name, trace, chunk_size):
      ans = yield in_tracers, {}
    out_tracer = trace.full_raise(ans)
    out_val, out_axis = out_tracer.val, out_tracer.axis_name
    del master, out_tracer
  if out_axis is not_mapped:
    out_val = batching.broadcast2(chunk_size, 0, out_val)
  yield out_val

@lu.transformation_with_aux
def split_axis_subtrace(master, names, *vals):
  trace = SplitAxisTrace(master, core.cur_sublevel())
  ans = yield map(partial(SplitAxisTracer, trace), names, vals), {}
  out_tracer = trace.full_raise(ans)
  out_val, out_name = out_tracer.val, out_tracer.axis_name
  yield out_val, out_name

class NotMapped(object): pass
not_mapped = NotMapped

class SplitAxisTuple(tuple): pass

@contextmanager
def add_chunk_to_axis_env(axis_name, soft_trace, soft_size):
  dynamic_axis_env[axis_name].soft_trace = soft_trace
  dynamic_axis_env[axis_name].soft_size = soft_size
  yield
  dynamic_axis_env[axis_name].soft_trace = None
  dynamic_axis_env[axis_name].soft_size = None

class SplitAxisTracer(core.Tracer):
  def __init__(self, trace, axis_name, val):
    self.trace = trace
    self.axis_name = axis_name
    self.val = val

  @property
  def aval(self):
    aval = batching.get_aval(self.val)
    if self.axis_name is not_mapped:
      return aval
    else:
      return batching.remove_batch_dim_from_aval(0, aval)

  def unpack(self):
    if self.name is not_mapped:
      return tuple(self.val)
    else:
      if type(self.name) is SplitAxisTuple:
        names = list(self.name)
      else:
        names = [self.name] * len(self.val)
      return map(partial(SplitAxisTracer, self.trace), names, self.val)

  def full_lower(self):
    if self.axis_name is not_mapped:
      return core.full_lower(self.val)
    else:
      return self

class SplitAxisTrace(core.Trace):
  def pure(self, val):
    return SplitAxisTracer(self, not_mapped, val)

  def lift(self, val):
    return SplitAxisTracer(self, not_mapped, val)

  def sublift(self, val):
    return SplitAxisTracer(self, val.axis_name, val.val)

  def process_primitive(self, primitive, tracers, params):
    vals_in, names_in = unzip2((t.val, t.axis_name) for t in tracers)
    if primitive is axis_index_p:
      dummy, = vals_in
      hard_idx = primitive.bind(dummy, **params)
      val_out = hard_idx * params['soft_size'] + onp.arange(params['soft_size'])
      return SplitAxisTracer(self, params['axis_name'], val_out)
    elif all(axis_name is not_mapped for axis_name in names_in):
      return primitive.bind(*vals_in, **params)
    else:
      name, = set(n for n in names_in if n is not not_mapped)
      if primitive in xla.parallel_translations:
        # if it's a pmap collective primitive, do something special
        if name == params['axis_name']:
          # if the name matches this tracer's name, apply the split_axis rule
          try:
            rule = split_axis_rules[primitive]
          except KeyError:
            msg = "split_axis for {} not implemented. Open a feature request!"
            raise NotImplementedError(msg.format(primitive))
          which_mapped = [n is not not_mapped for n in names_in]
          val_out, is_mapped = rule(vals_in, which_mapped, **params)
          name_out = name if is_mapped else not_mapped
          return SplitAxisTracer(self, name_out, val_out)
        else:
          # if not, bind the primitive without any processing
          val_out = primitive.bind(*vals_in, **params)
          return SplitAxisTracer(self, name, val_out)
      else:
        # if it's not a pmap collective primitive, act just like batching
        rule = batching.get_primitive_batcher(primitive)
        axes_in = [None if n is not_mapped else 0 for n in names_in]
        val_out, axis_out = rule(vals_in, axes_in, **params)
        if axis_out is None:
          return SplitAxisTracer(self, not_mapped, val_out)
        else:
          val_out = batching.moveaxis2(axis_out, 0, val_out)
          return SplitAxisTracer(self, name, val_out)

  def process_call(self, call_primitive, f, tracers, params):
    if call_primitive in pe.map_primitives:
      return self.process_map(call_primitive, f, tracers, params)
    else:
      vals, names = unzip2((t.val, t.axis_name) for t in tracers)
      if all(name is not_mapped for name in names):
        return call_primitive.bind(f, *vals, **params)
      else:
        f, name_out = split_axis_subtrace(f, self.master, names)
        val_out = call_primitive.bind(f, *vals, **params)
        return SplitAxisTracer(self, name_out(), val_out)

  def process_map(self, map_primitive, f, tracers, params):
    vals, names = unzip2((t.val, t.axis_name) for t in tracers)
    if all(name is not_mapped for name in names):
        return map_primitive.bind(f, *vals, **params)
    else:
      # because the map primitive maps over leading axes, we need to transpose
      # the software-mapped axis on any mapped arguments to be the second axis;
      # then we call the map primitive and resume the trace under the call
      vals_transposed = map(partial(transpose_mapped, 0, 1), names, vals)
      f, name_out = split_axis_subtrace(f, self.master, names)
      val_out_transposed = map_primitive.bind(f, *vals_transposed, **params)
      val_out = transpose_mapped(1, 0, name_out(), val_out_transposed)
      return SplitAxisTracer(self, name_out(), val_out)

  def post_process_call(self, call_primitive, out_tracer, params):
    val, name = out_tracer.val, out_tracer.axis_name
    master = self.master
    def todo(x):
      trace = SplitAxisTrace(master, core.cur_sublevel())
      return  SplitAxisTracer(trace, name, x)
    return  val, todo

  def pack(self, tracers):
    vals, names = unzip2((t.val, t.axis_name) for t in tracers)
    return SplitAxisTracer(self, SplitAxisTuple(names), core.pack(vals))

def transpose_mapped(src, dst, name, x):
  def transpose(name, x):
    if type(name) is SplitAxisTuple:
      return core.pack(map(transpose, name, x))
    elif name is not_mapped:
      return x
    else:
      return batching.moveaxis2(src,  dst, x)
  return transpose(name, x)


split_axis_rules = {}
