"""
Gtk-Based Main Loop

This is the implementation of :mod:`main_loop` for Gtk3.
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


from gi.repository import GLib, GObject, Gtk

from .main_loop import MainLoopABC






class MainLoopGtk(MainLoopABC):
    
    def __init__(self):
        super(MainLoopGtk, self).__init__()
        self.context = GObject.main_context_default()
        self.source = None

    def debug_shell_gtk(self, app):
        from IPython.lib.inputhook import enable_gtk3
        enable_gtk3()
        from IPython.frontend.terminal.ipapp import TerminalIPythonApp
        ip = TerminalIPythonApp.instance()
        ip.initialize(argv=[])
        ip.shell.enable_gui('gtk3')
        ip.shell.user_global_ns['app'] = app
        def ipy_import(module_name, identifier):
            module = importlib.import_module(module_name)
            ip.shell.user_global_ns[identifier] = getattr(module, identifier) 
        #ipy_import('sage_notebook.model.git_interface', 'GitInterface')
        ip.start()

    def run(self, debug=None):
        """
        Run the main loop.
        """
        GObject.timeout_add(50, self.select_setup)
        #self.select_setup()

        #GObject.timeout_add(500, callback)
        #loop = GLib.MainLoop()
        #loop.run()
        #return

        if debug is not None:
            self.debug_shell_gtk(debug)
        else:
            from gi.repository import Gtk
            # workaround for https://bugzilla.gnome.org/show_bug.cgi?id=622084
            import signal
            signal.signal(signal.SIGINT, signal.SIG_DFL)
            # end workaround
            logger.debug('Entering main loop')
            #main_loop = GLib.MainLoop()
            #main_loop.run()
            Gtk.main()

    def quit(self):
        if self.source is not None:
            self.source.destroy()
        Gtk.main_quit()
    


    def select_setup_new(self):
        """
        The newer implementation using GLib.Source.add_unix_fd()
        
        .. TODO::
        
            Too cutting edge right now, unfortunately. Implementation
            is not complete.
        """
        #self.source.remove()
        if self.source is not None:
            self.source.destroy()
        self.source = source = GLib.Source()

        rlist, wlist, xlist = self.select_args()
        print('select_setup', rlist, wlist, xlist)
        fds = set(rlist + wlist + xlist)

        # should use GLib.Source.add_unix_fd, but thats too cutting edge right now
        assert len(fds) == 1
        fd = next(iter(fds))

        condition = GLib.IOCondition(0)
        if fd in rlist:
            condition |= GLib.IOCondition.IN
        if fd in wlist:
            condition |= GLib.IOCondition.OUT
        if fd in xlist:
            condition |= GLib.IOCondition.ERR
        if condition.real != 0:
            source.add_unix_fd(fd, condition)

        source.set_callback(self.glib_select_callback, fd)
        #source.attach(self.context)


    
    def select_setup_old(self):
        """
        The older implementation using GLib.Source.add_poll()
        """
        rlist, wlist, xlist = self.select_args()
        fds = set(rlist + wlist + xlist)
        assert len(fds) == 1
        fd = next(iter(fds))

        condition = GLib.IOCondition(0)
        if fd in rlist:
            condition |= GLib.IOCondition.IN
        if fd in wlist:
            condition |= GLib.IOCondition.OUT
        if fd in xlist:
            condition |= GLib.IOCondition.ERR
        source = GLib.unix_fd_source_new(fd, condition)
        source.set_callback(self.glib_select_callback_old, (fd, rlist, wlist, xlist))
        source.attach(self.context)
        self.source = source

    select_setup = select_setup_old
                
    def glib_select_callback_old(self, args):
        fd, rlist, wlist, xlist = args
        import select
        rlist, wlist, xlist = select.select(rlist, wlist, xlist, 0)
        if rlist == wlist == xlist == []:
            pass
        else:
            self.select_handler(rlist, wlist, xlist)
        self.select_setup()
        return False


