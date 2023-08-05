"""Python wrappers around TensorFlow ops.

This file is MACHINE GENERATED! Do not edit.
Original C++ source file: lattice_interpolation_py_wrapper.cc
"""

import collections as _collections
import six as _six

from tensorflow.python import pywrap_tensorflow as _pywrap_tensorflow
from tensorflow.python.eager import context as _context
from tensorflow.python.eager import core as _core
from tensorflow.python.eager import execute as _execute
from tensorflow.python.framework import dtypes as _dtypes
from tensorflow.python.framework import errors as _errors
from tensorflow.python.framework import tensor_shape as _tensor_shape

from tensorflow.core.framework import op_def_pb2 as _op_def_pb2
# Needed to trigger the call to _set_call_cpp_shape_fn.
from tensorflow.python.framework import common_shapes as _common_shapes
from tensorflow.python.framework import op_def_registry as _op_def_registry
from tensorflow.python.framework import ops as _ops
from tensorflow.python.framework import op_def_library as _op_def_library
from tensorflow.python.util.deprecation import deprecated_endpoints
from tensorflow.python.util import dispatch as _dispatch
from tensorflow.python.util.tf_export import tf_export
from tensorflow.python.util.tf_export import kwarg_only as _kwarg_only
from tensorflow.tools.docs import doc_controls as _doc_controls


@_dispatch.add_dispatch_list
@tf_export('hypercube_gradient')
def hypercube_gradient(input, weight, grad_wrt_weight, lattice_sizes=[], name=None):
  r"""Computes gradients of HypercubeInterpolation. Returns a dense gradient.

  Inputs
    input: input tensor, `[?, d]`.
    grad_wrt_weight: Gradient with respect to the outputs of this operator,
    `[?, m_0 x m_1 x .. x m_{d - 1}]`

  Outputs
    grad_wrt_input: A gradient tensor, `[?, d]`, with respect to input.

  Args:
    input: A `Tensor`. Must be one of the following types: `float32`, `float64`.
    weight: A `Tensor`. Must have the same type as `input`.
    grad_wrt_weight: A `Tensor`. Must have the same type as `input`.
    lattice_sizes: An optional list of `ints`. Defaults to `[]`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor`. Has the same type as `input`.
  """
  _ctx = _context._context or _context.context()
  if _ctx is not None and _ctx._thread_local_data.is_eager:
    try:
      _result = _pywrap_tensorflow.TFE_Py_FastPathExecute(
        _ctx._context_handle, _ctx._thread_local_data.device_name,
        "HypercubeGradient", name, _ctx._post_execution_callbacks, input,
        weight, grad_wrt_weight, "lattice_sizes", lattice_sizes)
      return _result
    except _core._FallbackException:
      try:
        return hypercube_gradient_eager_fallback(
            input, weight, grad_wrt_weight, lattice_sizes=lattice_sizes,
            name=name, ctx=_ctx)
      except _core._SymbolicException:
        pass  # Add nodes to the TensorFlow graph.
      except (TypeError, ValueError):
        result = _dispatch.dispatch(
              hypercube_gradient, input=input, weight=weight,
                                  grad_wrt_weight=grad_wrt_weight,
                                  lattice_sizes=lattice_sizes, name=name)
        if result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
          return result
        raise
    except _core._NotOkStatusException as e:
      if name is not None:
        message = e.message + " name: " + name
      else:
        message = e.message
      _six.raise_from(_core._status_to_exception(e.code, message), None)
  # Add nodes to the TensorFlow graph.
  if lattice_sizes is None:
    lattice_sizes = []
  if not isinstance(lattice_sizes, (list, tuple)):
    raise TypeError(
        "Expected list for 'lattice_sizes' argument to "
        "'hypercube_gradient' Op, not %r." % lattice_sizes)
  lattice_sizes = [_execute.make_int(_i, "lattice_sizes") for _i in lattice_sizes]
  try:
    _, _, _op = _op_def_lib._apply_op_helper(
        "HypercubeGradient", input=input, weight=weight,
                             grad_wrt_weight=grad_wrt_weight,
                             lattice_sizes=lattice_sizes, name=name)
  except (TypeError, ValueError):
    result = _dispatch.dispatch(
          hypercube_gradient, input=input, weight=weight,
                              grad_wrt_weight=grad_wrt_weight,
                              lattice_sizes=lattice_sizes, name=name)
    if result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return result
    raise
  _result = _op.outputs[:]
  _inputs_flat = _op.inputs
  _attrs = ("Dtype", _op.get_attr("Dtype"), "lattice_sizes",
            _op.get_attr("lattice_sizes"))
  _execute.record_gradient(
      "HypercubeGradient", _inputs_flat, _attrs, _result, name)
  _result, = _result
  return _result

def HypercubeGradient(input, weight, grad_wrt_weight, lattice_sizes=[], name=None):
  return hypercube_gradient(input=input, weight=weight, grad_wrt_weight=grad_wrt_weight, lattice_sizes=lattice_sizes, name=name)
HypercubeGradient.__doc__ = hypercube_gradient.__doc__
HypercubeGradient = _doc_controls.do_not_generate_docs(_kwarg_only(HypercubeGradient))
tf_export("raw_ops.HypercubeGradient")(HypercubeGradient)


def hypercube_gradient_eager_fallback(input, weight, grad_wrt_weight, lattice_sizes=[], name=None, ctx=None):
  r"""This is the slowpath function for Eager mode.
  This is for function hypercube_gradient
  """
  _ctx = ctx if ctx else _context.context()
  if lattice_sizes is None:
    lattice_sizes = []
  if not isinstance(lattice_sizes, (list, tuple)):
    raise TypeError(
        "Expected list for 'lattice_sizes' argument to "
        "'hypercube_gradient' Op, not %r." % lattice_sizes)
  lattice_sizes = [_execute.make_int(_i, "lattice_sizes") for _i in lattice_sizes]
  _attr_Dtype, _inputs_Dtype = _execute.args_to_matching_eager([input, weight, grad_wrt_weight], _ctx, _dtypes.float32)
  (input, weight, grad_wrt_weight) = _inputs_Dtype
  _inputs_flat = [input, weight, grad_wrt_weight]
  _attrs = ("Dtype", _attr_Dtype, "lattice_sizes", lattice_sizes)
  _result = _execute.execute(b"HypercubeGradient", 1, inputs=_inputs_flat,
                             attrs=_attrs, ctx=_ctx, name=name)
  _execute.record_gradient(
      "HypercubeGradient", _inputs_flat, _attrs, _result, name)
  _result, = _result
  return _result


@_dispatch.add_dispatch_list
@tf_export('hypercube_interpolation')
def hypercube_interpolation(input, lattice_sizes=[], name=None):
  r"""Returns a tensor representing interpolation weights in a hypercube lattice

  interpolation.

  Inputs
    input: 2D tensor, `[?, d]`

  Params
    lattice_sizes: 1D int tensor that contains a lattice size per each dimension,
    [m_0, ..., m_{d - 1}].

  Outputs
    weights: 2D tensor that contains interpolation weights.
    [?, m_0 x m_1 ... x m_{d - 1}].

  Args:
    input: A `Tensor`. Must be one of the following types: `float32`, `float64`.
    lattice_sizes: An optional list of `ints`. Defaults to `[]`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor`. Has the same type as `input`.
  """
  _ctx = _context._context or _context.context()
  if _ctx is not None and _ctx._thread_local_data.is_eager:
    try:
      _result = _pywrap_tensorflow.TFE_Py_FastPathExecute(
        _ctx._context_handle, _ctx._thread_local_data.device_name,
        "HypercubeInterpolation", name, _ctx._post_execution_callbacks, input,
        "lattice_sizes", lattice_sizes)
      return _result
    except _core._FallbackException:
      try:
        return hypercube_interpolation_eager_fallback(
            input, lattice_sizes=lattice_sizes, name=name, ctx=_ctx)
      except _core._SymbolicException:
        pass  # Add nodes to the TensorFlow graph.
      except (TypeError, ValueError):
        result = _dispatch.dispatch(
              hypercube_interpolation, input=input,
                                       lattice_sizes=lattice_sizes, name=name)
        if result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
          return result
        raise
    except _core._NotOkStatusException as e:
      if name is not None:
        message = e.message + " name: " + name
      else:
        message = e.message
      _six.raise_from(_core._status_to_exception(e.code, message), None)
  # Add nodes to the TensorFlow graph.
  if lattice_sizes is None:
    lattice_sizes = []
  if not isinstance(lattice_sizes, (list, tuple)):
    raise TypeError(
        "Expected list for 'lattice_sizes' argument to "
        "'hypercube_interpolation' Op, not %r." % lattice_sizes)
  lattice_sizes = [_execute.make_int(_i, "lattice_sizes") for _i in lattice_sizes]
  try:
    _, _, _op = _op_def_lib._apply_op_helper(
        "HypercubeInterpolation", input=input, lattice_sizes=lattice_sizes,
                                  name=name)
  except (TypeError, ValueError):
    result = _dispatch.dispatch(
          hypercube_interpolation, input=input, lattice_sizes=lattice_sizes,
                                   name=name)
    if result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return result
    raise
  _result = _op.outputs[:]
  _inputs_flat = _op.inputs
  _attrs = ("Dtype", _op.get_attr("Dtype"), "lattice_sizes",
            _op.get_attr("lattice_sizes"))
  _execute.record_gradient(
      "HypercubeInterpolation", _inputs_flat, _attrs, _result, name)
  _result, = _result
  return _result

def HypercubeInterpolation(input, lattice_sizes=[], name=None):
  return hypercube_interpolation(input=input, lattice_sizes=lattice_sizes, name=name)
HypercubeInterpolation.__doc__ = hypercube_interpolation.__doc__
HypercubeInterpolation = _doc_controls.do_not_generate_docs(_kwarg_only(HypercubeInterpolation))
tf_export("raw_ops.HypercubeInterpolation")(HypercubeInterpolation)


def hypercube_interpolation_eager_fallback(input, lattice_sizes=[], name=None, ctx=None):
  r"""This is the slowpath function for Eager mode.
  This is for function hypercube_interpolation
  """
  _ctx = ctx if ctx else _context.context()
  if lattice_sizes is None:
    lattice_sizes = []
  if not isinstance(lattice_sizes, (list, tuple)):
    raise TypeError(
        "Expected list for 'lattice_sizes' argument to "
        "'hypercube_interpolation' Op, not %r." % lattice_sizes)
  lattice_sizes = [_execute.make_int(_i, "lattice_sizes") for _i in lattice_sizes]
  _attr_Dtype, (input,) = _execute.args_to_matching_eager([input], _ctx, _dtypes.float32)
  _inputs_flat = [input]
  _attrs = ("Dtype", _attr_Dtype, "lattice_sizes", lattice_sizes)
  _result = _execute.execute(b"HypercubeInterpolation", 1,
                             inputs=_inputs_flat, attrs=_attrs, ctx=_ctx,
                             name=name)
  _execute.record_gradient(
      "HypercubeInterpolation", _inputs_flat, _attrs, _result, name)
  _result, = _result
  return _result


@_dispatch.add_dispatch_list
@tf_export('simplex_gradient')
def simplex_gradient(input, weight, grad_wrt_weight, lattice_sizes=[], name=None):
  r"""Computes gradients of SimplexInterpolation. Returns a dense gradient.

  Inputs
    input: input tensor, `[?, d]`.
    grad_wrt_weight: Gradient with respect to the outputs of this operator,
    `[?, m_0 x m_1 x .. x m_{d - 1}]`

  Outputs
    grad_wrt_input: A gradient tensor, `[?, d]`, with respect to input.

  Args:
    input: A `Tensor`. Must be one of the following types: `float32`, `float64`.
    weight: A `Tensor`. Must have the same type as `input`.
    grad_wrt_weight: A `Tensor`. Must have the same type as `input`.
    lattice_sizes: An optional list of `ints`. Defaults to `[]`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor`. Has the same type as `input`.
  """
  _ctx = _context._context or _context.context()
  if _ctx is not None and _ctx._thread_local_data.is_eager:
    try:
      _result = _pywrap_tensorflow.TFE_Py_FastPathExecute(
        _ctx._context_handle, _ctx._thread_local_data.device_name,
        "SimplexGradient", name, _ctx._post_execution_callbacks, input,
        weight, grad_wrt_weight, "lattice_sizes", lattice_sizes)
      return _result
    except _core._FallbackException:
      try:
        return simplex_gradient_eager_fallback(
            input, weight, grad_wrt_weight, lattice_sizes=lattice_sizes,
            name=name, ctx=_ctx)
      except _core._SymbolicException:
        pass  # Add nodes to the TensorFlow graph.
      except (TypeError, ValueError):
        result = _dispatch.dispatch(
              simplex_gradient, input=input, weight=weight,
                                grad_wrt_weight=grad_wrt_weight,
                                lattice_sizes=lattice_sizes, name=name)
        if result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
          return result
        raise
    except _core._NotOkStatusException as e:
      if name is not None:
        message = e.message + " name: " + name
      else:
        message = e.message
      _six.raise_from(_core._status_to_exception(e.code, message), None)
  # Add nodes to the TensorFlow graph.
  if lattice_sizes is None:
    lattice_sizes = []
  if not isinstance(lattice_sizes, (list, tuple)):
    raise TypeError(
        "Expected list for 'lattice_sizes' argument to "
        "'simplex_gradient' Op, not %r." % lattice_sizes)
  lattice_sizes = [_execute.make_int(_i, "lattice_sizes") for _i in lattice_sizes]
  try:
    _, _, _op = _op_def_lib._apply_op_helper(
        "SimplexGradient", input=input, weight=weight,
                           grad_wrt_weight=grad_wrt_weight,
                           lattice_sizes=lattice_sizes, name=name)
  except (TypeError, ValueError):
    result = _dispatch.dispatch(
          simplex_gradient, input=input, weight=weight,
                            grad_wrt_weight=grad_wrt_weight,
                            lattice_sizes=lattice_sizes, name=name)
    if result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return result
    raise
  _result = _op.outputs[:]
  _inputs_flat = _op.inputs
  _attrs = ("Dtype", _op.get_attr("Dtype"), "lattice_sizes",
            _op.get_attr("lattice_sizes"))
  _execute.record_gradient(
      "SimplexGradient", _inputs_flat, _attrs, _result, name)
  _result, = _result
  return _result

def SimplexGradient(input, weight, grad_wrt_weight, lattice_sizes=[], name=None):
  return simplex_gradient(input=input, weight=weight, grad_wrt_weight=grad_wrt_weight, lattice_sizes=lattice_sizes, name=name)
SimplexGradient.__doc__ = simplex_gradient.__doc__
SimplexGradient = _doc_controls.do_not_generate_docs(_kwarg_only(SimplexGradient))
tf_export("raw_ops.SimplexGradient")(SimplexGradient)


def simplex_gradient_eager_fallback(input, weight, grad_wrt_weight, lattice_sizes=[], name=None, ctx=None):
  r"""This is the slowpath function for Eager mode.
  This is for function simplex_gradient
  """
  _ctx = ctx if ctx else _context.context()
  if lattice_sizes is None:
    lattice_sizes = []
  if not isinstance(lattice_sizes, (list, tuple)):
    raise TypeError(
        "Expected list for 'lattice_sizes' argument to "
        "'simplex_gradient' Op, not %r." % lattice_sizes)
  lattice_sizes = [_execute.make_int(_i, "lattice_sizes") for _i in lattice_sizes]
  _attr_Dtype, _inputs_Dtype = _execute.args_to_matching_eager([input, weight, grad_wrt_weight], _ctx, _dtypes.float32)
  (input, weight, grad_wrt_weight) = _inputs_Dtype
  _inputs_flat = [input, weight, grad_wrt_weight]
  _attrs = ("Dtype", _attr_Dtype, "lattice_sizes", lattice_sizes)
  _result = _execute.execute(b"SimplexGradient", 1, inputs=_inputs_flat,
                             attrs=_attrs, ctx=_ctx, name=name)
  _execute.record_gradient(
      "SimplexGradient", _inputs_flat, _attrs, _result, name)
  _result, = _result
  return _result


@_dispatch.add_dispatch_list
@tf_export('simplex_interpolation')
def simplex_interpolation(input, lattice_sizes=[], name=None):
  r"""Returns a tensor representing interpolation weights in a simplex lattice

  interpolation.

  Inputs
    input: 2D tensor, `[?, d]`

  Params
    lattice_sizes: 1D int tensor that contains a lattice size per each dimension,
    [m_0, ..., m_{d - 1}].

  Outputs
    weights: 2D tensor that contains interpolation weights.
    [?, m_0 x m_1 ... x m_{d - 1}].

  Args:
    input: A `Tensor`. Must be one of the following types: `float32`, `float64`.
    lattice_sizes: An optional list of `ints`. Defaults to `[]`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor`. Has the same type as `input`.
  """
  _ctx = _context._context or _context.context()
  if _ctx is not None and _ctx._thread_local_data.is_eager:
    try:
      _result = _pywrap_tensorflow.TFE_Py_FastPathExecute(
        _ctx._context_handle, _ctx._thread_local_data.device_name,
        "SimplexInterpolation", name, _ctx._post_execution_callbacks, input,
        "lattice_sizes", lattice_sizes)
      return _result
    except _core._FallbackException:
      try:
        return simplex_interpolation_eager_fallback(
            input, lattice_sizes=lattice_sizes, name=name, ctx=_ctx)
      except _core._SymbolicException:
        pass  # Add nodes to the TensorFlow graph.
      except (TypeError, ValueError):
        result = _dispatch.dispatch(
              simplex_interpolation, input=input, lattice_sizes=lattice_sizes,
                                     name=name)
        if result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
          return result
        raise
    except _core._NotOkStatusException as e:
      if name is not None:
        message = e.message + " name: " + name
      else:
        message = e.message
      _six.raise_from(_core._status_to_exception(e.code, message), None)
  # Add nodes to the TensorFlow graph.
  if lattice_sizes is None:
    lattice_sizes = []
  if not isinstance(lattice_sizes, (list, tuple)):
    raise TypeError(
        "Expected list for 'lattice_sizes' argument to "
        "'simplex_interpolation' Op, not %r." % lattice_sizes)
  lattice_sizes = [_execute.make_int(_i, "lattice_sizes") for _i in lattice_sizes]
  try:
    _, _, _op = _op_def_lib._apply_op_helper(
        "SimplexInterpolation", input=input, lattice_sizes=lattice_sizes,
                                name=name)
  except (TypeError, ValueError):
    result = _dispatch.dispatch(
          simplex_interpolation, input=input, lattice_sizes=lattice_sizes,
                                 name=name)
    if result is not _dispatch.OpDispatcher.NOT_SUPPORTED:
      return result
    raise
  _result = _op.outputs[:]
  _inputs_flat = _op.inputs
  _attrs = ("Dtype", _op.get_attr("Dtype"), "lattice_sizes",
            _op.get_attr("lattice_sizes"))
  _execute.record_gradient(
      "SimplexInterpolation", _inputs_flat, _attrs, _result, name)
  _result, = _result
  return _result

def SimplexInterpolation(input, lattice_sizes=[], name=None):
  return simplex_interpolation(input=input, lattice_sizes=lattice_sizes, name=name)
SimplexInterpolation.__doc__ = simplex_interpolation.__doc__
SimplexInterpolation = _doc_controls.do_not_generate_docs(_kwarg_only(SimplexInterpolation))
tf_export("raw_ops.SimplexInterpolation")(SimplexInterpolation)


def simplex_interpolation_eager_fallback(input, lattice_sizes=[], name=None, ctx=None):
  r"""This is the slowpath function for Eager mode.
  This is for function simplex_interpolation
  """
  _ctx = ctx if ctx else _context.context()
  if lattice_sizes is None:
    lattice_sizes = []
  if not isinstance(lattice_sizes, (list, tuple)):
    raise TypeError(
        "Expected list for 'lattice_sizes' argument to "
        "'simplex_interpolation' Op, not %r." % lattice_sizes)
  lattice_sizes = [_execute.make_int(_i, "lattice_sizes") for _i in lattice_sizes]
  _attr_Dtype, (input,) = _execute.args_to_matching_eager([input], _ctx, _dtypes.float32)
  _inputs_flat = [input]
  _attrs = ("Dtype", _attr_Dtype, "lattice_sizes", lattice_sizes)
  _result = _execute.execute(b"SimplexInterpolation", 1, inputs=_inputs_flat,
                             attrs=_attrs, ctx=_ctx, name=name)
  _execute.record_gradient(
      "SimplexInterpolation", _inputs_flat, _attrs, _result, name)
  _result, = _result
  return _result

def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib
# op {
#   name: "HypercubeGradient"
#   input_arg {
#     name: "input"
#     type_attr: "Dtype"
#   }
#   input_arg {
#     name: "weight"
#     type_attr: "Dtype"
#   }
#   input_arg {
#     name: "grad_wrt_weight"
#     type_attr: "Dtype"
#   }
#   output_arg {
#     name: "grad_wrt_input"
#     type_attr: "Dtype"
#   }
#   attr {
#     name: "Dtype"
#     type: "type"
#     default_value {
#       type: DT_FLOAT
#     }
#     allowed_values {
#       list {
#         type: DT_FLOAT
#         type: DT_DOUBLE
#       }
#     }
#   }
#   attr {
#     name: "lattice_sizes"
#     type: "list(int)"
#     default_value {
#       list {
#       }
#     }
#   }
# }
# op {
#   name: "HypercubeInterpolation"
#   input_arg {
#     name: "input"
#     type_attr: "Dtype"
#   }
#   output_arg {
#     name: "weights"
#     type_attr: "Dtype"
#   }
#   attr {
#     name: "Dtype"
#     type: "type"
#     default_value {
#       type: DT_FLOAT
#     }
#     allowed_values {
#       list {
#         type: DT_FLOAT
#         type: DT_DOUBLE
#       }
#     }
#   }
#   attr {
#     name: "lattice_sizes"
#     type: "list(int)"
#     default_value {
#       list {
#       }
#     }
#   }
# }
# op {
#   name: "SimplexGradient"
#   input_arg {
#     name: "input"
#     type_attr: "Dtype"
#   }
#   input_arg {
#     name: "weight"
#     type_attr: "Dtype"
#   }
#   input_arg {
#     name: "grad_wrt_weight"
#     type_attr: "Dtype"
#   }
#   output_arg {
#     name: "grad_wrt_input"
#     type_attr: "Dtype"
#   }
#   attr {
#     name: "Dtype"
#     type: "type"
#     default_value {
#       type: DT_FLOAT
#     }
#     allowed_values {
#       list {
#         type: DT_FLOAT
#         type: DT_DOUBLE
#       }
#     }
#   }
#   attr {
#     name: "lattice_sizes"
#     type: "list(int)"
#     default_value {
#       list {
#       }
#     }
#   }
# }
# op {
#   name: "SimplexInterpolation"
#   input_arg {
#     name: "input"
#     type_attr: "Dtype"
#   }
#   output_arg {
#     name: "weights"
#     type_attr: "Dtype"
#   }
#   attr {
#     name: "Dtype"
#     type: "type"
#     default_value {
#       type: DT_FLOAT
#     }
#     allowed_values {
#       list {
#         type: DT_FLOAT
#         type: DT_DOUBLE
#       }
#     }
#   }
#   attr {
#     name: "lattice_sizes"
#     type: "list(int)"
#     default_value {
#       list {
#       }
#     }
#   }
# }
_op_def_lib = _InitOpDefLibrary(b"\n\242\001\n\021HypercubeGradient\022\016\n\005input\"\005Dtype\022\017\n\006weight\"\005Dtype\022\030\n\017grad_wrt_weight\"\005Dtype\032\027\n\016grad_wrt_input\"\005Dtype\"\031\n\005Dtype\022\004type\032\0020\001:\006\n\0042\002\001\002\"\036\n\rlattice_sizes\022\tlist(int)\032\002\n\000\nu\n\026HypercubeInterpolation\022\016\n\005input\"\005Dtype\032\020\n\007weights\"\005Dtype\"\031\n\005Dtype\022\004type\032\0020\001:\006\n\0042\002\001\002\"\036\n\rlattice_sizes\022\tlist(int)\032\002\n\000\n\240\001\n\017SimplexGradient\022\016\n\005input\"\005Dtype\022\017\n\006weight\"\005Dtype\022\030\n\017grad_wrt_weight\"\005Dtype\032\027\n\016grad_wrt_input\"\005Dtype\"\031\n\005Dtype\022\004type\032\0020\001:\006\n\0042\002\001\002\"\036\n\rlattice_sizes\022\tlist(int)\032\002\n\000\ns\n\024SimplexInterpolation\022\016\n\005input\"\005Dtype\032\020\n\007weights\"\005Dtype\"\031\n\005Dtype\022\004type\032\0020\001:\006\n\0042\002\001\002\"\036\n\rlattice_sizes\022\tlist(int)\032\002\n\000")
