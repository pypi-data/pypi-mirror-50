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
	'CURRENT_BACK_END',
]

import sys as _sys

DEFAULT = 'PortAudioInterface'

class _NotLoaded( object ):
	__bool__ = __nonzero__ = lambda self: False
	__getattr__ = lambda self, attrName: getattr( Load(), attrName )
CURRENT_BACK_END = _NotLoaded()


def Load( name=None ):
	
	global CURRENT_BACK_END
	if not name and not CURRENT_BACK_END:
		name = DEFAULT
	
	target = _sys.modules[ __package__ ]

	if CURRENT_BACK_END:
		for symbol in CURRENT_BACK_END.__all__:
			if hasattr( target, symbol ):
				delattr( target, symbol )
	if name:
		exec( 'from . import {name}'.format( name=name ) ) # TODO: could make more secure
		CURRENT_BACK_END = locals()[ name ]
		
	setattr( target, 'CURRENT_BACK_END', CURRENT_BACK_END )
	for symbol in CURRENT_BACK_END.__all__:
		setattr( target, symbol, getattr( CURRENT_BACK_END, symbol ) )
	return CURRENT_BACK_END
