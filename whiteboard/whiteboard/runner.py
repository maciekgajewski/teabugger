from . import gdb as _gdb
from . import sink
import os


class Functions:

	def __init__(self):
		self.functions = []
	
	def findByName(self, name):
		for f in self.functions:
			if f['name'] == name:
				return f
	
	def update(self, frameInfo):
		f = self.findByName(frameInfo['func'])
		if f is None:
			# new function!
			f = {'name' : frameInfo['func'], 'addr' : frameInfo['addr']}
			self.functions.append(f)
			sink.write({'function' : f})


def waitForStopped(gdb):
	records = gdb.read()
	for r in records:
		#print(r)
		if r['type'] == '*' and r['class'] == 'stopped':
			return
	
	assert False

def runBinary(binary, output):
	print("Hello, running %s" % binary, file=output)

	gdb = _gdb.Gdb(binary)
	functions = Functions()
	
	# some config
	gdb.command('set backtrace past-main on')
	
	# set breakpoit at the beginning of main, get the source dir and file name
	r,o = gdb.command('-break-insert main')
	
	mainFile = r['result']['bkpt']['fullname']
	sourceDir = os.path.dirname(mainFile)
	
	print('source dir: %s' % sourceDir)
	
	# start program
	gdb.command('-exec-run')
	waitForStopped(gdb)

	r, o = gdb.command('-stack-info-depth')
	print(r)
	mainDepth = int(r['result']['depth'])
	print('main depth: %d' % mainDepth)
	
	lastDepth = mainDepth
	
	while True:
		# get frame, line info
		r, o = gdb.command('-stack-info-frame')
		#print(r)
		frameInfo = r['result']['frame']
		
		r, o = gdb.command('-stack-info-depth')
		depth = int(r['result']['depth'])
		
		# detect main exit
		if depth < mainDepth:
			break
		
			
		# is this in our source?
		if os.path.commonprefix([sourceDir, frameInfo['fullname']]) == sourceDir:

			functions.update(frameInfo)

			# analyse
			r, o = gdb.command('-stack-list-locals --all-values')
			locals = r['result']['locals']
			
			r, o = gdb.command('-stack-list-arguments --all-values 0 0')
			arguments = r['result']['stack-args'][0]['frame']['args']
			
			#print('>> args: %s' % arguments)
			#print('>> locals: %s' % locals)
			sink.write({'frame': {'depth' : depth, 'locals' : locals, 'arguments': arguments}})
			sink.write({'location': {'file' : frameInfo['fullname'], 'line' : frameInfo['line']}})
	
		gdb.command('-exec-step')
		waitForStopped(gdb)
	
