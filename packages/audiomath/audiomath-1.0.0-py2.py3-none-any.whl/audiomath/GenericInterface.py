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

"""
The GenericInterface submodule provides `GenericPlayer`. and `GenericRecorder` classes.
Specific interface implementations can subclass these.
"""
__all__ = [
	'Fader',
]

import sys
import time
import inspect
import weakref

import numpy

from . import Base; from .Base import Sound

class GenericPlayer( object ):

	__global_t0 = [ None ]
	
	def __init__( self, sound=None ):
		if not isinstance( sound, Sound ): sound = Sound( sound )
		self.sound = sound
		self._loop = False
		self._playing = False
		self._speed = 1.0
		self._volume = 1.0
		self._levels = []
		self._pan = 0.0
		self._norm = 'inf'
		self._t0 = None
		self._nextSample = 0
		self._blank = None
		self._blankParams = None
		self._channelSub = None
		self._channelSubParams = None
		self._sampleSub = None
		self._sampleSubParams = None
		self._sampleRateEqualizationFactor = 1.0
		self.__synchronizeDynamics = True
		self.__panLevels = [ 1.0, 1.0 ]

	@property
	def synchronizeDynamics( self ): return True if self.__synchronizeDynamics else False
	@synchronizeDynamics.setter
	def synchronizeDynamics( self, value ):
		if value:
			if self.__synchronizeDynamics: return
			self.__synchronizeDynamics = 'playing'
			self._t0 = None
		else:
			if not self.__synchronizeDynamics: return
			self.__synchronizeDynamics = False
			self._t0 = self.__global_t0[ 0 ]
			
		if not value and self.__synchronizeDynamics: return
		
	def _OutputCallback( self, t, outputFrameCount, numberOfChannels, sampleFormat ):
		
		if self.__global_t0[ 0 ] is None: self.__global_t0[ 0 ] = t # all players will share this t0
		if self._t0 is None: self._t0 = t
		
		runDynamics = True
		if self.__synchronizeDynamics:
			runDynamics = self._playing
			if self.__synchronizeDynamics == 'playing' and not self._playing:
				self.__synchronizeDynamics = ( 'paused', t )
			elif isinstance( self.__synchronizeDynamics, tuple ) and self._playing:
				self._t0 += t - self.__synchronizeDynamics[ 1 ]
				self.__synchronizeDynamics = 'playing'
				
		t -= self._t0
		if runDynamics: self._RunDynamics( t )

		if not self._playing or not self._speed:
			return None

		blankParams = ( outputFrameCount, numberOfChannels, sampleFormat )
		if self._blankParams != blankParams:
			self._blankParams = blankParams
			self._blank = numpy.zeros( [ outputFrameCount, numberOfChannels ], dtype=sampleFormat )
		frame = self._blank

		speed = self._speed * self._sampleRateEqualizationFactor
		sampleSubParams = ( outputFrameCount, speed )
		if speed == 1.0:
			if self._sampleSubParams != sampleSubParams:
				self._sampleSubParams = sampleSubParams
				self._sampleSub = numpy.arange( outputFrameCount ) # NB: not a slice (see below)
			sampleSub = self._sampleSub + int( self._nextSample )
			nextSample = sampleSub[ -1 ] + 1
		else:
			if self._sampleSubParams != sampleSubParams:
				self._sampleSubParams = sampleSubParams
				self._sampleSub = numpy.linspace( 0, outputFrameCount * speed, outputFrameCount, endpoint=False )
			sampleSub = ( self._sampleSub + self._nextSample ).astype( int )
			nextSample = self._nextSample + outputFrameCount * speed
		
		snd = self.sound
		nSamplesAvailable = snd.NumberOfSamples()		
		if self._loop:
			sampleSub %= nSamplesAvailable
		elif sampleSub[ -1 ] >= nSamplesAvailable:
			sampleSub = sampleSub[ sampleSub < nSamplesAvailable ]
			frame.flat = 0 # silence the frame (although the beginning may be overwritten below)
			nextSample = 0
			self.playing = False
		source = snd.y[ sampleSub, : ] # this creates a copy, because sampleSub is a sequence not a slice
		
		nChannelsAvailable = source.shape[ 1 ]
		channelSubParams = ( numberOfChannels, nChannelsAvailable )
		if self._channelSubParams != channelSubParams:
			self._channelSubParams = channelSubParams
			if   numberOfChannels == nChannelsAvailable: self._channelSub = slice( None )
			elif numberOfChannels <  nChannelsAvailable: self._channelSub = slice( None, numberOfChannels )
			else: self._channelSub = ( list( range( nChannelsAvailable ) ) * numberOfChannels )[ :numberOfChannels ]
		channelSub = self._channelSub
		if channelSub: source = source[ :, channelSub ]
		
		# TODO: apply scaling factor if changing formats between float and int
		left, right = self.__panLevels
		left *= self._volume
		right *= self._volume
		if left  != 1.0: source[ :, 0::2 ] *= left
		if right != 1.0: source[ :, 1::2 ] *= right
		levels = self._levels
		if levels:
			nch = source.shape[ 1 ]
			if len( levels ) != nch: levels[ : ] = ( levels * nch )[ :nch ]
			source *= [ levels ]
		frame[ :source.shape[ 0 ], :source.shape[ 1 ] ] = source # TODO: optimize packing of frame when created?
		self._nextSample = nextSample
		return frame
		
	@property
	def nInputChannels( self  ):
		return self._nInputChannels # TODO: not plumbed in
		
	@property
	def nOutputChannels( self ):
		return self._nOutputChannels # TODO: not plumbed in
	
	@property
	def playing( self ):
		return self._playing
	@playing.setter
	def playing( self, value ):
		if self.SetDynamic( 'playing', value if callable( value ) else None ): return
		self._playing = value
	
	@property
	def loop( self ):
		return self._loop
	@loop.setter
	def loop( self, value ):
		if self.SetDynamic( 'loop', value if callable( value ) else None ): return
		self._loop = value
	
	@property
	def speed( self ):
		"""DOC-TODO"""
		return self._speed
	@speed.setter
	def speed( self, value ):
		if self.SetDynamic( 'speed', value if callable( value ) else None ): return
		self._speed = float( value )
		
	@property
	def volume( self ):
		"""DOC-TODO"""
		return self._volume
	@volume.setter
	def volume( self, value ):
		if self.SetDynamic( 'volume', value if callable( value ) else None ): return
		self._volume = float( value )
	vol = volume
	
	@property
	def levels( self ):
		"""DOC-TODO"""
		return self._levels
	@levels.setter
	def levels( self, value ):
		if self.SetDynamic( 'levels', value if callable( value ) else None ): return
		try: len( value )
		except: value = [ float( value ) ]
		else: value = [ float( each ) for each in value ]
		self._levels[ : ] = value

	@property
	def pan( self ):
		"""DOC-TODO"""
		return self._pan
	@pan.setter
	def pan( self, value ):
		if self.SetDynamic( 'pan', value if callable( value ) else None ): return
		try: len( value )
		except: pass
		else: self.__panLevels[ : ] = float( value[ 0 ] ), float( value[ 1 ] ); return
		self._pan = float( value )
		self._UpdateLevels( pan=value )

	@property
	def norm( self ):
		"""DOC-TODO"""
		return self._norm
	@norm.setter
	def norm( self, value ):
		if self.SetDynamic( 'norm', value if callable( value ) else None ): return
		self._norm = value
		self._UpdateLevels( norm=value )
		
	def _UpdateLevels( self, pan=None, norm=None ):
		if pan  is None: pan  = self._pan
		if norm is None: norm = self._norm
		if norm is None or pan is None: return
		v = [ 0.5 + 0.5 * min( 1.0, max( -1.0, vi ) ) for vi in [ -pan, pan ] ]
		if 'inf' in str( norm ).lower():  denom = max( v, key=abs )
		else: denom = sum( vi ** norm for vi in v ) ** ( 1.0 / norm if norm else 1.0 )
		if denom: v = [ vi / float( denom ) for vi in v ]
		self.__panLevels[ : ] = v
	
	def GetDynamic( self, name ):
		"""
		DOC-TODO
		"""
		dynamics = getattr( self, '_dynamics', None )
		return dynamics.get( name, None ) if dynamics else None
		
	def SetDynamic( self, name, func, order=1 ):
		"""
		DOC-TODO
		"""
		dynamics = getattr( self, '_dynamics', None )
		if func is None:
			if dynamics: dynamics.pop( name, None )
		else:
			if dynamics is None: dynamics = self._dynamics = {}
			try: getargspec = inspect.getfullargspec
			except: getargspec = inspect.getargspec
			try: spec = getargspec( func )
			except: spec = getargspec( func.__call__ )
			nArgs = len( spec.args )
			if hasattr( func, '__self__' ): nArgs -= 1
			elif not inspect.isfunction( func ) and not inspect.ismethod( func ): nArgs -= 1  # callable custom instance: won't have a __self__ itself but its __call__ method will
			if nArgs == 0 and spec.varargs: nArgs = 1
			dynamics[ name ] = ( order, name, func, nArgs )
			return func
	
	def _RunDynamics( self, t ):
		dynamics = getattr( self, '_dynamics', None )
		if dynamics is None: dynamics = self._dynamics = {}
		updates = {}
		for entry in sorted( dynamics.values() ):
			order, name, func, nArgs = entry
			try:
				if nArgs == 0: value = func()
				elif nArgs == 1: value = func( t )
				elif nArgs == 2: value = func( self, t )
				else: raise TypeError( 'dynamic property values should take 0, 1 or 2 arguments' )
			except StopIteration as exc:
				value = None
				for arg in exc.args:
					if isinstance( arg, dict ):
						if value is None: value = arg.pop( '_', None )
						updates.update( arg )
					else: value = arg
				if value is None: dynamics.pop( name )
				else: setattr( self, name, value )
			except:
				einfo = sys.exc_info()
				sys.stderr.write( 'Exception while evaluating dynamic .%s property of %s:\n' % ( name, self ) )
				getattr( self, '_excepthook', sys.excepthook )( *einfo )
				dynamics.pop( name )
			else:
				setattr( self, name, value )
				dynamics[ name ] = entry
		if updates:
			for name, value in updates.items():
				setattr( self, name, value )

	def Set( self, **kwargs ):
		for k, v in kwargs.items():
			if not hasattr( self, k ): raise AttributeError( '%s instance has no attribute %r' % ( self.__class__.__name__, k ) )
			setattr( self, k, v )
		return self
		
	def Play( self, position=None, wait=False, **kwargs ):
		"""
		DOC-TODO
		"""
		if position is not None: self.Seek( position )
		if kwargs: self.Set( **kwargs )
		self._playing = True
		if wait: self.Wait()
		#return self
		
	def Pause( self, position=None, **kwargs ):
		"""
		DOC-TODO
		"""
		if position is not None: self.Seek( position )
		if kwargs: self.Set( **kwargs )
		self._playing = False
		#return self
	Stop = Pause
	
	def Wait( self ):
		"""
		DOC-TODO
		"""
		try:
			while self.playing: time.sleep( 0.001 )
		except KeyboardInterrupt:
			self.playing = False

	def Seek( self, position, relative=False ):
		"""
		DOC-TODO
		"""
		samples = int( round( self.sound.fs * position ) )
		if relative: self._nextSample = max( 0, self._nextSample + samples )
		else: self._nextSample = ( self.sound.NumberOfSamples() + samples ) if samples < 0 else samples
		return self
	
	@property
	def head( self ):
		return self._nextSample / self.sound.fs
	@head.setter
	def head( self, value ):
		self.Seek( value, relative=False )
		

class GenericRecorder( object ):

	def __init__( self, seconds, fs=44100, numberOfChannels=1, sampleFormat='float32', start=True ):
		if isinstance( seconds, Sound ): self.sound = seconds
		else: self.sound = Sound( seconds, fs=fs, nchan=numberOfChannels )
		self._numberOfChannels = self.sound.NumberOfChannels()
		self._nextSample = 0
		self.recording = start
		self.__array_interface__ = dict( version=3, typestr=sampleFormat )
		
	def _InputCallback( self, t, inputData, frameCount ):
		if self.recording:
			self.__array_interface__[ 'data' ] = ( inputData.value, True )
			self.__array_interface__[ 'shape' ] =( frameCount, self._numberOfChannels )
			x = numpy.array( self )
			dst = self.sound.y[ self._nextSample:self._nextSample + frameCount, : ]
			dst.flat = x[ :dst.shape[ 0 ], : ].flat
			self._nextSample += dst.shape[ 0 ]
			if self._nextSample >= self.sound.y.shape[ 0 ]:
				self.recording = False
				self._nextSample = 0
		
	def Record( self, position=None, wait=True ):
		"""
		DOC-TODO
		"""
		if position is not None: self.Seek( position )
		self.recording = True
		if wait: self.Wait()
		
	def Pause( self, position=None ):
		"""
		DOC-TODO
		"""
		if position is not None: self.Seek( position )
		self.recording = False
	Stop = Pause
		
	def Wait( self ):
		"""
		DOC-TODO
		"""
		try: self.WaitFor( self )  # ownself wait for ownself lah!
		except KeyboardInterrupt: self.recording = False
	
	def WaitFor( self, func, finalRecordingStatus=None ):
		"""
		DOC-TODO
		"""
		if isinstance( func, GenericRecorder ):
			obj = func
			func = lambda: None if obj.recording else True
		if isinstance( func, GenericPlayer ):
			obj = func
			func = lambda: None if obj.playing else True
		if isinstance( func, str ):
			prompt = func
			try: from builtins import raw_input as ask # Python 2 (for some reason just referencing `raw_input` directly gave a NameError on Python 2.7.15 on linux...)
			except ImportError: ask = input # Python 3
			def func():
				try: return ask( prompt )
				except EOFError: print( '' ); return ''
		while func() is None:
			time.sleep( 0.001 )
		if finalRecordingStatus is not None:
			self.recording = finalRecordingStatus
		
	def Seek( self, position, relative=False ):
		"""
		DOC-TODO
		"""
		samples = int( round( self.sound.fs * position ) )
		if relative: self._nextSample = max( 0, self._nextSample + samples )
		else: self._nextSample = self.sound.NumberOfSamples() + samples if samples < 0 else samples
		return self
	
	@property
	def head( self ):
		return self._nextSample / self.sound.fs
	@head.setter
	def head( self, value ):
		self.Seek( value, relative=False )
		
	def Cut( self, position=None ):
		if position is None: position = self.head
		if position: self.sound = self.sound[ :float( position ) ]
		return self.sound

	@classmethod
	def MakeRecording( cls, space=60, stream=None, prompt='Recording for {duration:g} seconds - press return to finish early: ', verbose=None, cut=True ):
		r = cls( seconds=space, stream=stream, start=True, verbose=verbose )
		if prompt:
			if isinstance( prompt, str ): prompt = prompt.format( duration=r.sound.Duration() )
			r.WaitFor( prompt, finalRecordingStatus=False )
		else:
			if r.verbose: print( 'Recording for {duration:g} seconds - press ctrl + C to finish early'.format( duration=r.sound.Duration() ) )
			r.Wait()
		return r.Cut() if cut else r.sound

class Fader( object ):
	def __init__( self, duration=1.0, start=1, end=0, transform=None, pauseWhenDone='auto' ):
		self.t0 = None
		self.start = start
		self.end = end
		self.duration = duration
		self.transform = transform
		if pauseWhenDone == 'auto': pauseWhenDone = ( end == 0 )
		self.pauseWhenDone = pauseWhenDone
	def __call__( self, t ):
	 	if self.t0 is None: self.t0 = t
	 	t -= self.t0
	 	if t <= self.duration: value = self.start + ( self.end - self.start ) * t / self.duration
	 	elif self.pauseWhenDone: raise StopIteration( dict( playing=False ) )
	 	else: value = self.end 
	 	if self.transform: value = self.transform( value )
	 	return value
	 