"""
Gevent-Based Main Loop

This is the implementation of :mod:`main_loop` for gevent.
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

import logging
logger = logging.getLogger('GUI')

import gevent
import gevent.select
from .main_loop import MainLoopABC



class MainLoopGevent(MainLoopABC):

    def __init__(self):
        super(MainLoopGevent, self).__init__()
        self._debug = None
        self._quit = False

    def run(self, debug=None):
        self._debug = debug
        self._greenlet = gevent.Greenlet.spawn(self.loop, debug=debug)
        self.run_forever()

    def run_forever(self):
        self._greenlet.join()

    def loop(self, debug=None):
        while not self._quit:
            rlist, wlist, xlist = self.select_args()
            rlist, wlist, xlist = gevent.select.select(rlist, wlist, xlist, 1)
            # print('gevent loop', rlist, wlist, xlist)
            self.select_handler(rlist, wlist, xlist)
        
    def quit(self):
        self._quit = True

    def select_setup():
        raise NotImplementedError

