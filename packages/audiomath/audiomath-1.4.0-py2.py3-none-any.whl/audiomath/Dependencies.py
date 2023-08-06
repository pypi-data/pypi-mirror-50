# $BEGIN_AUDIOMATH_LICENSE$
# 
# This file is part of the audiomath project, a Python framework for
# real-time manipulation of psychophysical stimuli for vision science.
# 
# Copyright (c) 2017-2019 Jeremy Hill, Scott Mooney
# 
# audiomath is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/ .
# 
# $END_AUDIOMATH_LICENSE$
__all__ = [
	'numpy',
]

import sys

from . import DependencyManagement; from .DependencyManagement import Import, Define, RegisterVersion

numpy = Import( 'numpy', registerVersion=True )

# Define but don't import yet (used less often for more specialized purposes, and might be slow to import)
Define( 'IPython', packageName='ipython', registerVersion=True )
Define( 'matplotlib', registerVersion=True )
