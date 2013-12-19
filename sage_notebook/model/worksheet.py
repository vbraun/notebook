"""
Model for the Worksheet
"""




class Cell(object):
    def __init__(self):
        self._input = None
        self.clear_output()

    def set_input(self, input_string):
        self._input = input_string

    def clear_output(self):
        self._stdout = None
        self._stderr = None
        
    def accumulate_stdout(self, stdout):
        self._stdout += stdout

    def accumulate_stderr(self, stderr):
        self._stderr += stderr

    @property
    def stdout(self):
        return self._stdout

    @property
    def stderr(self):
        return self._stderr



class Worksheet(object):

    def __init__(self):
        pass
        

