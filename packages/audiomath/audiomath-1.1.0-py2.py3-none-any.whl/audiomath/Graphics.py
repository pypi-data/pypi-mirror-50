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
	
]

import sys
import numpy

from . import Base; from .Base import Sound
	
def LoadPlt():
	try:
		import matplotlib
		if not 'matplotlib.backends' in sys.modules and 'IPython' in sys.modules:
			matplotlib.interactive( True )
		import matplotlib.pyplot as plt
		return plt
	except ImportError:
		moduleName = packageName = 'matplotlib'
		raise ImportError( '%s module failed to import %r - you need to install the third-party %s package for this functionality' % ( __name__, moduleName, packageName ) )

def Plot( self, hold=False, zeroBased=False ):
	nchan = self.NumberOfChannels()
	nsamp = self.NumberOfSamples()
	t = numpy.arange( 0, nsamp ) / float( self.fs )
	y = numpy.asarray( self.y ) / -2.0
	y = numpy.clip( y, -0.5, 0.5 )
	offset = numpy.arange( nchan )
	if not zeroBased: offset += 1
	y += offset

	plt = LoadPlt()
	if not hold: plt.cla()
	h = plt.plot( t, y )
	ax = plt.gca()
	ax.set_yticks( offset )
	ax.set_ylim( offset.max() + 1, offset.min() - 1 )
	ax.set_xlim( t[ 0 ], t[ -1 ] )
	ax.xaxis.grid( True )
	ax.yaxis.grid( True )
	plt.draw()
Sound.Plot = Plot
