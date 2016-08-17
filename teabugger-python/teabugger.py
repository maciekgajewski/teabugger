#!/usr/bin/env python3

import sys
import teabugger

if len(sys.argv) < 2:
	print("Usage: teabuger <BINARY>")
	sys.exit(1)

binary = sys.argv[1]

teabugger.runBinary(binary, sys.stdout)
