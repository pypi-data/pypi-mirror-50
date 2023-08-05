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

from . import Base;             from .Base             import *
from . import GenericInterface; from .GenericInterface import *
from . import IO;               from .IO               import *    # anything except an uncompressed .wav file requires AVbin
from . import Plotting;         from .Plotting         import *    # requires matplotlib
from . import BackEnd;          from .BackEnd          import *
from . import Meta;             from .Meta             import *
BackEnd.Load() # Loads the default back end, .PortAudioInterface