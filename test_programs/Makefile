all: out/push_back.debug out/push_back.rwdi

out/push_back.debug: push_back.cc
	mkdir -p out
	g++ -o -O0 -g -o out/push_back.debug push_back.cc

out/push_back.rwdi: push_back.cc
	mkdir -p out
	g++ -o -O2 -g -o out/push_back.rwdi push_back.cc