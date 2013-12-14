"""
Windows in Gtk
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



from .window import WindowABC, ModalDialogABC



class WindowGtk(WindowABC):

    def __init__(self, name, presenter, builder):
        super().__init__(name, presenter)
        self.window = builder.get_object(name)

    def save_geometry(self):
        x, y = self.window.get_size()
        geometry = dict()
        geometry['x'] = x
        geometry['y'] = y
        return geometry
        
    def restore_geometry(self, geometry_dict={}):
        x = geometry_dict.get('x', 1024)
        y = geometry_dict.get('y',  600)
        self.window.resize(x, y)

    def show(self):
        """
        Show window. 

        If the window is already visible, nothing is done.
        """
        self.window.show()

    def present(self):
        """
        Bring to the user's attention
        
        Implies :meth:`show`. If the window is already visible, this 
        method will deiconify / bring it to the foreground as necessary.
        """
        self.window.present()

    def hide(self):
        self.window.hide()

    def destroy(self):
        return self.window.destroy()




class ModalDialogGtk(ModalDialogABC):
    

    def __init__(self, parent_window, builder, name):
        """
        INPUT:
        
         - ``parent_window`` -- A :class:`Window` instance. The dialog
          is displayed on top of its parent.

        - ``object_id`` -- anything that identifies the window
        """
        super().__init__(builder, name)
        self.window.set_transient_for(parent_window.window)

