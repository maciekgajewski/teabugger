#!/usr/bin/env python3

import sys
import whiteboard

if len(sys.argv) < 2:
	print("Usage: whiteboard <BINARY>")
	sys.exit(1)

binary = sys.argv[1]

whiteboard.runBinary(binary, sys.stdout)
