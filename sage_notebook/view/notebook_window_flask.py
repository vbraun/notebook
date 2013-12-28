"""
The Notebook Window

This is the Flask implementation of :mod:`notebook_window`
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

from .window_flask import WindowFlaskSocket
from .notebook_window import NotebookWindowABC


class NotebookWindowFlask(NotebookWindowABC, WindowFlaskSocket):

    def __init__(self, presenter):
        WindowFlaskSocket.__init__(self, 'notebook', presenter)

    def on_receive(self, message):
        self.on_notebook_evaluate_cell('test_id', message)

    def set_output(self, cell):
        self.send(cell.as_plain_text())

    def cell_busy(self, cell):
        """
        Update the view of the cell to display a running computation.
        """
        self.send('busy')

    def cell_update(self, cell):
        """
        Update the view of the cell to display a partial result.
        """
        self.set_output(cell)
        
    def cell_finished(self, cell):
        """
        Update the view of the cell to display the final result
        """
        self.set_output(cell)
        self.send('finished')
