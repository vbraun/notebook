"""
Code completion result

EXAMPLES::

    sage: from sage_notebook.model.code_completion import Request
    sage: request = Request('x = pi.', int(4+3))
    sage: request.input
    'x = pi.'
    sage: request.pos
    7
    sage: result = request.complete('pi.', ['N', 'Order', 'abs'])
    sage: result.request is request
    True
    sage: result.base
    'pi.n'
    sage: result.completions
    ('N', 'Order', 'abs')
"""


class Request(object):

    def __init__(self, input_string, cursor_pos, cell_id=None, label=None):
        self._string = input_string
        self._pos = cursor_pos
        self._cell_id = cell_id
        self._label = label

    @property
    def cell_id(self):
        return self._cell_id

    @property
    def label(self):
        return self._label

    @property
    def string(self):
        return self._string

    @property
    def pos(self):
        return self._pos

    def complete(self, base, completion):
        return Completion(self, base, completion)



class Completion(object):

    def __init__(self, request, base, completion):
        self._request = request
        self._base = base
        self._completion = tuple(completion)

    @property
    def request(self):
        return self._request

    @property
    def base(self):
        return self._base

    @property
    def completions(self):
        return self._completion
