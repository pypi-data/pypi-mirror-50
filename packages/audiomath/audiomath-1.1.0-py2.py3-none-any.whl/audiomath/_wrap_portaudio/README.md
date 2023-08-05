Libraries built from sources obtained at http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz
via http://www.portaudio.com/download.html

On Linux (Ubuntu 18.04 LTS), ALSA was installed first::
	
	sudo apt install libasound-dev

Then the standard combo worked::
	
	./configure
	make

producing the dynamic library inside `lib/.libs/`

On macOS (10.13, High Sierra, 2017)::

	./configure --disable-mac-universal
	make

the `--disable-mac-universal` was necessary in order to work around two errors from
`./configure`::

	xcode-select: error: tool 'xcodebuild' requires Xcode, but active developer directory '/Library/Developer/CommandLineTools' is a command line tools instance
	configure: error: Could not find 10.5 to 10.12 SDK.

(although the first one could presumably be worked-around by biting the bullet and
installing full-blown XCode, and the second has other suggested workarounds at
https://github.com/VCVRack/Rack/issues/144 )

For Windows the procedure is documented at https://github.com/VCVRack/Rack/issues/144
(TODO: don't remember whether or not that worked out-of-the-box for me).


PortAudio Credits and License
=============================

Here is the PortAudio license V19 as retrieved on 20190801 from 
http://www.portaudio.com/license.html

PortAudio Portable Real-Time Audio Library
Copyright (c) 1999-2011 Ross Bencina and Phil Burk

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the 
Software without restriction, including without limitation the rights to use, copy, 
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the 
following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT.

IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES 
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
