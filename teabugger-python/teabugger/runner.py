from . import gdb as _gdb

def runBinary(binary, output):
	print("Hello, running %s" % binary, file=output)

	gdb = _gdb.Gdb()

	
