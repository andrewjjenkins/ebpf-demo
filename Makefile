
all: what

what: what.c
	gcc -Wall -Werror what.c -o what -lm

clean:
	rm -f what

.PHONY: all what
