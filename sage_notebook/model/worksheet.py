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
        self._input = None
        self.clear_output()

    @property
    def id(self):
        return self._id
    
    def clear_output(self):
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



class Worksheet(object):

    def __init__(self):
        pass
        
    def get_cell(self, cell_id):
        pass
