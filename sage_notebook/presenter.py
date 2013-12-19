"""
The Presenter (Controller)

Here is where it all comes together, the presenter ties together the
data model with the gui to create an application. It neither knows
about data nor about the gui, it just ties the two together.
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




class Presenter(object):

    def __init__(self, view_class, model_class, main_loop_class):
        self.main_loop = main_loop_class()
        self.view = view_class(self)
        self.model = model_class(self)
        self.main_loop.add_rpc_clients(self.model.get_rpc_clients())
        self.show_notebook_window()

        #if self.model.config.sage_root is None:
        #    self.show_setup_assistant(None, None, self.setup_assistant_first_run_finished)
        #else:
        #    self.show_notebook_window()
 
    def save_geometry(self):
        geometry = self.model.config.window_geometry
        geometry.update(self.view.get_geometry())
        self.model.config.window_geometry = geometry

    def get_saved_geometry(self, name):
        return self.model.config.window_geometry.get(name, {})

    def terminate(self):
        """
        Quit the program
        """
        self.save_geometry()
        self.view.terminate()
        self.model.terminate()

    ###################################################################
    # The main Notebook window

    def show_notebook_window(self):
        return self.view.show_notebook_window()

    def hide_notebook_window(self):
        self.view.hide_notebook_window()
        if self.view.current_window is None:
            self.terminate()

    ###################################################################
    # The about window

    def show_about_window(self):
        self.view.show_about_window()

    def hide_about_window(self):
        self.view.hide_about_window()
        if self.view.current_window is None:
            self.terminate()

    ###################################################################
    # Common for all modal dialogs

    def destroy_modal_dialog(self):
        self.view.destroy_modal_dialog()
        if self.view.current_window is None:
            self.terminate() 

    ###################################################################
    # Misc. notification dialog (modal)

    def show_notification(self, parent, text):
        self.view.new_notification_dialog(parent, text).show()

    ###################################################################
    # Error dialog (modal)

    def show_error(self, parent, title, text):
        self.view.new_error_dialog(parent, title, text).show()

    ###################################################################
    # Setup assistant (modal)

    def sage_installation(self, sage_root):
        """
        Return data about the Sage installation at ``sage_root``
    
        INPUT:

        - ``sage_root`` -- a directory name or ``None`` (default). The 
          path will be searched if not specified.
        """
        return self.model.sage_installation(sage_root)

    def show_setup_assistant(self, parent, sage_root, callback):
        """
        Assistant to figure out SAGE_ROOT
        
        INPUT:

        - ``sage_root`` -- string or ``None``. The initial value for 
          ``SAGE_ROOT``. If ``None``: Will be figured out from 
          calling ``sage`` in the ``$PATH``.
    
        - ``callback`` -- function / method. Will be called back with 
          the new :class:`sageui.model.sage_installation.SageInstallation`
        """
        self.view.new_setup_assistant(parent, sage_root, callback).show()

    def setup_assistant_first_run_finished(self, sage_install):
        """
        The callback for the first run
        """
        self.model.config.sage_root = sage_install.sage_root
        self.model.config.sage_version = sage_install.version
        if not self.view.have_open_window():
            self.show_default_window()


        
