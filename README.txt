Prerequsites:
 - Python 2.x (tested with 2.7)
 - Graphviz ('dot' should be in your path, but for Windows users, if it's in
   'C:\Program Files (x86)\Graphviz 2.28\bin', envsetup.bat will add it)

Included prerequsites:
 - pyparsing library
 - pydot library

Unzip somewhere. Open a shell and 'cd' to the project root. (The envsetup
scripts won't work if run from a different location! Be careful!)

In a Unix shell, run 'source envsetup.sh'. In Windows cmd, run
'envsetup.bat'. (This tells Python to use the included copies of pyparsing
and pydot. For Windows users, it also adds a possible path for Python and Dot
to your PATH. This step is optional if, uh, it's not needed. :-))

Run 'python src/dot-svg.py -o <file.html> <file.dot>'.
