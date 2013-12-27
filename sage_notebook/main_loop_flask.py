"""
Gevent-Based Main Loop

This is the implementation of :mod:`main_loop` for Flask/gevent.
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
from geventwebsocket.handler import WebSocketHandler


from .main_loop_gevent import MainLoopGevent


class MainLoopFlask(MainLoopGevent):

    def add_view(self, view):
        self.flask_app = view.flask_app

    def run(self, debug=None):
        self._debug = debug
        #self._sage_greenlet = gevent.Greenlet.spawn(self.loop, debug=debug)
        self._httpd_greenlet = gevent.Greenlet.spawn(self.httpd, debug=debug)
        self.run_forever()

    def run_forever(self):
        #self._sage_greenlet.join()
        self._httpd_greenlet.join()

    def httpd(self, debug=None):
        httpd = gevent.pywsgi.WSGIServer(
            ('localhost', 5000), self.flask_app, handler_class=WebSocketHandler)
        httpd.serve_forever()
