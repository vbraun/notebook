"""
Stand-Alone Main Loop

This is a demo implementation without integration into a third-party
event loop. It is for documentation and doctesting purposes, but not
actually used in the Sage notebook.
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

from .main_loop import MainLoopABC


class MainLoopStandalone(MainLoopABC):
    
    def __init__(self):
        super(MainLoopStandalone, self).__init__()
        self._quit = False

    def run(self, debug=None):
        import socket
        while not self._quit:
            rlist, wlist, xlist = self.select_args()
            rlist, wlist, xlist = select.select(rlist, wlist, xlist, 1)
            self.select_handler(rlist, wlist, xlist)
            
    def quit(self):
        self._quit = True
