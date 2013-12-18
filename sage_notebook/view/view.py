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

from .window import WindowABC


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

    def _add_window(self, window):
        assert isinstance(window, WindowABC)
        self._open_windows.add(window)
        self._current_window = window

    def _show_window(self, window):
        """
        Show the window.

        This adds the window to the set of open windows and puts it
        into the foreground.

        INPUT:

        - ``window`` -- an instance of
          :class:`~sage_notebook.view.window.WindowABC`.
        """
        assert isinstance(window, WindowABC)
        self._open_windows.add(window)
        self._current_window = window
        window.present()

    def _hide_window(self, window):
        """
        Hide the window.

        INPUT:

        - ``window`` -- an instance of
          :class:`~sage_notebook.view.window.WindowABC`.
        """
        assert isinstance(window, WindowABC)
        window.hide()
        self._open_windows.remove(window)
        try:
            self._current_window = next(iter(self._open_windows))
            self._current_window.present()
        except StopIteration:
            self._current_window = None
        
    @property
    def current_window(self):
        return self._current_window

    @property
    def current_dialog(self):
        return self._current_dialog


    ###################################################################
    # To be implemented in derived classes

    @property
    def resource_dir(self):
        raise NotImplemented

    def terminate(self):
        pass

        
    ###################################################################
    # The About Dialog (which need not be modal, so we call it "About Window")

    @property
    def about_window(self):
        raise NotImplementedError
        
    def show_about_window(self):
        about = self.about_window
        self._show_window(about)

    def hide_about_window(self):
        about = self.about_window
        self._hide_window(about)

        
    ###################################################################
    # The main Notebook window

    @property
    def notebook_window(self):
        raise NotImplementedError
        
    def show_notebook_window(self):
        nb = self.notebook_window
        self._show_window(nb)

    def hide_notebook_window(self):
        nb = self.notebook_window
        self._hide_window(nb)
        
    ###################################################################
    # The Preferences window

    @property
    def preferences_window(self):
        raise NotImplementedError

    def show_preferences_window(self, config):
        prefs = self.preference_window
        prefs.update_from(config)
        self._show_window(prefs)

    def hide_preferences_window(self):
        prefs = self.preferences_window
        self._hide_window(prefs)


    ###################################################################
    # Modal dialogs

    def new_notification_dialog(self, parent, text):
        raise NotImplementedError

    def new_error_dialog(self, parent, title, text):
        raise NotImplementedError
        
    def new_setup_assistant(self, parent, sage_root, callback):
        raise NotImplementedError

    def destroy_modal_dialog(self):
        """
        Destroy the currently-shown modal dialog
        """
        assert self._current_dialog is not None
        self._current_dialog.destroy()
        self._current_dialog = None

