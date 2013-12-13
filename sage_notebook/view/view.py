"""
Abstract Base Class of Views

Holds a number of persistent windows/dialogs as well as modal
dialogs. They are treated slighty differently:

* An ordinary window is only constructed once when it is 
  required. When the user closes it, it is only hidden and ready
  to be shown again as needed.

* Modal dialogs are continuously re-constructed. There can only 
  be one modal dialog at any one time. When the user closes it,
  it must call :meth:`View.destroy_modal_dialog`. Modal dialogs 
  have their parent window as argument so they can display 
  in front of it.
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




class ViewABC(object):

    def __init__(self, presenter):
        self.presenter = presenter
        self._current_window = None
        self._current_dialog = None
        self._open_windows = set()
        self.window_geometry = dict()

    def get_geometry(self):
        """
        Return the width x height of the windows
        """
        geometry = dict()
        for window in self._open_windows:
            geometry[window.name()] = window.get_geometry()
        return geometry

    def restore_geometry(self, geometry):
        for window in self._open_windows:
            try:
                window_geometry = geometry[window.name()]
            except KeyError:
                continue
            window.restore_geometry(window_geometry)
        
    @property
    def current_window(self):
        return self._current_window

    @property
    def current_dialog(self):
        return self._current_dialog

    @property
    def resource_dir(self):
        raise NotImplemented

    def terminate(self):
        raise NotImplemented

        
    ###################################################################
    # The main Notebook window

    @property
    def notebook_window(self):
        raise NotImplementedError
        
    def show_notebook_window(self):
        nb = self.notebook_window
        self._open_windows.add(nb)
        self._current_window = nb
        nb.present()

    def hide_notebook_window(self):
        nb = self.notebook_window
        nb.hide()
        self._open_windows.remove(nb)
