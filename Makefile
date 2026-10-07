CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -Wpedantic -O2 -g

.PHONY: all clean test
all: myshell
myshell: src/myshell.c
	$(CC) $(CFLAGS) $< -o $@
clean:
	rm -f myshell
test: myshell
	python3 tests/run_tests.py all
	python3 tests/test_trace_parser.py
