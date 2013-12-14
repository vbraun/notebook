#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add our custom widgets to glade3
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
import sys


print('Importing Sage Notebook widgets')

gui_path = os.path.split(os.path.split(__file__)[0])[0]
sys.path.append(gui_path)
sage_notebook_path = os.path.split(os.path.split(gui_path)[0])[0]
sys.path.append(sage_notebook_path)

for p in sys.path:
    print(p)

from cell_widget import CellWidget



