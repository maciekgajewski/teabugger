from subprocess import Popen, PIPE


class Gdb:
	"""GDB Session"""

	def __init__(self, binary):
		"""Creates GDB session on binary"""

		print("Created GDB session")

		args=['gdb', '--interpreter=mi', binary]
		self.process = Popen(args, stdin=PIPE, stdout=PIPE)

		self.read()

	def read(self):
		""" Read all input from the debugger """
		for line in self.process.stdout:
			print("read line: %s" % line)



