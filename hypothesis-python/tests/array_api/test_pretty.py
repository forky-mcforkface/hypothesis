# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Copyright the Hypothesis Authors.
# Individual contributors are listed in AUTHORS.rst and the git log.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.

from inspect import signature

import pytest


@pytest.mark.parametrize(
    "name",
    [
        "from_dtype",
        "arrays",
        "array_shapes",
        "scalar_dtypes",
        "boolean_dtypes",
        "numeric_dtypes",
        "integer_dtypes",
        "unsigned_integer_dtypes",
        "floating_dtypes",
        "valid_tuple_axes",
        "broadcastable_shapes",
        "mutually_broadcastable_shapes",
        "indices",
    ],
)
def test_namespaced_methods_meta(xp, xps, name):
    """Namespaced method objects have good meta attributes."""
    func = getattr(xps, name)
    assert func.__name__ == name
    assert func.__doc__ is not None
    # The (private) top-level strategy methods may expose a xp argument in their
    # function signatures. make_strategies_namespace() exists to wrap these
    # top-level methods by binding the passed xp argument, and so the namespace
    # it returns should not expose xp in any of its function signatures.
    assert "xp" not in signature(func).parameters.keys()


@pytest.mark.parametrize(
    "name, valid_args",
    [
        ("from_dtype", ["int8"]),
        ("arrays", ["int8", 5]),
        ("array_shapes", []),
        ("scalar_dtypes", []),
        ("boolean_dtypes", []),
        ("numeric_dtypes", []),
        ("integer_dtypes", []),
        ("unsigned_integer_dtypes", []),
        ("floating_dtypes", []),
        ("valid_tuple_axes", [0]),
        ("broadcastable_shapes", [()]),
        ("mutually_broadcastable_shapes", [3]),
        ("indices", [(5,)]),
    ],
)
def test_namespaced_strategies_repr(xp, xps, name, valid_args):
    """Namespaced strategies have good repr."""
    func = getattr(xps, name)
    strat = func(*valid_args)
    assert repr(strat).startswith(name + "("), f"{name} not in strat repr {strat!r}"
    assert len(repr(strat)) < 100, "strat repr looks too long"
    assert xp.__name__ not in repr(strat), f"{xp.__name__} in strat repr"


def test_strategies_namespace_repr(xp, xps):
    """Strategies namespace has good repr."""
    expected = f"make_strategies_namespace({xp.__name__})"
    assert repr(xps) == expected
    assert str(xps) == expected
