"""
Model for the Worksheet
"""




class Cell(object):
    def __init__(self, cell_id=None):
        if cell_id is None:
            import uuid
            self._id = uuid.uuid4().hex
        else:
            self._id = cell_id
        self._index = None
        self._input = None
        self.clear_output()

    def __repr__(self):
        return 'Cell id {0}'.format(self.id)

    @property
    def id(self):
        return self._id
    
    @property
    def index(self):
        """
        Return the ``n`` in ``In[n]/Out[n]``
        
        OUTPUT:

        An integer or ``None``.
        """
        return self._index

    @index.setter
    def index(self, value):
        self._index = value
        
    def clear_output(self):
        self._index = None
        self._stdout = ''
        self._stderr = ''
        
    def accumulate_stdout(self, stdout):
        self._stdout += stdout

    def accumulate_stderr(self, stderr):
        self._stderr += stderr

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value):
        self._input = value

    @property
    def stdout(self):
        return self._stdout

    @property
    def stderr(self):
        return self._stderr

    def as_plain_text(self):
        result = self._stdout.rstrip()
        if len(self._stderr) > 0:
            result += self._stderr.rstrip()
        return result


class Worksheet(object):

    def __init__(self):
        self._cells_dict = dict()
        self._order = list()

    def __repr__(self):
        return 'Worksheet containing {0} cells'.format(self.n_cells())

    @classmethod
    def create_default(cls):
        ws = cls()
        c = Cell()
        c.input = '123'
        ws.append(c)
        c = Cell()
        c.input = '123^2'
        ws.append(c)
        c = Cell()
        c.input = 'def f(x):\n    return 1'
        ws.append(c)
        c = Cell()
        c.input = '# test'
        ws.append(c)
        return ws
        
    def insert(self, pos, cell):
        self._cells_dict[cell.id] = cell
        self._order.insert(pos, cell.id)

    def append(self, cell):
        self.insert(self.n_cells(), cell)

    def n_cells(self):
        return len(self._cells_dict)

    __len__ = n_cells

    def get_cell(self, cell_id):
        return self._cells_dict[cell_id]
        
    def get_indent(self, cell_id):
        return 0
    
        
    def __iter__(self):
        for cell_id in self._order:
            yield self._cells_dict[cell_id]
