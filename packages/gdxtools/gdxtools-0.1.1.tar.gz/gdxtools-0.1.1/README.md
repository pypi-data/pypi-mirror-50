# gdxrw
gdxrw contains two classes (gdx_reader and gdx_writer) that enable rapid read and write operations of GAMS GDX files.  These 'helper' classes will allow the user to interface with the GAMS python API through a more intuitive interface (enabled by python dicts).

# Use
The example file that is included here shows how these classes are utilizied in reading from the 'transport_out.gdx' file with 'gdx_reader'. The example file also includes an implementation of 'gdx_writer' that creates 'transport_out_chk.gdx'.  The user can use the GAMS utility 'gdxdiff' to view the differences between the original GDX file and the newly created check GDX file.  At this time gdxrw does not write equations or variables into a GDX file (but it will read)... this functionality might be added later on.

# Requirements
Python 3, GAMS API
