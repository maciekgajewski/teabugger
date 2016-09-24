from . import sink

class StackFrame:

	def __init__(self, gdb):
		self.locals = {}
		self.gdb = gdb

	def update(self, frameInfo):
		#print('frame info=%s, depth=%d' % (frameInfo, depth))

		# analyse
		r, o = self.gdb.command('-stack-list-locals --all-values')
		locals = r['result']['locals']

		r, o = self.gdb.command('-stack-list-arguments --all-values 0 0')
		arguments = r['result']['stack-args'][0]['frame']['args']

		vars = arguments + locals

		print('vars=%s' % vars)

class Stack:

	def __init__(self, gdb):
		self.frames = []
		self.gdb = gdb

	def update(self, frameInfo, depth):
		# push
		if depth >= len(self.frames):
			while depth != len(self.frames)-1:
				self.push(frameInfo)
		# pop
		elif depth < len(self.frames)-1:
			while depth != len(self.frames)-1:
				self.pop()

		self.frames[-1].update(frameInfo)

	def push(self, frameInfo):
		sink.write('stack-push')
		frame = StackFrame(self.gdb)
		self.frames.append(frame)

	def pop(self):
		sink.write('stack-pop')
		self.frames.pop()