"""
Windows (Webpages) in Flask

This is the Flask implementation of :mod:`window`.
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


class WindowFlask(WindowABC):

    def show(self):
        """
        Show the window. 

        If the window is already visible, nothing is done.
        """
        print('show')
        pass

    def present(self):
        """
        Bring to the user's attention
        
        Implies :meth:`show`. If the window is already visible, this 
        method will deiconify / bring it to the foreground as necessary.
        """
        self.show()

    def hide(self):
        """
        Hide window temporarily.
        
        Use :meth:`show` to show the window again.
        """
        print('hide')
        pass

    def destroy(self):
        """
        Hide window and release all resources.

        After the window is destroyed, it is no longer possible to
        :meth:`show` it.
        """
        print('destroy')
        pass




class ModalDialogFlask(ModalDialogABC):
    
    pass
