#!/usr/bin/bash
if ! ./main.py fibonacci | grep -i "^0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181 $" > /dev/null; then
	echo "fibonacci wrong"
fi
if ! ./main.py hello_world | grep -i "^Hello World!$" > /dev/null; then
	echo "hello_world wrong"
fi
if ! echo "this is a cat program" | ./main.py cat | grep -i "^this is a cat program$" > /dev/null; then
	echo "cat wrong"
fi
if ! echo "1" | timeout 1s ./main.py truthmachine | grep -i "11" > /dev/null; then
	echo "truthmachine wrong"
fi
