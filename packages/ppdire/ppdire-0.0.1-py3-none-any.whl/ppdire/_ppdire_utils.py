#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:37:56 2019

@author: sven
"""

@classmethod   
def _get_param_names(cls):
    """Get parameter names for the estimator"""
    # fetch the constructor or the original constructor before
    # deprecation wrapping if any
    init = getattr(cls.__init__, 'deprecated_original', cls.__init__)
    if init is object.__init__:
        # No explicit constructor to introspect
        return []

    # introspect the constructor arguments to find the model parameters
    # to represent
    init_signature = inspect.signature(init)
    # Consider the constructor parameters excluding 'self'
    parameters = [p for p in init_signature.parameters.values()
                  if p.name != 'self' and p.kind != p.VAR_KEYWORD]
    for p in parameters:
        if p.kind == p.VAR_POSITIONAL:
            raise RuntimeError("scikit-learn estimators should always "
                               "specify their parameters in the signature"
                               " of their __init__ (no varargs)."
                               " %s with constructor %s doesn't "
                               " follow this convention."
                               % (cls, init_signature))
    # Extract and sort argument names excluding 'self'
    return sorted([p.name for p in parameters])

def get_params(self, deep=False):
    """Get parameters for this estimator.
    Parameters
    ----------
    deep : boolean, optional
        If True, will return the parameters for this estimator and
        contained subobjects that are estimators.
    Returns
    -------
    params : mapping of string to any
        Parameter names mapped to their values.
    ------
    Copied from ScikitLlearn instead of imported to avoid 'deep=True'
    """
    out = dict()
    for key in self._get_param_names():
        value = getattr(self, key, None)
        if deep and hasattr(value, 'get_params'):
            deep_items = value.get_params().items()
            out.update((key + '__' + k, val) for k, val in deep_items)
        out[key] = value
    return out
    
def set_params(self, **params):
    """Set the parameters of this estimator.
    Copied from ScikitLearn, adapted to avoid calling 'deep=True'
    Returns
    -------
    self
    ------
    Copied from ScikitLlearn instead of imported to avoid 'deep=True'
    """
    if not params:
        # Simple optimization to gain speed (inspect is slow)
        return self
    valid_params = self.get_params()

    nested_params = defaultdict(dict)  # grouped by prefix
    for key, value in params.items():
        key, delim, sub_key = key.partition('__')
        if key not in valid_params:
            raise ValueError('Invalid parameter %s for estimator %s. '
                             'Check the list of available parameters '
                             'with `estimator.get_params().keys()`.' %
                             (key, self))

        if delim:
            nested_params[key][sub_key] = value
        else:
            setattr(self, key, value)
            valid_params[key] = value

    for key, sub_params in nested_params.items():
        valid_params[key].set_params(**sub_params)

    return self
