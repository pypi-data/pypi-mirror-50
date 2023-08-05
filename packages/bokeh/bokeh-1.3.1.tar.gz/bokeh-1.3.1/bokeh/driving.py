#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2019, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
''' Provide a set of decorators useful for repeatedly updating a
a function parameter in a specified way each time the function is
called.

These decorators can be especially useful in conjunction with periodic
callbacks in a Bokeh server application.

Example:

    As an example, consider the ``bounce`` forcing function, which
    advances a sequence forwards and backwards:

    .. code-block:: python

        from bokeh.driving import bounce

        @bounce([0, 1, 2])
        def update(i):
            print(i)

    If this function is repeatedly called, it will print the following
    sequence on standard out:

    .. code-block:: none

        0 1 2 2 1 0 0 1 2 2 1 ...

'''

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
from functools import partial

# External imports

# Bokeh imports

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'bounce',
    'cosine',
    'count',
    'force',
    'linear',
    'repeat',
    'sine',
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

def bounce(sequence):
    ''' Return a driver function that can advance a "bounced" sequence
    of values.

    .. code-block:: none

        seq = [0, 1, 2, 3]

        # bounce(seq) => [0, 1, 2, 3, 3, 2, 1, 0, 0, 1, 2, ...]

    Args:
        sequence (seq) : a sequence of values for the driver to bounce

    '''
    N = len(sequence)
    def f(i):
        div, mod = divmod(i, N)
        if div % 2 == 0:
            return sequence[mod]
        else:
            return sequence[N-mod-1]
    return partial(force, sequence=_advance(f))

def cosine(w, A=1, phi=0, offset=0):
    ''' Return a driver function that can advance a sequence of cosine values.

    .. code-block:: none

        value = A * cos(w*i + phi) + offset

    Args:
        w (float) : a frequency for the cosine driver
        A (float) : an amplitude for the cosine driver
        phi (float) : a phase offset to start the cosine driver with
        offset (float) : a global offset to add to the driver values

    '''
    from math import cos
    def f(i):
        return A * cos(w*i + phi) + offset
    return partial(force, sequence=_advance(f))

def count():
    ''' Return a driver function that can advance a simple count.

    '''
    return partial(force, sequence=_advance(lambda x: x))

def force(f, sequence):
    ''' Return a decorator that can "force" a function with an arbitrary
    supplied generator

    Args:
        sequence (iterable) :
            generator to drive f with

    Returns:
        decorator

    '''
    def wrapper():
        f(next(sequence))
    return wrapper

def linear(m=1, b=0):
    ''' Return a driver function that can advance a sequence of linear values.

    .. code-block:: none

        value = m * i + b

    Args:
        m (float) : a slope for the linear driver
        x (float) : an offset for the linear driver

    '''
    def f(i):
        return m * i + b
    return partial(force, sequence=_advance(f))

def repeat(sequence):
    ''' Return a driver function that can advance a repeated of values.

    .. code-block:: none

        seq = [0, 1, 2, 3]

        # repeat(seq) => [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, ...]

    Args:
        sequence (seq) : a sequence of values for the driver to bounce

    '''
    N = len(sequence)
    def f(i):
        return sequence[i%N]
    return partial(force, sequence=_advance(f))

def sine(w, A=1, phi=0, offset=0):
    ''' Return a driver function that can advance a sequence of sine values.

    .. code-block:: none

        value = A * sin(w*i + phi) + offset

    Args:
        w (float) : a frequency for the sine driver
        A (float) : an amplitude for the sine driver
        phi (float) : a phase offset to start the sine driver with
        offset (float) : a global offset to add to the driver values

    '''
    from math import sin
    def f(i):
        return A * sin(w*i + phi) + offset
    return partial(force, sequence=_advance(f))

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

def _advance(f):
    ''' Yield a sequence generated by calling a given function with
    successively incremented integer values.

    Args:
        f (callable) :
            The function to advance

    Yields:
        f(i) where i increases each call

    '''
    i = 0
    while True:
        yield f(i)
        i += 1

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
