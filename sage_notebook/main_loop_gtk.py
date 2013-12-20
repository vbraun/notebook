
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








class SocketSource(GLib.Source):
    def __init__(self):
        super().__init__(self)
        self.callback = None
        self.pollfds = []

    def my_set_callback(self, callback):
        self.callback = callback

    def prepare(self):
        print('prepare')
        return False

    def check(self):
        print('check')
        for pollfd in self.pollfds:
            if pollfd.revents:
                return True
        return False

    def dispatch(self, callback, args):
        print('dispatch', args)
        self.callback(args)
        return True

    def add_socket(self, rlist, wlist, xlist):
        fd = rlist[0]
        pollfd = GLib.PollFD(fd, GLib.IO_IN | GLib.IO_OUT)
        self.pollfds.append(pollfd)
        self.add_poll(pollfd)
        print(pollfd)

    def rm_socket(self, socket):
        fd = socket.fileno()
        for pollfd in self.pollfds:
            if pollfd.fd == fd:
                self.remove_poll(pollfd)
                self.pollfds.remove(pollfd)




        # for fd in set(rlist + wlist + xlist):
        #     condition = GLib.IOCondition(0)
        #     if fd in rlist:
        #         condition |= GLib.IOCondition.IN
        #     if fd in wlist:
        #         condition |= GLib.IOCondition.OUT
        #     if fd in xlist:
        #         condition |= GLib.IOCondition.ERR
        #     if condition.real != 0:
        #         pollfd = GLib.PollFD(fd, condition)
        #         source.add_poll(pollfd)
        #         source.set_callback(self.glib_select_callback, pollfd)
        # source.attach()






class MainLoopGtk(MainLoopABC):
    
    def __init__(self):
        super().__init__()
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
            main_loop = GLib.MainLoop()
            main_loop.run()

    def quit(self):
        pass
    
    


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



        # #if self.source is not None:
        # #    self.source.destroy()
        # source = SocketSource()
        # source.my_set_callback(self.glib_select_callback)
        
        # rlist, wlist, xlist = self.select_args()
        # print('select_setup_old', rlist, wlist, xlist)

        # import select
        # select.select(rlist, wlist, xlist)

        # for fd in set(rlist + wlist + xlist):
        #     source.add_socket(rlist, wlist, xlist)
        # self.source = source
        # source.attach(self.main_loop.get_context())




        # client = self._rpc_clients[0]
        # rlist, wlist, xlist = client.select_args()
        # fds = set(rlist + wlist + xlist)
        # context = GObject.main_context_default()
        # for fd in fds:
        #     condition = GLib.IOCondition(0)
        #     if fd in rlist:
        #         condition |= GLib.IOCondition.IN
        #     if fd in wlist:
        #         condition |= GLib.IOCondition.OUT
        #     if fd in xlist:
        #         condition |= GLib.IOCondition.ERR
        #     if condition.real != 0:
        #         source = GLib.unix_fd_source_new(fd, condition)
        #         source.set_callback(self.loop, fd)
        #         source.attach(context)


        # print('destroy')
        # self.source.destroy()
        # self.source = source = GLib.Source()

        # rlist, wlist, xlist = self.select_args()
        # print('select_setup', rlist, wlist, xlist)

        # for fd in set(rlist + wlist + xlist):
        #     condition = GLib.IOCondition(0)
        #     if fd in rlist:
        #         condition |= GLib.IOCondition.IN
        #     if fd in wlist:
        #         condition |= GLib.IOCondition.OUT
        #     if fd in xlist:
        #         condition |= GLib.IOCondition.ERR
        #     if condition.real != 0:
        #         pollfd = GLib.PollFD(fd, condition)
        #         source.add_poll(pollfd)
        #         source.set_callback(self.glib_select_callback, pollfd)
        # source.attach()
    

