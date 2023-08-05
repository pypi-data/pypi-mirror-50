# $BEGIN_AUDIOMATH_LICENSE$
# 
# This file is part of the audiomath project, a Python package for
# recording, manipulating and playing sound files.
# 
# Copyright (c) 2017-2019 Jeremy Hill
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
	'__meta__',
	'__version__',
	'PackagePath',
	'WhereAmI',
	'PACKAGE_LOCATION',
]

import os
import ast
import inspect

def WhereAmI( nFileSystemLevelsUp=1, nStackLevelsBack=0 ):
	"""
	`WhereAmI( 0 )` is equivalent to `__file__`
	
	`WhereAmI()` or `WhereAmI(1)` gives you the current source file's
	parent directory.
	"""
	try:
		frame = inspect.currentframe()
		for i in range( abs( nStackLevelsBack ) + 1 ):
			frame = frame.f_back
		file = inspect.getfile( frame )
	finally:
		del frame  # https://docs.python.org/3/library/inspect.html#the-interpreter-stack
	return os.path.realpath( os.path.join( file, *[ '..' ] * abs( nFileSystemLevelsUp ) ) )
	
PACKAGE_LOCATION = WhereAmI()

def PackagePath( *pieces ):
	return os.path.realpath( os.path.join( PACKAGE_LOCATION, *pieces ) )

__meta__ = ast.literal_eval( open( PackagePath( 'MASTER_META' ), 'rt' ).read() )
__version__ = __meta__[ 'version' ]
