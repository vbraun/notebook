
from sage.rpc.core.transport import TransportError



class MainLoopABC(object):

    def __init__(self):
        self._rpc_clients = []

    def add_rpc_clients(self, clients):
        self._rpc_clients.extend(clients)

    def run(self, debug=None):
        """
        Run the main loop.
        """
        raise NotImplementedError

    def quit(self):
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
