from subprocess import Popen, PIPE


class Gdb:
	"""GDB Session"""

	def __init__(self, binary):
		"""Creates GDB session on binary"""

		print("Created GDB session")

		args=['gdb', '--interpreter=mi', binary]
		self.process = Popen(args, stdin=PIPE, stdout=PIPE, universal_newlines=True)

		self.read()

	def read(self):
		""" Read all input from the debugger """
		for line in self.process.stdout:
			stripped = line.strip() # TODO must a clever, pythonish way to do it in the for statemen
			
			if stripped == '(gdb)':
				return
			self.processLine(stripped)

	def processLine(self, line):
		type = line[0]
		text = line[1:]

		print('type=%s, text=%s' % (type, text))


