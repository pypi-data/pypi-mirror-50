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
audiomath is a package for manipulating sound waveforms. It allows you to:

- Represent sounds as `numpy` arrays, contained within instances of the `Sound`
  class. The methods and operator overloadings provided by the `Sound` class
  allow common operations to be performed with minimal coding---for example:
  slicing and concatenation in time, selection and stacking of channels,
  resampling, mixing, rescaling and modulation.
  
- Plot the resulting waveforms, via the third-party package `matplotlib`.
  
- Read and write uncompressed `.wav` files (via the Python standard library).

- Read other audio formats using the third-party AVbin library (binaries are
  included in the package, for a selection of platforms).

- Record and play back sounds using the third-party PortAudio library (binaries
  are included in the package, for a selection of platforms).

- Plug in other recording/playback back-ends with moderate development effort.
"""

#from . import DependencyManagement; DependencyManagement.Sabotage( 'numpy', 'matplotlib' ) # !!!! for debugging only
from . import Base;                 from .Base                 import *
from . import Functional;           from .Functional           import *
from . import GenericInterface;     from .GenericInterface     import *
from . import IO;                   from .IO                   import *    # anything except an uncompressed .wav file requires AVbin
from . import Graphics;             from .Graphics             import *    # requires matplotlib
from . import Meta;                 from .Meta                 import *
from . import BackEnd;              from .BackEnd              import *
from . import DependencyManagement; from .DependencyManagement import * 

from . import PortAudioInterface;   from .PortAudioInterface   import *    # we only do this as a concession to linting by PyCharm etc
BackEnd.Load()   # This is how back-ends are intended to be loaded. The default is .PortAudioInterface.  Others (as they are developed) won't be visible in PyCharm
