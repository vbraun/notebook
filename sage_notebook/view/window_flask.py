"""
Windows (Webpages) in Flask

This is the Flask implementation of :mod:`window`.

In the Sage notebook, a window is a long-lived object. We do not free
the resources when a window is closed to avoid having to reconstruct
the GUI when it is reopened.

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


from .window import WindowABC, ModalDialogABC
import flask



class WindowFlask(WindowABC):
    """
    Flask Window
    """

    @property
    def url(self):
        return '/' + self.name + '/'
        
    @property
    def endpoint(self):
        """
        The Endpoint

        An endpoint is a name (string) that can be used to look up the
        url using ``url_for(endpoint)`` in the Flask routing
        system. In the simplest examples it is the name of the view
        function, but it can be anything really.
        """
        return self.name

    def show(self):
        """
        Show the window. 

        If the window is already visible, nothing is done.
        """
        print('show')
        pass

    def present(self):
        """
        Bring to the user's attention
        
        Implies :meth:`show`. If the window is already visible, this 
        method will deiconify / bring it to the foreground as necessary.
        """
        self.show()

    def hide(self):
        """
        Hide window temporarily.
        
        Use :meth:`show` to show the window again.
        """
        print('hide')
        pass

    def destroy(self):
        """
        Hide window and release all resources.

        After the window is destroyed, it is no longer possible to
        :meth:`show` it.
        """
        print('destroy')
        pass

    def dispatch_request(self):
        return flask.render_template(self.name + '.html')        

    def add_url_rule_to(self, app):
        app.add_url_rule(self.url, self.endpoint, self.dispatch_request)



class WindowFlaskSocket(WindowFlask):
    """
    Flask + Websocket Window
    """

    @property
    def url_socket(self):
        return self.url + 'ws'
        
    @property
    def endpoint_socket(self):
        """
        Return the Endpoint

        An endpoint is a name (string) that can be used to look up the
        url using ``url_for(endpoint)`` in the Flask routing
        system. In the simplest examples it is the name of the view
        function, but it can be anything really.
        """
        return self.name + '_ws'

    def socket(self, ws):
        while True:
            print 'socket loop'
            message = ws.receive()
            if message is None:
                print "got none"
                continue
            print 'msg =', message
            ws.send(message)

    def dispatch_socket(self):
        req = flask.request
        print 'dispatch socket', req
        if req.environ.get('wsgi.websocket'):
            ws = req.environ['wsgi.websocket']
            self.socket(ws)
        else:
            flask.abort(400, 'Expected WebSocket request.')

    def add_url_rule_to(self, app):
        super(WindowFlaskSocket, self).add_url_rule_to(app)
        app.add_url_rule(self.url_socket, self.endpoint_socket, self.dispatch_socket)



class ModalDialogFlask(ModalDialogABC):
    
    pass
