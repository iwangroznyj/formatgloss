Formatgloss
===========


## Description ##

The linguistic software Toolbox can produce interlinearised glosses of data
acquired during fieldwork.  However glosses containing combining diacritics are
often misaligned.

The present script scans text files for Toolbox glosses and realigns them
taking diacritics into consideration.  It comes with a command-line interface
as well as a graphical user interface.


## Requirements ##

 * This script requires at least Python 2.6 (but not Python 3!)
 * The graphical user interface requires wxPython


## Usage ##

The graphical user interface is started by running following script:

    formatgloss.pyw

The command-line interface is run with the `formatgloss_cli.py` script.  This
script takes two arguments:  The first determines the input file containing the
Toolbox glosses to be reformatted.  The second argument names the file to which
the reformatted glosses are to be saved.  This second argument is optional.  If
it is omitted, the reformatted text is printed out on standard output.

    formatgloss_cli.py input_file [output_file]


## License ##

Copyright (c) 2013 Johannes Englisch

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
