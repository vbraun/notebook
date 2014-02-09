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

import logging
logger = logging.getLogger('GUI')


class Presenter(object):

    def __init__(self, view_class, model_class, main_loop_class):
        self.main_loop = main_loop_class()
        self.view = view_class(self)
        self.model = model_class(self)
        self.main_loop.add_view(self.view)
        self.main_loop.add_rpc_clients(self.model.get_rpc_clients())
        if self.model.config.sage_root is None:
            callback = self.on_setup_assistant_first_run_finished
            self.show_setup_assistant(None, None, callback)
        else:
            self.show_notebook_window_worksheet()
 
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
        self.main_loop.quit()

    ###################################################################
    # The main Notebook window

    def evaluate_cell_init(self, cell_id, input_string):
        """
        Initiate evaluating a notebook cell
        """
        logger.info('evaluating cell %s', cell_id)
        cell = self.model.eval_cell_init(cell_id, input_string)
        self.view.notebook_window.cell_busy(cell)

    def on_evaluate_cell_updated(self, cell_id, cell):
        """
        Callback for changes in a notebook cell that is currently
        computing.
        
        Typically, this adds partial output. This may only be
        triggered after a preceeding :meth:`evaluate_cell_init`, and
        not after a subsequent :meth:`on_evaluate_cell_finish`.
        """
        logger.debug('updating cell %s', cell_id)
        self.model.eval_cell_update(cell)
        self.view.notebook_window.cell_update(cell)

    def on_evaluate_cell_finished(self, cell_id, cell):
        """
        Callback for changes in a notebook cell that just finished.

        This finishes the computation on the cell. This will only be
        triggered after a preceeding :meth:`on_evaluate_cell_init`.

        The cell need not have finished successfully, it might have
        had an error or even crashed the Sage process. However, it is
        guaranteed that every :meth:`evaluate_cell_init` is followed
        up with a :meth:`on_evaluate_cell_finished`.
        """
        logger.info('finished cell %s', cell_id)
        self.model.eval_cell_finished(cell)
        self.view.notebook_window.cell_finished(cell)

    def insert_cell_at(self, pos, template_cell=None):
        cell = self.model.insert_cell_at(pos, template_cell)
        self.view.notebook_window.set_worksheet(self.model.worksheet)
        self.view.notebook_window.cell_grab_focus(cell)

    def delete_cell(self, cell_id):
        cell = self.model.delete_cell(cell_id)
        self.view.notebook_window.set_worksheet(self.model.worksheet)
        self.view.notebook_window.cell_grab_focus(cell)

    def auto_complete(self, text, cursor, callback):
        """
        Call back with suggestions for auto-completion.
        """
        pass

    def show_notebook_window_worksheet(self):
        """
        Load & display a new worksheet.
        """
        # TODO: load different worksheets
        model = self.model.load_worksheet()
        view = self.show_notebook_window()
        view.set_worksheet(model)

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
        logger.debug('destroy_modal_dialog')
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

    def get_sage_installation(self, sage_root=None):
        """
        Return data about the Sage installation at ``sage_root``
    
        INPUT:

        - ``sage_root`` -- a directory name or ``None`` (default). The 
          path will be searched if not specified.
        """
        return self.model.get_sage_installation(sage_root)

    def set_sage_installation(self, sage_install):
        """
        Return data about the Sage installation at ``sage_root``
    
        INPUT:

        - ``sage_root`` -- a directory name or ``None`` (default). The 
          path will be searched if not specified.
        """
        self.model.config.sage_root = sage_install.sage_root
        self.model.config.sage_version = sage_install.version

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

    def on_setup_assistant_first_run_finished(self, sage_install):
        """
        The callback for the first run
        
        .. note::

            The assistant is responsible to call
            :meth:`destroy_modal_dialog` after the callback returns.
        """
        self.set_sage_installation(sage_install)
        self.show_notebook_window_worksheet()
        

        
