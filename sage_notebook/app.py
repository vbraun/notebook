"""
The Application

The application class is basically just a container to hold
Model/View/Presenter. There is only one instance. On the debug REPL
(if you start with the ``--debug`` option) it is assigned to the
variable ``app`` in the global namespace.
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


#from sage_notebook.presenter import Presenter
#from sage_notebook.view.view import View
#from sage_notebook.model.model import Model


class Application(object):

    def __init__(self):
        #self.presenter = Presenter(View, Model)
        #self.view = self.presenter.view
        #self.model = self.presenter.model
        pass



