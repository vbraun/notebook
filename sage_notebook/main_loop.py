"""
Main Loop Abstract Base Class

Unlike the Sage command line, GUI programs generally are organized
around a main loop. You tell the gui what to display, and then give up
control to the main loop. The main loop will then handle interaction
with the user, and call back into your own code to process input. For
example, you press a button and in response a function
``View.on_button_press`` is called. 

This means that we cannot wait for output from the compute server
ourselves, we have to integrate with the main loop to make it listen
for updates. The notebook can support any main loop implementation
that allows to ``select()`` for additional sockets, which is a rather
basic requirement for main loops. Implementations are
:mod:`main_loop_gtk` and :mod:`main_loop_http`.
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



from sage.rpc.core.transport import TransportError



class MainLoopABC(object):

    def __init__(self):
        self._rpc_clients = []

    def add_rpc_clients(self, clients):
        self._rpc_clients.extend(clients)

    def run(self, debug=None):
        """
        Run the main loop.

        This method shall relinquish control to the implementation's
        main loop and not exit until the program quits.

        INPUT:

        - ``debug`` -- anything. Generally will be ``None``,
          indicating no debugging. Otherwise, run in an IPython shell
          and make the ``debug`` value available interactively for
          ease of debugging.
        """
        raise NotImplementedError

    def quit(self):
        """
        Force the main loop to quit.
        
        This method is called when the user requests the program to
        finish, e.g., by pressing a "Quit" button.
        """
        raise NotImplementedError

    def select_setup():
        """
        Select for :meth:`select_args` and make sure :meth:`select_handle` is called.
        """
        raise NotImplementedError

    def select_args(self):
        idle = self._rpc_clients
        rlist = []
        wlist = []
        xlist = []
        for obj in list(idle):
            try:
                rl, wl, xl = obj.select_args()
            except TransportError:
                idle.remove(obj)
                print('select_args TransportError', obj)
                continue
            rlist += rl
            wlist += wl
            xlist += xl
        return rlist, wlist, xlist

    def select_handler(self, rlist, wlist, xlist):
        if rlist == [] and wlist == [] and xlist == []:
            return # timeout?
        idle = self._rpc_clients
        import select
        #rlist, wlist, xlist = select.select(rlist, wlist, xlist, 0)
        for obj in list(idle):
            try:
                obj.select_handle(rlist, wlist, xlist)
            except TransportError:
                idle.remove(obj)
                print('select_handler TransportError', obj)
                obj.close()
