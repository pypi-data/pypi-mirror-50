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
	'PORTAUDIO', 'SetDefaultVerbosity', 
	'GetHostApiInfo', 'GetDeviceInfo', 'FindDevice', 'FindDevices',
	'GetOutputDevice', 'SetOutputDevice', 'Player',
	'GetInputDevice',  'SetInputDevice',  'Recorder', 'Record',
]

from . import GenericInterface

from . import _wrap_portaudio; from ._wrap_portaudio import PORTAUDIO, SetDefaultVerbosity, GetHostApiInfo, GetDeviceInfo, FindDevice, FindDevices, Stream

SINGLE_OUTPUT_STREAM = True   # seems to need to be True on Windows
DEFAULT_OUTPUT_DEVICE = None
def SetOutputDevice( device ):
	global DEFAULT_OUTPUT_DEVICE
	DEFAULT_OUTPUT_DEVICE = FindDevice( id=device, returnAll=False )[ 'index' ]
	
def GetOutputDevice():
	device = DEFAULT_OUTPUT_DEVICE
	if device is None: return None
	return FindDevice( id=device, returnAll=False )

SINGLE_INPUT_STREAM = True
DEFAULT_INPUT_DEVICE = None
def SetInputDevice( device ):
	global DEFAULT_INPUT_DEVICE
	DEFAULT_INPUT_DEVICE = FindDevice( id=device, returnAll=False )[ 'index' ]
	
def GetInputDevice():
	device = DEFAULT_INPUT_DEVICE
	if device is None: return None
	return FindDevice( id=device, returnAll=False )
	

class Player( GenericInterface.GenericPlayer ):
	__stream = __verbose = None
	def __init__( self, sound, resample=False, stream=None, verbose=None ):
		self.__stream = None
		self.__verbose = verbose
		if self.verbose: print( '%r is being initialized' % self )
		super( Player, self ).__init__( sound=sound )
		global SINGLE_OUTPUT_STREAM, DEFAULT_OUTPUT_DEVICE
		if stream is None: stream = DEFAULT_OUTPUT_DEVICE
		if SINGLE_OUTPUT_STREAM:
			alreadyInitialized = isinstance( SINGLE_OUTPUT_STREAM, Stream )
			mode = 'oo' if stream is None else None
			if not isinstance( stream, Stream ):
				stream = FindDevice( id=stream, mode=mode )[ 'index' ]
				if alreadyInitialized and stream == SINGLE_OUTPUT_STREAM.outputDevice[ 'index' ]: stream = SINGLE_OUTPUT_STREAM
				else: stream = Stream( device=stream, sound=self.sound )
			#if alreadyInitialized and stream and stream is not SINGLE_OUTPUT_STREAM: raise RuntimeError( 'cannot create multiple Streams' )
			self.__stream = stream if stream else SINGLE_OUTPUT_STREAM if alreadyInitialized else Stream( sound=self.sound )
			if not alreadyInitialized: SINGLE_OUTPUT_STREAM = self.__stream
			if not DEFAULT_OUTPUT_DEVICE: DEFAULT_OUTPUT_DEVICE = self.__stream.outputDevice[ 'index' ]
		else:
			if stream is None: stream = DEFAULT_OUTPUT_DEVICE
			self.__stream = stream if isinstance( stream, Stream ) else Stream( device=stream, sound=self.sound )
		soundFs = self.sound.fs
		streamFs = self.__stream.fs
		if soundFs != streamFs:
			if resample:
				if self.verbose: print( '%r is resampling its sound from %g to %g Hz' % ( self, soundFs, streamFs ) )
				self.sound = self.sound.Resample( streamFs )
			else:
				factor = self._sampleRateEqualizationFactor = soundFs / streamFs
				if self.verbose: print( '%r will play at %g * nominal speed to match stream rate of %g Hz' % ( self, factor, streamFs ) )
					
		self.__stream._AddOutputCallback( self._OutputCallback )

	@property
	def stream( self ):
		return self.__stream

	@property
	def verbose( self ):
		if self.__verbose is not None: return self.__verbose
		return self.__stream.verbose if self.__stream else False
	@verbose.setter
	def verbose( self, value ):
		self.__verbose = value
	
	def __del__( self ):
		if self.verbose: print( '%r is being deleted' % self )
		self.Pause()
		global SINGLE_OUTPUT_STREAM
		if self.__stream is SINGLE_OUTPUT_STREAM:
			if SINGLE_OUTPUT_STREAM._RemoveOutputCallback( self ) == 0: # if nobody is using it any more,
				SINGLE_OUTPUT_STREAM = True # let the global Stream instance get garbage-collected
		self.__stream = None


class Recorder( GenericInterface.GenericRecorder ):
	__stream = __verbose = None
	def __init__( self, seconds, stream=None, start=True, verbose=None ):
		self.__stream = None
		self.__verbose = verbose
		if self.verbose: print( '%r is being initialized' % self )
		global SINGLE_INPUT_STREAM, DEFAULT_INPUT_DEVICE
		if stream is None: stream = DEFAULT_INPUT_DEVICE
		if SINGLE_INPUT_STREAM:
			alreadyInitialized = isinstance( SINGLE_INPUT_STREAM, Stream )
			if not isinstance( stream, Stream ):
				stream = FindDevice( id=stream, mode='i' if stream is None else None )[ 'index' ]
				if alreadyInitialized and stream == SINGLE_INPUT_STREAM.inputDevice[ 'index' ]: stream = SINGLE_INPUT_STREAM
				else: stream = Stream( device=stream, mode='i' )
			#if alreadyInitialized and stream and stream is not SINGLE_INPUT_STREAM: raise RuntimeError( 'cannot create multiple Streams' )
			self.__stream = stream if stream else SINGLE_INPUT_STREAM if alreadyInitialized else Stream( mode='i' )
			if not alreadyInitialized: SINGLE_INPUT_STREAM = self.__stream
		else:
			if stream is None: stream = DEFAULT_INPUT_DEVICE
			self.__stream = stream if isinstance( stream, Stream ) else Stream( device=stream, mode='i' )
		if not DEFAULT_INPUT_DEVICE: DEFAULT_INPUT_DEVICE = self.__stream.inputDevice[ 'index' ]
			
		stream = self.__stream
		super( Recorder, self ).__init__( seconds=seconds, fs=stream.fs, numberOfChannels=stream.nInputChannels, sampleFormat=stream.sampleFormat[ 'numpy' ], start=start )
		
		self.__stream._AddInputCallback( self._InputCallback )

	@property
	def stream( self ):
		return self.__stream
		
	@property
	def verbose( self ):
		if self.__verbose is not None: return self.__verbose
		return self.__stream.verbose if self.__stream else False
	@verbose.setter
	def verbose( self, value ):
		self.__verbose = value
	
	def __del__( self ):
		if self.verbose: print( '%r is being deleted' % self )
		self.Pause()
		global SINGLE_INPUT_STREAM
		if self.__stream is SINGLE_INPUT_STREAM:
			if SINGLE_INPUT_STREAM._RemoveInputCallback( self ) == 0: # if nobody is using it any more,
				SINGLE_INPUT_STREAM = True # let the global Stream instance get garbage-collected
		self.__stream = None


Record = Recorder.MakeRecording