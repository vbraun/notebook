"""
The compute service
"""
import os
import logging
logger = logging.getLogger('GUI')

from sage.rpc.core.transport import TransportListen
from sage.rpc.core.monitor import MonitorClient



class ComputeServiceClient(MonitorClient):
    
    def __init__(self, service, *args, **kwds):
        super().__init__(*args, **kwds)
        self.service = service

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

    def _impl_sage_eval_result(self, cpu_time, wall_time, label):
        """
        RPC callback when evaluation is finished
        """
        self.service._impl_sage_eval_result(cpu_time, wall_time, label)

    def _impl_sage_eval_crash(self, label):
        """
        RPC callback when the compute server crashed
        """
        self.service._impl_sage_eval_crash(self, label)



class Queue(object):

    def __init__(self):
        self._current_label = None
        self._cells = dict()
        self._next = list()

    def __getitem__(self, label):
        return self._cells[label]

    def is_empty(self):
        return self._current_label is None

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
        assert len(self._cells) == len(self._next)

    def pop(self):
        old_label, old_cell = self.current_label, self.current_cell
        if old_label is not None:
            del self._cells[old_label]
            self._next.remove(old_label)
        if len(self._next) == 0:
            self._current_label = None
        else:
            self._current_label = self._next[0]
            self._next = self._next[1:]
        assert len(self._cells) == len(self._next)
        return (old_label, old_cell)
        




class ComputeService(object):

    def __init__(self, presenter):
        self.presenter = presenter
        self.queue = Queue()
        self.start_client()
        from sage.rpc.core.logging_origin import logger
        logger.setLevel(logging.DEBUG)

    def start_client(self):
        interface = 'localhost'
        cookie = self._random_cookie()
        uri = 'tcp://localhost:0'
        transport = TransportListen(uri)
        self._monitor = monitor = self._spawn_monitor(
            cookie, transport.port(), interface)
        transport.accept()
        self._client = ComputeServiceClient(self, transport, cookie)
        #client.wait_for_initialization()
        #self._add_idle(client)        
        #import time
        #for i in range(200):
        #    self._inputhook()
        #    time.sleep(0.01)
        
    def restart_client(self):
        raise NotImplementedError

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

    def eval(self, cell):
        """
        Start evaluating a notebook cell.
        """
        ready = self.queue.is_empty()
        cell.clear_output()
        self.queue.push(cell.id, cell)
        if ready:
            self._client.sage_eval(cell.input, cell.id)
    
    def _impl_sage_eval_stdin(self, cell_id):
        """
        RPC callback when evaluation requests stdin
        """
        cell = self.queue.current_cell
        assert cell.id == cell_id
        logger.error('stdin')   # not implemented
        
    def _impl_sage_eval_stdout(self, stdout, cell_id):
        """
        RPC callback when evaluation produces stdout
        """
        cell = self.queue.current_cell
        assert cell.id == cell_id
        logger.debug('stdout %s', stdout.strip())
        cell.accumulate_stdout(stdout)
        self.presenter.on_evaluate_cell_updated(cell_id, cell)

    def _impl_sage_eval_stderr(self, stderr, cell_id):
        """
        RPC callback when evaluation produces stderr
        """
        cell = self.queue.current_cell
        assert cell.id == cell_id
        logger.debug('stderr %s', stderr.strip())
        cell.accumulate_stdout(stdout)
        self.presenter.on_evaluate_cell_updated(cell_id, cell)

    def _impl_sage_eval_result(self, cpu_time, wall_time, cell_id):
        """
        RPC callback when evaluation finished successfully
        """
        cell = self.queue.current_cell
        assert cell.id == cell_id
        self.queue.pop()
        next_cell = self.queue.current_cell
        if next_cell is not None:
            self.client.sage_eval(next_cell.input, cell.id)
        self.presenter.on_evaluate_cell_finished(cell_id, cell)

    def _impl_sage_eval_crash(self, cell_id):
        """
        RPC callback when the compute server crashed
        """
        cell = self.queue.current_cell
        assert cell.id == cell_id
        self.queue.pop()
        self.presenter.on_evaluate_cell_finished(cell_id, cell)
        logger.warning('crashed')
        self.restart_client()
        next_cell = self.queue.current_cell
        if next_cell is not None:
            self.client.sage_eval(next_cell.input, cell.id)
        

