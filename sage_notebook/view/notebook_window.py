"""
Abstract Base Class of the Notebook Window
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


from .window import WindowABC


class NotebookWindowABC(WindowABC):

    def on_notebook_evaluate_cell(self, cell_id, input_string):
        """
        Callback to use for cell evaluation request (like Ctrl-Enter)
        """
        self.presenter.evaluate_cell_init(cell_id, input_string)

    def cell_busy(self, cell):
        """
        Update the view of the cell to display a running computation.
        """
        raise NotImplemented

    def cell_update(self, cell):
        """
        Update the view of the cell to display a partial result.
        """
        raise NotImplemented
        
    def cell_finished(self, cell):
        """
        Update the view of the cell to display the final result
        """
        raise NotImplemented
        
