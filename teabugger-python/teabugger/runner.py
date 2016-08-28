from . import gdb as _gdb
import os

def waitForStopped(gdb):
	records = gdb.read()
	for r in records:
		if r['type'] == '*' and r['class'] == 'stopped':
			return
	
	assert False

def runBinary(binary, output):
	print("Hello, running %s" % binary, file=output)

	gdb = _gdb.Gdb(binary)
	
	# set breakpoit at the beginning of main, get the source dir and file name
	r,o = gdb.command('-break-insert main')
	
	mainFile = r['result']['bkpt']['fullname']
	sourceDir = os.path.dirname(mainFile)
	
	print('source dir: %s' % sourceDir)
	
	# start program
	gdb.command('-exec-run')
	
	# wait for breakpoint hit
	waitForStopped(gdb)
	
	# get frame, line info
	# TODO	
