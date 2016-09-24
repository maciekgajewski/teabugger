from . import sink


class Variable:

	def __init__(self, gdb, name, value):
		self.gdb = gdb
		self.name = name
		self.value = value
		# create GDB object
		r, o = self.gdb.command('-var-create - * %s' % name)
		self.objname = r['result']['name']
		# get type
		r, o = self.gdb.command('-var-info-type %s' % self.objname)
		self.type = r['result']['type']
		# get addr
		r, o = self.gdb.command('-data-evaluate-expression &%s' % name)
		self.addr = int(r['result']['value'], 16)
		# get size
		r, o = self.gdb.command('-data-evaluate-expression sizeof(%s)' % name)
		self.size = int(r['result']['value'])

	def write(self, sink):
		sink.write({'variable': {'name': self.name, 'value' : self.value, 'size': self.size, 'addr': self.addr, 'type': self.type}})


class StackFrame:

	def __init__(self, gdb, frameInfo):
		self.locals = {}
		self.gdb = gdb

		# if not anonymous frame, get args, populate function name
		if frameInfo is not None:
			r, o = self.gdb.command('-stack-list-arguments --all-values 0 0')
			arguments = r['result']['stack-args'][0]['frame']['args']

			for a in arguments:
				name = a['name']
				var = Variable(self.gdb, name, a['value'])
				self.locals[name] = var

			# build function name
			argtypes = [self.locals[a['name']].type for a in arguments]
			fname='%s(%s)' % (frameInfo['func'], ','.join(argtypes))
			addr = int(frameInfo['addr'], 16)
			sink.write({'stack': 'push', 'func' : fname, 'addr' : addr})

			# report args
			for v in self.locals.values():
				v.write(sink)
		else:
			sink.write({'stack':'push'})


	def update(self, frameInfo):
		# analyse
		r, o = self.gdb.command('-stack-list-locals --all-values')
		locals = r['result']['locals']
		for l in locals:
			name = l['name']
			if name not in self.locals:
				v = Variable(self.gdb, name, l['value'])
				self.locals[name] = v
				v.write(sink)

class Stack:

	def __init__(self, gdb):
		self.frames = []
		self.gdb = gdb

	def update(self, frameInfo, depth):
		# push
		if depth > len(self.frames)-1:
			while depth > len(self.frames):
				self.push(None)
			self.push(frameInfo)
		# pop
		elif depth < len(self.frames)-1:
			while depth < len(self.frames)-1:
				self.pop()

		self.frames[-1].update(frameInfo)

	def push(self, frameInfo):
		frame = StackFrame(self.gdb, frameInfo)
		self.frames.append(frame)

	def pop(self):
		sink.write({'stack' : 'pop'})
		self.frames.pop()