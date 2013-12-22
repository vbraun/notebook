"""
Container for Configuration Data
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


import io
import os
import sys
import json
import logging


class Config(object):

    def __init__(self):
        self._load()

    def _save(self):
        data_json = json.JSONEncoder(indent=2).encode(self._data)
        if sys.version_info.major < 3:
            data_json = data_json.decode('utf-8')
        with io.open(self.settings_file, 'w', encoding='utf-8') as f:
            f.write(data_json)

    def _load(self):
        try:        
            with io.open(self.settings_file, 'r', encoding='utf-8') as f:
                self._data = json.JSONDecoder().decode(f.read())
        except (EOFError, IOError, OSError, ValueError) as e:
            logging.info('loading configuration failed: %s', e)
            self._data = dict()
        
    @property
    def version(self):
        return 1

    @property
    def dot_sage_directory(self):
        return os.path.join(os.path.expanduser('~'), '.sage')

    @property
    def notebooks_directory(self):
        path = os.path.join(self.dot_sage_directory, 'notebooks')
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    @property 
    def settings_file(self):
        return os.path.join(self.notebooks_directory, 'settings.json')

    ###########################################################3
    # read/write properties follow

    @property
    def sage_root(self):
        return self._data.get('sage_root', None)

    @sage_root.setter
    def sage_root(self, value):
        self._data['sage_root'] = value
        self._save()

    @property
    def sage_version(self):
        return self._data.get('sage_version', 'Unknown version')
    
    @sage_version.setter
    def sage_version(self, value):
        self._data['sage_version'] = value
        self._save()

    @property 
    def window_geometry(self):
        return self._data.get('window_geometry', {})

    @window_geometry.setter
    def window_geometry(self, value):
        self._data['window_geometry'] = value
        self._save()

        
    
