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


from sage_notebook.presenter import Presenter
from sage_notebook.model.model import Model




class Application(object):

    def __init__(self, view_backend):
        if view_backend == 'gtk':
            from sage_notebook.view.view_gtk import ViewGtk as View
            from sage_notebook.main_loop_gtk import MainLoopGtk as MainLoop
        elif view_backend == 'http':
            from sage_notebook.view.view_http import ViewHttp as View
        elif view_backend == 'text':
            from sage_notebook.view.view_text import ViewText as View
        self.presenter = Presenter(View, Model, MainLoop)
        self.view = self.presenter.view
        self.model = self.presenter.model
        self.main_loop = self.presenter.main_loop

    def run(self, debug):
        self.main_loop.run(debug)



