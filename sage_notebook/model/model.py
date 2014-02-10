"""
The Data Model and Backend
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


from .config import Config
from .compute_service import ComputeService

from .worksheet import Cell, Worksheet


class Model:
    
    def __init__(self, presenter):
        self.presenter = presenter
        c = Config()
        self.config = c
        self.compute = ComputeService(presenter)
        self.worksheet = None

    def get_rpc_clients(self):
        return [self.compute.rpc_client]

    def terminate(self):
        # save
        pass

    def get_sage_installation(self, sage_root):
        """
        Return data about the Sage installation at ``sage_root``
    
        INPUT:

        - ``sage_root`` -- a directory name or ``None`` (default). The 
          path will be searched if not specified.
        """
        from .sage_installation import SageInstallation
        return SageInstallation(sage_root)

    # Worksheet data model

    def get_cell(self, cell_id):
        return self.worksheet.get_cell(cell_id)

    def insert_cell_at(self, pos, template_cell=None):
        """
        Insert and return the new cell

        INPUT:

        - ``pos`` -- integer. The position in the worksheet.
        
        - ``template_cell`` -- a cell or ``None``. If specified, it
          will be copied for the new cell.

        OUTPUT:

        The newly created cell (which is now at position ``pos``) is
        returned.
        """
        ws = self.worksheet
        if template_cell is None:
            cell = Cell()
        else:
            cell = template_cell.copy()
        ws.insert(pos, cell)
        return cell
        
    def delete_cell(self, cell_id):
        """
        Delete the cell and return the cell that takes its place.
        """
        cell = self.get_cell(cell_id)
        ws = self.worksheet
        pos = ws.index(cell)
        ws.delete(cell)
        if pos == ws.n_cells():
            # deleted the last cell
            pos = ws.n_cells() - 1
        return ws[pos]
        
    def load_worksheet(self):
        self.worksheet = ws = Worksheet.create_default()
        return ws

    # Evaluation of cells

    def eval_cell_init(self, cell_id, input_string):
        """
        Prepare the cell for evaluation
        """
        cell = self.get_cell(cell_id)
        cell.input = input_string
        cell.index = None
        self.compute.eval(cell)
        return cell

    def eval_cell_update(self, cell):
        """
        We got partial output for ``cell``.
        """
        pass

    def eval_cell_finished(self, cell):
        """
        Evaluation finished
        """
        pass

    # autocompletion

    def code_complete_init(self, input_string, cursor_pos, cell_id, label):
        """
        Initiate auto-completion.
        """
        from .code_completion import Request
        request = Request(input_string, cursor_pos, cell_id, label)
        self.compute.code_complete(request)

    def code_complete_finished(self, cell, completion):
        """
        Callback with suggestions for auto-completion.
        """
        pass
