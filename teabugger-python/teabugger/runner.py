from . import gdb as _gdb

def runBinary(binary, output):
	print("Hello, running %s" % binary, file=output)

	gdb = _gdb.Gdb(binary)
	r,o = gdb.command('-break-insert main')
	print('result: %s' % r)
	
