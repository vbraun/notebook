"""
The compute service
"""
import os
import logging

from sage.rpc.core.transport import TransportListen
from sage.rpc.core.monitor import MonitorClient



class ComputeServiceClient(MonitorClient):
    
    def __init__(self, service, *args, **kwds):
        super().__init__(*args, **kwds)
        self.service = service

    def _impl_sage_eval_result(self, cpu_time, wall_time, label):
        """
        RPC callback when evaluation is finished
        """
        self.service._impl_sage_eval_result(cpu_time, wall_time, label)

    def _impl_sage_eval_stdin(self, label):
        """
        RPC callback when evaluation requests stdin
        """
        self.service._impl_sage_eval_stdin(label)

    def _impl_sage_eval_stdout(self, stdout, label):
        """
        RPC callback when evaluation produces stdout
        """
        self.service._impl_sage_eval_stdout(stdout, label)

    def _impl_sage_eval_stderr(self, stderr, label):
        """
        RPC callback when evaluation produces stderr
        """
        self.service._impl_sage_eval_stderr(stderr, label)

    def _impl_sage_eval_crash(self, label):
        """
        RPC callback when the compute server crashed
        """
        self.service._impl_sage_eval_crash(self)



class Queue(object):

    def __init__(self):
        self._current_label = None
        self._cells = dict()
        self._next = list()

    def __getitem__(self, label):
        return self._cells[label]

    @property
    def current_label(self):
        return self._current_label

    @property
    def current_cell(self):
        try:
            return self._cells[self._current_label]
        except KeyError:
            return None

    def push(self, label, cell):
        assert label not in self._cells
        self._cells[label] = cell
        self._next.append(label)
        if self._current_label is None:
            self._current_label = label

    def pop(self):
        old_label, old_cell = self.current_label, self.current_cell
        if old_label is not None:
            del self._cells[label]
        if len(self._next) == 0:
            self._current_label = None
        else:
            self._current_label = self._next[0]
            self._next = self._next[1:]
        return (old_label, old_cell)
        




class ComputeService(object):

    def __init__(self, model):
        self.model = model
        self.queue = Queue()
        self.start()
        from sage.rpc.core.logging_origin import logger
        logger.setLevel(logging.DEBUG)


    def start(self):
        interface = 'localhost'
        cookie = self._random_cookie()
        uri = 'tcp://localhost:0'
        transport = TransportListen(uri)
        self._monitor = monitor = self._spawn_monitor(
            cookie, transport.port(), interface)
        transport.accept()
        self._client = client = ComputeServiceClient(self, transport, cookie)
        #client.wait_for_initialization()
        #self._add_idle(client)        
        #import time
        #for i in range(200):
        #    self._inputhook()
        #    time.sleep(0.01)
        
    @property
    def rpc_client(self):
        return self._client

    def _random_cookie(self, length=30):
        """
        Return a new random string.

        OUTPUT:

        A random string.

        EXAMPLES::

            sage: sage_remote.random_cookie()    # random output
            'FayJpeGUjD7wg0tSqQGEpzupkWX1km'
        """
        import string
        import random
        return ''.join(random.choice(string.ascii_letters + string.digits) 
                       for x in range(length))

    def _spawn_monitor(self, cookie, port, interface):
        """
        Create a server in a new process.

        See :meth:`start_server` for a description of the input.

        OUTPUT:

        The subprocess running the server.
        """
        env = dict(os.environ)
        env['COOKIE'] = cookie
        cmd = ['sage', '-python', '-c',
               'from sage.rpc.core.monitor import start_monitor; '
               'start_monitor({0}, "{1}")'.format(port, interface)]
        import sys
        from subprocess import Popen
        return Popen(cmd, env=env, stdout=sys.stdout, stderr=sys.stderr)

    def select_args(self):
        return self._client.select_args()

    def select_handle(self, rlist ,wlist, xlist):
        return self._client.select_handle(rlist, wlist, xlist)

    def eval(self, cell):
        """
        Start evaluating a notebook cell.
        """

    def _impl_sage_eval_result(self, cpu_time, wall_time, label):
        """
        RPC callback when evaluation is finished
        """
        service._impl_sage_eval_result(cpu_time, wall_time, label)

    def _impl_sage_eval_stdin(self, label):
        """
        RPC callback when evaluation requests stdin
        """
        self.log.debug('stdin')
        print('Input requested')

    def _impl_sage_eval_stdout(self, stdout, label):
        """
        RPC callback when evaluation produces stdout
        """
        self.log.debug('stdout %s', stdout.strip())
        print('STDOUT ' + stdout)

    def _impl_sage_eval_stderr(self, stderr, label):
        """
        RPC callback when evaluation produces stderr
        """
        self.log.debug('stderr %s', stderr.strip())
        print('STDERR ' + stderr)

    def _impl_sage_eval_crash(self):
        """
        RPC callback when the compute server crashed
        """
        print('Compute server crashed.')

