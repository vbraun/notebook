"""
Handle Command Line Options and Launch the Sage Notebook
"""

##############################################################################
#  Sage Notebook: A Graphical User Interface for Sage
#  Copyright (C) 2013  Volker Braun <vbraun.name@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################


import sys
import os
import importlib
import logging

from .logger import logger



def check_gtk_prerequisites():
    try:
        from gi.repository import Gtk
    except ImportError:
        logger.critical('Missing dependency: GTK3 Python interface.')
        sys.exit(1)
    try:
        from gi.repository import GtkSource, GObject
        GObject.type_register(GtkSource.View)
    except ImportError:
        logger.critical('Missing dependency: GtkSourceView widget.')
        sys.exit(1)        
    try:
        import cairo
    except ImportError:
        logger.critical('Missing dependency: Python Cairo interface.')
        sys.exit(1)
    try: 
        from gi.repository import Vte
    except ImportError:
        logger.critical('Missing dependency: VTE terminal widget.')
        sys.exit(1)



def launch_gtk(debug=False):
    check_gtk_prerequisites()
    from sage_notebook.app import Application
    app = Application('gtk')
    app.run(debug)
    logger.debug('Main loop quit')


def launch_flask(debug=False):
    from sage_notebook.app import Application
    app = Application('flask')
    app.run(debug)


description = """
The Sage Notebook
"""


def run_doctests(args):
    from sage_notebook.doctest.control import DocTestController
    DC = DocTestController(*args)
    err = DC.run()
    sys.exit(err)


def launch():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=description)
    parser.add_argument('--debug', dest='debug', action='store_true',
                        default=False, help='debug')
    parser.add_argument('--doctest', dest='doctest', action='store_true',
                        default=False, help='doctest')
    parser.add_argument('--log', dest='log', default=None,
                        help='one of [DEBUG, INFO, ERROR, WARNING, CRITICAL]')
    args = parser.parse_args()
    if args.log is not None:
        level = getattr(logging, args.log)
        logger.setLevel(level=level)
    if args.doctest:
        raise ValueError('run test.py for now')
    else:
        launch_gtk(debug=args.debug)
