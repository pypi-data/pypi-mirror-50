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
	'msec2samples', 'samples2msec',
	'ACROSS_SAMPLES', 'ACROSS_CHANNELS',
	'Silence', 'Rise', 'Plateau', 'Fall', 'HannWindow',
	'Cat', 'Stack', 'AutoScale', 'Center', 'Cut', 'PadEndTo', 'PadStartTo', 'Reverse', 'Trim',
	'PanHelper', 'InterpolateSamples',
	'Sound',
]
import numpy
from copy import deepcopy

ACROSS_SAMPLES  = 0
ACROSS_CHANNELS = 1
DEFAULT_DTYPE_IN_MEMORY = 'f4'

class SoundBug( Exception ): pass

def isnumpyarray( x ):
	return isinstance( x, numpy.ndarray )

DTYPES = dict(
	int8    = ( '<i1',  8, 1, True,  float( 2 **  7 ) ),
	int16   = ( '<i2', 16, 2, True,  float( 2 ** 15 ) ),
	int32   = ( '<i4', 32, 4, True,  float( 2 ** 31 ) ),
	int64   = ( '<i8', 64, 8, True,  float( 2 ** 63 ) ),
	uint8   = ( '<u1',  8, 1, False, float( 2 **  7 ) ), # yes that's correct
	uint16  = ( '<u2', 16, 2, False, float( 2 ** 15 ) ), # yes that's correct
	uint32  = ( '<u4', 32, 4, False, float( 2 ** 31 ) ), # yes that's correct
	uint64  = ( '<u8', 64, 8, False, float( 2 ** 63 ) ), # yes that's correct
	float32 = ( '<f4', 32, 4, True,  None ),
	float64 = ( '<f8', 64, 8, True,  None ),
)
for entry in list( DTYPES.values() ): DTYPES[ entry[ 0 ] ] = DTYPES[ entry[ 0 ][ 1: ] ] = entry
DTYPES[ None ] = DTYPES[ '<i2' ] # default

	
def msec2samples( msec, fs ):
	if hasattr( fs, 'fs' ): fs = fs.fs
	if msec is None or fs is None: return None
	if isinstance( msec, ( tuple, list ) ): msec = numpy.array( msec )
	if isinstance( msec, numpy.ndarray ): msec = msec.astype( numpy.float64 )
	else: msec = float( msec )
	return numpy.round( float( fs ) * msec / 1000.0 )

def samples2msec( samples, fs ):
	if hasattr(fs, 'fs'): fs = fs.fs
	if samples is None or fs is None: return None
	if isinstance( samples, ( tuple, list ) ): samples = numpy.array( samples )
	if isinstance( samples, numpy.ndarray ): samples = samples.astype( numpy.float64 )
	else: samples = float( samples )
	return 1000.0 * samples / float( fs )

def NumberOfSamples( a ):
	"""
	Return the number of samples in an array `a`, or in a `Sound` instance `a` that
	contains an array `a.y`.
	"""
	if hasattr( a, 'sound' ) and hasattr( a.sound, 'y' ) and isnumpyarray( a.sound.y ): a = a.sound.y
	elif hasattr( a, 'y' ) and isnumpyarray( a.y ): a = a.y
	if not isnumpyarray( a ): raise SoundBug( 'NumberOfSamples() function called on something other than a numpy.array' )
	if len( a.shape ) <= ACROSS_SAMPLES: return 1
	return a.shape[ ACROSS_SAMPLES ]

def NumberOfChannels(a):
	"""
	Return the number of channels in an array `a`, or in a `Sound` instance `a` that
	contains an array `a.y`.
	"""
	if hasattr( a, 'sound' ) and hasattr( a.sound, 'y' ) and isnumpyarray( a.sound.y ): a = a.sound.y
	elif hasattr( a, 'y' ) and isnumpyarray( a.y ): a = a.y
	if not isnumpyarray( a ): raise SoundBug( 'NumberOfChannels() function called on something other than a numpy.array' )
	if len( a.shape ) <= ACROSS_CHANNELS: return 1
	return a.shape[ ACROSS_CHANNELS ]

def infer_dtype( thing ):
	if hasattr( thing, 'sound' ) and hasattr( thing.sound, 'y' ) and isnumpyarray( thing.sound.y ): dtype = thing.sound.y.dtype
	elif hasattr( thing, 'y' ) and isnumpyarray( thing.y ): dtype = thing.y.dtype
	elif isnumpyarray( thing ): dtype = thing.dtype
	elif hasattr( thing, 'dtype_in_memory' ): dtype = thing.dtype_in_memory
	else: dtype = thing
	return dtype

def Silence( nsamp, nchan, dtype=DEFAULT_DTYPE_IN_MEMORY, dc=0 ):
	dtype = infer_dtype( dtype )
	if nsamp < 0: nsamp = 0
	z = numpy.zeros( ( int( nsamp ), int( nchan ) ), dtype )
	if dc: z += dc
	return z
	
def Rise( duration, fs=1000, hann=False ):
	y = numpy.linspace( 0.0, 1.0, msec2samples( duration * 1000.0, fs ) ).astype( DEFAULT_DTYPE_IN_MEMORY )
	y.shape = ( y.shape[ 0 ], 1 )
	if hann: y = 0.5 - 0.5 * numpy.cos( y * numpy.pi )
	s = Sound( fs=fs ); s.y = y; return s

def Plateau( duration, fs=1000, dc=1.0 ):
	y = Silence( msec2samples( duration * 1000.0, fs ), 1, dtype=DEFAULT_DTYPE_IN_MEMORY, dc=dc )
	s = Sound( fs=fs ); s.y = y; return s
	
def Fall( duration, fs=1000, hann=False ):
	y = numpy.linspace( 1.0, 0.0, msec2samples( duration * 1000.0, fs ) ).astype( DEFAULT_DTYPE_IN_MEMORY )
	y.shape = ( y.shape[ 0 ], 1 )
	if hann: y = 0.5 - 0.5 * numpy.cos( y * numpy.pi )
	s = Sound( fs=fs ); s.y = y; return s

def HannWindow( duration, fs=1000, plateau_duration=0 ):
	risetime = ( float( duration ) - float( plateau_duration ) ) / 2.0
	r = Rise( risetime, fs=fs, hann=True )
	f = Fall( risetime, fs=fs, hann=True )
	ns = msec2samples( duration * 1000.0, fs ) - r.NumberOfSamples() - f.NumberOfSamples()
	if ns > 0: p = Silence( ns, 1, dc=1.0 )
	else: p = 0.0
	return r % p % f

def Cat( *args ):
	"""
	Concatenate sounds in time.
	"""
	args = [ arg for item in args for arg in ( item if isinstance( item, ( tuple, list ) ) else [ item ] ) ]
	nchan = 1
	fs = None
	s = None
	for arg in args:
		if isinstance( arg, Sound ):
			if s is None: s = arg.copy()

			if nchan == 1: nchan = arg.NumberOfChannels()
			elif not arg.NumberOfChannels() in ( 1, nchan ): raise ValueError( 'incompatible numbers of channels' )

			if fs is None: fs = float( arg.fs )
			elif fs != arg.fs: raise ValueError( 'incompatible sampling frequencies' )
	if s is None:
		raise TypeError( 'no Sound object found' )
	for i, arg in enumerate( args ):
		if isinstance(arg, Sound):
			dat = arg.y
			if NumberOfChannels(dat) == 1 and nchan > 1:
				dat = dat.repeat(nchan, axis=ACROSS_CHANNELS)
		elif isinstance(arg, numpy.ndarray):
			dat = arg
		elif isinstance(arg,float) or isinstance(arg,int):
			nsamp = round(float(arg) * fs)
			nsamp = max(0, nsamp)
			dat = Silence(nsamp, nchan, s)
		else:
			raise TypeError( "don't know how to concatenate type %s" % arg.__class__.__name__ )
		args[i] = dat
	s.y = numpy.concatenate( args, axis=ACROSS_SAMPLES )
	return s

def Stack( *pargs ):
	"""
	Stack multiple Sound objects to make one multi-channel Sound object.
	"""
	s = []
	for arg in pargs:
		if isinstance( arg, ( list, tuple ) ): s.append( Stack( *arg ) )
		elif isinstance( arg, Sound ): s.append( arg )
		else: raise TypeError( "arguments must be Sound objects (or sequences thereof)" )
	out = s.pop( 0 ).copy()
	while len( s ): out &= s.pop( 0 )
	return out	

def AutoScale(s, max_abs_amp=0.95):
	"""
	Creates an auto-scaled copy of `Sound` instance `s` instead of modifying the
	instance. Otherwise, see the `Sound.AutoScale` method.
	"""
	s = s.copy()
	s.AutoScale(max_abs_amp=max_abs_amp)
	return s
	
def Center(s):
	s = s.copy()
	s.Center()
	return s
	
def Cut(s, start=None, stop=None):
	s = s.copy()
	s.Cut(start=start, stop=stop)
	return s

def PadEndTo(s, seconds):
	s = s.copy()
	s.PadEndTo(seconds=seconds)
	return s

def PadStartTo(s, seconds):
	s = s.copy()
	s.PadStartTo(seconds=seconds)
	return s

def Reverse(s):
	s = s.copy()
	s.Reverse()
	return s

def Trim(s, thresh=0.05, tailoff=0.2):
	s = s.copy()
	s.Trim(thresh=thresh, tailoff=tailoff)
	return s

def PanHelper( v, nchan=None, norm='inf' ):
	
	try:
		nchan = int( nchan )
	except:
		if nchan is not None: nchan = NumberOfChannels( nchan )
	
	if isinstance( v, ( tuple, list, numpy.ndarray ) ):
		v = numpy.array( v, dtype='float' )
		v = v.flatten()
		if len( v )==1:
			v = float( v[ 0 ] ) # scalar numpy value
		else:
			# Interpret any kind of multi-element tuple/list/array
			# as a per-channel list of volumes. Just standardize its
			# shape and size. Ignore the norm parameter.
			if nchan is None: nchan = len( v )
			elif len( v ) < nchan: v = numpy.tile( v, numpy.ceil( float( nchan ) / len( v ) ) )
			if len( v ) > nchan: v = v[ :nchan ]
			shape = [ 1, 1 ]
			shape[ ACROSS_CHANNELS ] = nchan
			v.shape = tuple( shape )
	else:
		v = float( v ) # could be converting from Modulator, etc
		
	if isinstance( v, float ):
		# Interpret any kind of scalar as a stereo pan value in the
		# range -1 to +1. Normalize according to the specified norm.
		if nchan is None: nchan = 2
		v = 0.5 + 0.5 * numpy.clip( [ -v, v ], -1.0, 1.0 )
		if nchan > 2: v = numpy.tile( v, int( nchan / 2 ) )
		if len( v ) == nchan - 1: v = numpy.concatenate( ( v, [ 1.0 ] ) )
		if isinstance( norm, str)  and norm.lower() == 'inf': norm = numpy.inf
		if norm in [ numpy.inf, 'inf', 'INF' ]: v /= max( v )
		else: v /= sum( v ** norm ) ** ( 1.0 / { 0.0:1.0 }.get( norm, norm ) )
		v = PanHelper( v, nchan=nchan )

	return v

def InterpolateSamples( y, xi ):
	sub = [ slice( None ), slice( None ) ]
	x = numpy.arange( float( NumberOfSamples( y ) ) )
	shape = [ 1, 1 ]
	shape[ ACROSS_SAMPLES ] = len( xi )
	shape[ ACROSS_CHANNELS ] = NumberOfChannels( y )
	yi = numpy.zeros( shape, dtype='float' )
	for sub[ ACROSS_CHANNELS ] in range( NumberOfChannels( y ) ):
		tsub = tuple( sub )
		yi[ tsub ] = numpy.interp( x=xi, xp=x, fp=y[ tsub ] )
	return yi


class Sound( object ):
	debug = False

	"""
	`s = Sound(filename)` creates a Sound object

	`s.y` is a `numpy.array` containing the sound data.
	
	In addition to the more obvious object methods, here is some operator
	overloading you might enjoy:
	
	Slicing, expressed in units of seconds:
	
		The following syntax returns Sound objects wrapped around slices
		into the original array::

			s[:0.5]   #  returns the first half-second of `s`
			s[-0.5:]  #  returns the last half-second of `s`
			
			s[ :, 0 ] # returns the first channel of `s`
			s[ :, -2: ] # returns the last two channels of `s`
			s[ 0.25:0.5, [0,1,3] ] # returns a particular time-slice of the chosen channels
			
		Where possible, the resulting `Sound` instances' arrays are *views* into
		the original sound data. Therefore, things like  `s[2.0:-1.0].AutoScale()`
		or  `s[1.0:2.0] *= 2` will change the specified segments of the *original*
		sound data in `s`. Note one subtlety, however ::
		
		    # Does each of these examples modify the selected segment of `s` in-place?
		                                      
			s[ 0.1:0.2,  : ] *= 2             # yes
			q = s[ 0.1:0.2,  : ];  q *= 2     # yes  (`q` contains a view into `s`)
			
			s[ 0.1:0.2,  ::2 ] *= 2           # yes
			q = s[ 0.1:0.2,  ::2 ];  q *= 2   # yes  (`q` contains a view into `s`)
			
			s[ 0.1:0.2,  0 ] *= 2             # yes (creates a copy, but then uses `__setitem__` on the original)
			q = s[ 0.1:0.2,  0 ];  q *= 2     # - NO (creates a copy, then just modifies the copy in-place)
			
			s[ 0.1:0.2,  [1,3] ] *= 2         # yes (creates a copy, but then uses `__setitem__` on the original)
			q = s[ 0.1:0.2,  [1,3] ];  q *= 2 # - NO (creates a copy, then just modifies the copy in-place)
	
	Numerical ops:
	
		- The `+` and `-` operators can be used to superimpose sounds (even if lengths
		  do not match).
		  
		- The `*` and `/` operators can be used to scale amplitudes (usually by a
		  scalar numeric factor, but you can also use a list of scaling factors to
		  scale channels separately, or window a signal by multiplying two objects
		  together).
		  
		- The `+=`, `-=`, `*=` and `/=` operators work as you might expect, modifying
		  a `Sound` instance's data array in-place.
	 
	Concatenation of sound data in time:
	
		The syntax `s1 % s2` is the same as `Cat( s1, s2 )`---i.e. it returns
		a new `Sound` instance containing a new array of samples, in which the
		samples of `s1` and `s2` are concatenated in time. This can be performed
		even if there is a mismatch in the number of channels.
		
		Either argument may be a scalar,  so `s % 0.4` returns a new object with
		400 msec of silence appended, and `0.4 % s` returns a new object with 400
		msec of silence pre-pended.
	
		Concatenation can be performed in-place with `s %= arg` or equivalently
		using the instance method `s.Cat( arg1, arg2, ... )`: in either case the
		instance `s` gets its internal sample array replaced by a new array.
	
	Creating multichannel objects:
	
		The syntax `s1 & s2` is the same as `Stack( s1, s2 )`---i.e. it returns a
		new `Sound` instance containing a new array of samples, comprising the
		channels of `s1` and the channels of `s2`. Either one may be automatically
		padded with silence at the end as necessary to ensure that the lengths match.
		
		Stacking may be performed in-place with `s1 &= s2` or equivalently with the
		instance method `s1.Stack( s2, s3, ... ):  in either case instance `s1` gets
		its internal sample array replaced by a new array.

	"""
	
	def __init__(self, source=None, fs=None, bits=None, nchan=2, dtype=None ):
		"""
		DOC-TODO
		"""
		self.__y = numpy.zeros( ( 0, nchan ), dtype=DEFAULT_DTYPE_IN_MEMORY )
		self.__fs = None
		self.__revision = 0
		self.__compression = ( 'NONE', 'not compressed' )
		self.__dtype_encoded = None
		self.filename = None
		
		if isinstance( source, Sound ):
			self.__y = source.__y
			self.__fs = source.__fs
			self.filename = source.filename
			self.__compression = source.__compression
			self.__dtype_encoded = source.__dtype_encoded
			source = None
		
		if dtype: self.dtype_encoded = dtype
		if self.__dtype_encoded is None and bits is None: bits = 16
		if bits is not None: self.bits = bits   # NB: changes self.__dtype_encoded
		
		if self.__fs is None and fs is None: fs = 44100
		if fs is not None: self.fs = fs

		if isinstance( source, ( int, float ) ): self.y = Silence( msec2samples( source * 1000.0, self ), nchan, dtype=dtype )
		elif isnumpyarray( source ): self.y = source
		elif source is not None: self.Read( source )
			
		
	
	def Copy( self, empty=False ):
		y = self.__y
		if empty and y is not None: self.__y = y[ :0 ]
		c = deepcopy( self )
		self.__y = y
		return c
	copy = Copy
	
	@property
	def y( self ): return self.__y
	@y.setter
	def y( self, value ):
		if not isnumpyarray( value ): value = numpy.array( value, dtype=DEFAULT_DTYPE_IN_MEMORY )
		if value.ndim > 2: raise ValueError( "too many dimensions" )
		while value.ndim < 2: value = value[ :, None ]
		self.__y = value
	
	@property
	def fs( self ): return self.__fs
	@fs.setter
	def fs( self, value ): self.__fs = float( value )
	
	@property
	def revision( self ): return self.__revision
	
	@property
	def compression( self ): return self.__compression
	@compression.setter
	def compression( self, value ):
		if not isinstance( value, ( tuple, list ) ) or len( value ) != 2 or not isinstance( value[ 0 ], str ) or not isinstance( value[ 1 ], str ):
			raise ValueError( ".compression must be a sequence of two strings" )
		self.__compression = value
	
	@property
	def bits( self ): canonical_dtype, nbits, nbytes, signed, factor = DTYPES[ self.__dtype_encoded ]; return nbits
	@bits.setter
	def bits( self, value ): self.SetBitDepth( value )
	nbits = bits
	
	@property
	def bytes( self ): return int( numpy.ceil( self.bits / 8.0 ) )
	nbytes = bytes
	
	@property
	def dtype_encoded( self ): return self.__dtype_encoded
	@dtype_encoded.setter
	def dtype_encoded( self, value ): canonical_dtype, nbits, nbytes, signed, factor = DTYPES[ value ]; self.__dtype_encoded = canonical_dtype
	
	@property
	def dtype_in_memory( self ): return self.__y.dtype.name
	@dtype_in_memory.setter
	def dtype_in_memory( self, value ): self.__y = self.__y.astype( value )
		
	
			
	def SetBitDepth(self, bits):
		if   bits ==  8: dtype = '<u1'  # yep
		elif bits == 16: dtype = '<i2'
		elif bits == 24: dtype = '<i4'
		elif bits == 32: dtype = '<i4'
		elif isinstance( bits, str ): dtype = bits.lower()
		else: raise ValueError( 'unrecognized bit precision' )
		
		dtype, nbits, nbytes, signed, factor = DTYPES[ dtype ]
		if dtype != self.__dtype_encoded: self._BumpRevision()
		self.__dtype_encoded = dtype

	def NumberOfChannels( self ):
		"""
		`s.NumberOfChannels()` returns the number of channels.
		"""
		return NumberOfChannels( self )
		
	def NumberOfSamples( self ):
		"""
		`s.NumberOfSamples()` returns the length of the sound in samples.
		"""
		return NumberOfSamples( self )
	
	def Duration(self):
		"""
		`s.Duration()` returns the duration of the sound in seconds.
		"""
		return float( self.NumberOfSamples() ) / float( self.fs )
		
	def __repr__(self):
		s = "<%s.%s instance at 0x%08X>" % ( self.__class__.__module__, self.__class__.__name__, id( self ) )
		if self.filename: s += '\n    (file %s)' % self.filename
		s += '\n'
		s += '    %d bits, %d channels, %d samples @ %g Hz = %g sec' % ( self.bits, self.NumberOfChannels(), self.NumberOfSamples(), self.fs, self.Duration() )
		return s
			
	def str2dat( self, raw, nsamp=None, nchan=None, dtype=None ):
		if dtype is None: dtype = self.__dtype_encoded
		else: dtype = dtype.lower()
		canonical_dtype, nbits, nbytes, signed, factor = DTYPES[ dtype ]
		if nchan is None: nchan = self.NumberOfChannels()
		y = numpy.fromstring( raw, dtype=canonical_dtype )
		if nsamp is None: nsamp = int( y.size / nchan )
		y.shape = ( nsamp, nchan )
		y = y.astype( self.dtype_in_memory )
		if factor:
			if not signed: y -= factor
			y /= factor
		return y

	def dat2str(self, data=None):
		"""
		s.dat2str(data=None) converts from a numpy.array to a string.
		data defaults to s.y
		
		The string output contains raw bytes which can be written, for example, to an
		open audio stream.
		"""
		if isinstance(data,str): return data
		if data is None: data = self.y
		nchan = NumberOfChannels(data)
		nsamp = NumberOfSamples(data)
		if nchan != self.NumberOfChannels():
			raise ValueError( 'data has a different number of channels from object' )
		dtype = self.__dtype_encoded
		canonical_dtype, nbits, nbytes, signed, factor = DTYPES[ dtype ]
		if factor:
			data = data * factor
			data = numpy.clip(data, -factor, factor - 1)
			if not signed: data += factor
			#data += 0.5 # in principle the astype method should perform a floor() operation, so adding 0.5 first should be a good idea. however, for some reason it doesn't correctly reconstruct the original raw data when this is added
		data = data.astype( dtype )
		data = data.tostring()
		return data

	def AutoScale( self, max_abs_amp=0.95 ):
		self.Center()
		m = abs( self.y ).max()
		self.y *= ( max_abs_amp / m )
		self._BumpRevision()
	
	def Cat( self, *args ):
		s = Cat( self, *args )
		self.y = s.y
		self._BumpRevision()

	def Center( self ):
		"""
		Remove the DC offset from each channel by subtracting the median value.
		"""
		try: med = numpy.median( self.y, axis=ACROSS_SAMPLES ) # newer numpy versions only
		except: med = numpy.median( self.y ) # older numpy versions only (grr!)
		shape = list( self.y.shape )
		shape[ ACROSS_SAMPLES ] = 1
		med.shape = shape
		self.y -= med
		self._BumpRevision()
		
	def Cut( self, start=None, stop=None ):
		"""
		Shorten the instance's internal sample array by taking only samples
		from `start` to `stop`.  Either end-point may be `None`. Either may be
		a positive number of seconds (measured from the start) or a negative
		number of seconds (measured from the end).
		"""
		if start is None:  start = 0.0
		if stop is None: stop = self.Duration()
		if start < 0.0: start += self.Duration()
		if stop < 0.0:  stop += self.Duration()
		start = max( 0, round( float( start ) * float( self.fs ) ) )
		stop = min( self.NumberOfSamples(), round( float( stop ) * float( self.fs ) ) )
		stop = max( start, stop )
		subs = [ slice( None ), slice( None ) ]
		subs[ ACROSS_SAMPLES ] = slice( start, stop )
		self.y = self.y[ subs[ 0 ], subs[ 1 ] ]
		self._BumpRevision()
		
	
	def IsolateChannels( self, ind ):
		"""
		DOC-TODO
		"""
		subs = [ slice( None ), slice( None ) ]
		subs[ ACROSS_CHANNELS ] = ind
		s.y = s.y[ subs[ 0 ], subs[ 1 ] ]
	
	def ExtractChannels( self, ind ):
		"""
		Return a new `Sound` instance containing a copy of the specified channel or
		channels of the original.
		"""
		s = self.copy()
		s.IsolateChannels( ind )
		return s
	
	def Fade( self, risetime=0, falltime=0, hann=False ):
		if risetime: self[ :float( risetime ) ]  *= Rise( risetime, fs=self.fs, hann=hann )
		if falltime: self[ -float( falltime ): ] *= Fall( falltime, fs=self.fs, hann=hann )
		self._BumpRevision()
	
	def HannWindow( self ):
		return HannWindow( self.Duration(), self.fs )
		
	def Left( self ):
		s = self.copy() # new instance...
		subs = [ slice( None ), slice( None ) ]
		subs[ ACROSS_CHANNELS ] = slice( 0, None, 2 )
		s.y = self.y[ subs[ 0 ], subs[ 1 ] ]  # ...but a view into the original array
		return s

	def Right( self ):
		s = self.copy() # new instance...
		subs = [ slice( None ), slice( None ) ]
		subs[ ACROSS_CHANNELS ] = slice( 1 if self.NumberOfChannels() > 1 else 0, None, 2 )
		s.y = self.y[ subs[ 0 ], subs[ 1 ] ]  # ...but a view into the original array
		return s

	def Mono(self):
		s = self.copy()
		s.y = numpy.asmatrix(s.y).mean(axis=ACROSS_CHANNELS).A
		return s
		
	def PadEndTo(self, seconds):
		if isinstance(seconds, Sound):
			seconds = seconds.Duration()
		extra_sec = seconds - self.Duration()
		if extra_sec > 0.0:
			s = Cat(self, extra_sec)
			self.y = s.y
		self._BumpRevision()
	
	def PadStartTo(self, seconds):
		if isinstance(seconds, Sound):
			seconds = seconds.Duration()
		extra_sec = seconds - self.Duration()
		if extra_sec > 0.0:
			s = Cat(extra_sec, self)
			self.y = s.y
		self._BumpRevision()
	
	def Reverse( self ):
		self.y = numpy.flipud( self.y )
		self._BumpRevision()			
	
	def Trim(self, thresh=0.05, tailoff=0.2):
		y = numpy.max(abs(self.y), axis=ACROSS_CHANNELS)
		start,stop = numpy.where(y>thresh)[0][[0,-1]]
		stop += round(float(tailoff) * float(self.fs))
		stop = min(stop, self.NumberOfSamples())
		y = self.y[start:stop,:]
		self.y = y.copy()
		self._BumpRevision()	
		
	def _BumpRevision(self):
		self.__revision += 1
		
	def _PrepareForArithmetic( self, other, equalize_channels=True, equalize_duration=True ):
		if isinstance( other, Sound ):
			if self.fs != other.fs:
				raise ValueError( 'incompatible sampling rates' )
			other = other.y
		me = self.y
		if isinstance( other, list ) and False not in [ isinstance( x, ( bool, int, float ) ) for x in other ]:
			other = numpy.concatenate( [ numpy.asmatrix( x, dtype=numpy.float64 ).A for x in other ], axis=ACROSS_CHANNELS )
			equalize_duration = False
		if isnumpyarray( other ):
			if equalize_channels:
				if NumberOfChannels( other ) == 1 and NumberOfChannels( me ) > 1:
					other = other.repeat( NumberOfChannels( me ), axis=ACROSS_CHANNELS )
				if NumberOfChannels( other ) > 1 and NumberOfChannels( me ) == 1:
					me = me.repeat( NumberOfChannels( other ), axis=ACROSS_CHANNELS )
			nchan_me = NumberOfChannels( me )
			nchan_other = NumberOfChannels( other )
			if equalize_channels and nchan_other != nchan_me:
				raise ValueError( 'incompatible numbers of channels' )
			if equalize_duration:
				needed = NumberOfSamples( other ) - NumberOfSamples( me )
				if needed > 0:
					extra = Silence( needed, nchan_me, me )
					me = numpy.concatenate( ( me, extra ), axis=ACROSS_SAMPLES )
				if needed < 0:
					extra = Silence( -needed, nchan_other, other )
					other = numpy.concatenate( ( other, extra ), axis=ACROSS_SAMPLES )
		return ( me, other )
	
	# addition, subtraction
	def __iadd__( self, other ):
		( me, other ) = self._PrepareForArithmetic( other )
		me += other
		self.y = me
		self._BumpRevision()
		return self
	def __add__( self, other ):
		return self.copy().__iadd__( other )
	def __radd__( self, other ):
		return self.__add__( other )
	def __isub__(self, other):
		( me, other ) = self._PrepareForArithmetic( other )
		me -= other
		self.y = me
		self._BumpRevision()
		return self
	def __sub__( self, other ):
		return self.copy().__isub__( other )
	def __rsub__( self, other ):
		s = self.__mul__( -1 )
		s.__iadd__( other )
		return s

	# multiplication, division
	def __imul__( self, other ):
		( me, other ) = self._PrepareForArithmetic( other )
		me *= other
		self.y = me		
		self._BumpRevision()
		return self
	def __mul__( self, other ):
		return self.copy().__imul__( other )
	def __rmul__( self, other ):
		return self.__mul__( other )
	def __idiv__( self, other ):
		( me, other ) = self._PrepareForArithmetic( other )
		me /= other
		self.y = me		
		self._BumpRevision()
		return self
	def __div__( self, other ):
		return self.copy().__idiv__( other )
	__truediv__ = __div__
	__itruediv__ = __idiv__

	# Channel-stacking using the & operator
	def __iand__( self, other ):
		if not ( isinstance( other, Sound ) or isnumpyarray( other ) ):
			raise TypeError( 'w1 & w2 only works if w1 and w2 are both wavs, or if w2 is a numpy.array' )
		( me, other ) = self._PrepareForArithmetic( other, equalize_channels=False )
		me = numpy.concatenate( ( me, other ), axis=ACROSS_CHANNELS )
		self.y = me
		self._BumpRevision()
		return self
	def __and__( self, other ):
		return self.copy().__iand__( other )
	
	# Concatenation using the % operator
	def __imod__( self, other ):
		self.Cat( other )
		self._BumpRevision()
		return self
	def __mod__( self, other ):
		return Cat( self, other )
	def __rmod__( self, other ):
		return Cat( other, self )

	# Unary + and - (both cause data to be deep-copied)
	def __neg__( self ): return -1.0 * self
	def __pos__( self ): return self.copy()

	# Slicing with [] indexing, (first ranges expressed in seconds, second channel index or range):
	def __getitem__(self, range):
		subs = self._TranslateSlice(range)
		s = Sound(fs=self.fs, bits=self.bits, nchan=NumberOfChannels(self))
		s.y = self.y[subs[0],subs[1]]
		return s

	def __setitem__(self, range, val):
		subs = self._TranslateSlice(range)
		if isinstance(val,Sound): val = val.y
		self.y[subs[0],subs[1]] = val
		self._BumpRevision()

	def _TranslateSlice( self, range ):
		chans = slice( None )
		if isinstance( range, ( tuple, list ) ): range, chans = range
		if not isinstance( range, slice ): raise TypeError( 'indices must be ranges, expressed in seconds' )
		if isinstance( chans, ( int, float ) ): chans = [ chans ]
		subs = [ None, None ]

		start, stop, step = None, None, None
		if range.step is not None:
			raise ValueError( 'custom step sizes are not possible when slicing %s objects in time' % self.__class__.__name__ )
		if range.start is not None:
			start = int( msec2samples( float( range.start ) * 1000.0, self ) )
			if range.stop is not None:
				stop = min( range.stop, self.Duration() )
				duration = float( stop ) - float( range.start )
				stop  = int( msec2samples( duration * 1000.0, self ) ) + start
		elif range.stop is not None:
			stop = int( msec2samples( float( range.stop ) * 1000.0, self ) )

		subs[ ACROSS_SAMPLES ] = slice( start, stop, step )
		subs[ ACROSS_CHANNELS ] = chans
		return subs
	
	def msec2samples( self, msec ):
		return msec2samples( msec, self )
		
	def samples2msec( self, samples ):
		return samples2msec( samples, self )
	
	def Resample( self, newfs ):
		s = self.copy()
		if newfs != s.fs:
			newN = s.NumberOfSamples() * newfs / s.fs
			s.y = InterpolateSamples( s.y, numpy.linspace( 0, s.NumberOfSamples(), newN, endpoint=False ) )
			s.fs = newfs
		return s

	def Play( self, *pargs, **kwargs ):
		from . import BackEnd; from .BackEnd import CURRENT_BACK_END as impl
		p = impl.Player( self, verbose=True )
		p.Play( *pargs, **kwargs )
		p.Wait()
	
	def Record( self, **kwargs ):
		from . import BackEnd; from .BackEnd import CURRENT_BACK_END as impl
		kwargs[ 'verbose' ] = True
		impl.Record( self, **kwargs )
		# TODO: doesn't cope well with mismatch between number-of-channels or sampling-frequency, between Sound and Stream
