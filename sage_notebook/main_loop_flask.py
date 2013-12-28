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
from geventwebsocket.handler import WSGIHandler, WebSocketHandler


from .main_loop_gevent import MainLoopGevent


def request_logger(self):
    """
    Callback to log requests using Flask's request logger
    """
    log = self.server.log
    if log:
        if hasattr(log, 'info'):
            log.info(self.format_request() + '\n')
        else:
            log.write(self.format_request() + '\n')



class MainLoopFlask(MainLoopGevent):

    def add_view(self, view):
        self.flask_app = view.flask_app

    def run(self, debug=None):
        self._debug = debug
        self._sage_greenlet = gevent.Greenlet.spawn(self.loop, debug=debug)
        self._httpd_greenlet = gevent.Greenlet.spawn(self.httpd, debug=debug)
        if debug is None:
            self.run_forever()
        else:
            self.flask_app.debug = True
            self.debug_shell(debug)

    def run_forever(self):
        self._sage_greenlet.join()
        self._httpd_greenlet.join()

    def debug_shell(self, app):
        """
        Variant of :meth:`run_forever` that drops us into an IPython shell
        """
        from IPython.terminal.ipapp import TerminalIPythonApp
        ip = TerminalIPythonApp.instance()
        ip.initialize(argv=[])
        ip.shell.user_global_ns['app'] = app
        def ipy_import(module_name, identifier):
            module = importlib.import_module(module_name)
            ip.shell.user_global_ns[identifier] = getattr(module, identifier) 
        #ipy_import('sage_notebook.model.git_interface', 'GitInterface')
        from IPython.lib.inputhook import inputhook_manager
        inputhook_manager.set_inputhook(self.ipython_inputhook)
        ip.start()

    def ipython_inputhook(self):
        self._httpd_greenlet.join(0)
        self._sage_greenlet.join(0)
        return True

    def httpd(self, debug=None):
        httpd = gevent.pywsgi.WSGIServer(
            ('localhost', 5000), self.flask_app, 
            handler_class=WebSocketHandler)
        if debug is not None:
            WebSocketHandler.log_request = request_logger
        httpd.serve_forever()
