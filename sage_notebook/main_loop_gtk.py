
import logging
logger = logging.getLogger('GUI')


from gi.repository import GLib, GObject

from .main_loop import MainLoopABC




counter = 0

def callback(*args):
    global counter
    counter += 1
    print('callback called {0}'.format(counter))
    if counter > 10:
        print('last call')
        return False
    return True


def cb(*args, **kwds):
    print('callback!! {0} {1}'.format(args, kwds))


class MainLoopGtk(MainLoopABC):
    
    def __init__(self):
        self._rpc_clients = []

    def add_rpc_clients(self, clients):
        self._rpc_clients.extend(clients)
    
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
        client = self._rpc_clients[0]
        rlist, wlist, xlist = client.select_args()
        fds = set(rlist + wlist + xlist)
        context = GObject.main_context_default()
        for fd in fds:
            condition = GLib.IOCondition(0)
            if fd in rlist:
                condition |= GLib.IOCondition.IN
            if fd in wlist:
                condition |= GLib.IOCondition.OUT
            if fd in xlist:
                condition |= GLib.IOCondition.ERR
            if condition.real != 0:
                source = GLib.unix_fd_source_new(fd, condition)
                source.set_callback(self.loop, fd)
                source.attach(context)

        GObject.timeout_add(500, callback)
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
            Gtk.main()

    def quit(self):
        pass
    
    def loop(self, fd):
        """
        Main loop idle handler.
        
        Bidirectional RPC is 100% asynchronous, so ideally the
        different endpoints should run in separate processes or
        threads. However, on the Sage command line we have only a
        single thread. Hence we fake the asynchronous operation by
        hooking in the idle loop (when Sage is sitting at the input
        prompt).
        """
        idle = self._rpc_clients
        from sage.rpc.core.transport import TransportError
        rlist = []
        wlist = []
        xlist = []
        for obj in list(idle):
            try:
                rl, wl, xl = obj.select_args()
            except TransportError:
                idle.discard(obj)
                continue
            rlist += rl
            wlist += wl
            xlist += xl
        import select
        rlist, wlist, xlist = select.select(rlist, wlist, xlist, 0)
        if rlist == [] and wlist == [] and xlist == []:
            return   # timeout
        for obj in list(idle):
            try:
                obj.select_handle(rlist, wlist, xlist)
            except TransportError:
                idle.discard(obj)
                obj.close()

