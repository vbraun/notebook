"""
Query data about an existing Sage install
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


import os
import subprocess
from sage_notebook.misc.cached_property import cached_property


class SageInstallation(object):
    
    def __init__(self, sage_root=None):
        if sage_root is None:
            sage_root = self._sage_from_path()
        self.sage_root = sage_root
        
    def _sage_from_path(self):
        try:
            sage_root = subprocess.check_output([
                'sage',
                '-python', '-c',
                'import os; print os.environ["SAGE_ROOT"]'
            ]).decode('utf-8')
        except subprocess.CalledProcessError as err:
            return None
        return sage_root.strip()

    @cached_property
    def is_usable(self):
        if self.sage_root is None:
            return False
        if not os.path.isfile(os.path.join(self.sage_root, 'sage')):
            return False
        return True
        
    @cached_property
    def has_git(self):
        assert self.is_usable
        return os.path.isdir(os.path.join(self.sage_root, '.git'))

    @cached_property
    def version(self):
        assert self.is_usable
        try:
            version = subprocess.check_output([
                os.path.join(self.sage_root, 'sage'), '--version'
            ]).decode('utf-8')
        except CalledProcessError as err:
            return str(err)
        return version

        
