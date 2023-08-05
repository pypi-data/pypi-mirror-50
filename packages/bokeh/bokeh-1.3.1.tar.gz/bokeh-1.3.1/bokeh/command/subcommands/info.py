#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2019, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
'''

To display information about Bokeh and Bokeh server configuration,
type ``bokeh info`` on the command line.

.. code-block:: sh

    bokeh info

This will print general information to standard output, such as Python and Bokeh versions:

.. code-block:: none

    Python version      :  3.6.5
    IPython version     :  6.3.1
    Bokeh version       :  0.12.15
    BokehJS static path :  /opt/anaconda/lib/python3.6/site-packages/bokeh/server/static
    node.js version     :  v8.11.1
    npm version         :  5.8.0

Sometimes it can be useful to get just paths to the BokehJS static files in order
to configure other servers or processes. To do this, use the ``--static`` option

.. code-block:: sh

    bokeh info --static

This will produce output like what is shown below

.. code-block:: none

    /opt/anaconda/lib/python3.6/site-packages/bokeh/server/static

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
import sys

# External imports

# Bokeh imports
from bokeh import __version__
from bokeh.settings import settings
from bokeh.util.compiler import nodejs_version, npmjs_version
from bokeh.util.dependencies import import_optional

from ..subcommand import Subcommand

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    'Info',
)

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

def _version(modname, attr):
    mod = import_optional(modname)
    if mod:
        return getattr(mod, attr)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

class Info(Subcommand):
    ''' Subcommand to print information about Bokeh and Bokeh server configuration.

    '''

    #: name for this subcommand
    name = "info"

    help = "print information about Bokeh and Bokeh server configuration"

    args = (

        ('--static', dict(
            action='store_true',
            help="Print the locations of BokehJS static files",
        )),

    )

    def invoke(self, args):
        '''

        '''
        if args.static:
            print(settings.bokehjsdir())
        else:
            if_installed = lambda version_or_none: version_or_none or "(not installed)"

            print("Python version      :  %s" % sys.version.split('\n')[0])
            print("IPython version     :  %s" % if_installed(_version('IPython', '__version__')))
            print("Tornado version     :  %s" % if_installed(_version('tornado', 'version')))
            print("Bokeh version       :  %s" % __version__)
            print("BokehJS static path :  %s" % settings.bokehjsdir())
            print("node.js version     :  %s" % if_installed(nodejs_version()))
            print("npm version         :  %s" % if_installed(npmjs_version()))

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
