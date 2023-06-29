#!/usr/bin/env python
""""
TODO
rename commands
move all repeatable logic into functions
- expr as function input
rewrite in C
get EOF for input
fix while loops
typehint everything
test script

unified design choices
 - always pop


implemented commands:
	pP
	oO
	i
	+-*/
	n
	q
	wW
	fF
	g
	.

not implemented commands:
	dDrc
"""

from sys import argv, stdin
import operator
from typing import Callable

in_ptr: int = 0
input_str: str = ""
stacks: dict[str,list[int]] = {
	'\"': [],	# default stack
}

def noop():
	pass

jumps: dict[int,int] = {}

def parse(s):
	s = ''.join(c for c in s if c not in  " \n\t")

	while_arr = []
	if_arr = []
	i = 0
	while i < len(s):
		c = s[i]
		if c == 'w':
			while_arr.append(i)
		elif c == 'W':
			jump = while_arr.pop()
			jumps[jump] = i
			jumps[i] = jump
		elif c == 'f':
			if_arr.append(i)
		elif c == 'F':
			jump = if_arr.pop()
			jumps[jump] = i-1
		i += ops[c][1]+1
	return s

def stack_push(stack,num): # expr: str
	if stack not in stacks: # expr[0]
		stacks[stack] = []
	stacks[stack].append(num)

def expr_eval(expr: str):
	if expr not in "0123456789":
		out = int(stacks[expr].pop())
	else:
		out = int(expr)
	return out

def input_func(expr: str):
	global input_str
	if input_str == "":
		input_str = stdin.readline()
	if input_str != "":
		stack_push('\"', ord(input_str[0]))
		input_str = input_str[1:]
	else:
		stack_push('\"', 0)

ops: dict[str,tuple[Callable,int]] = {
	'+': (operator.add,2),
	'-': (operator.sub,2),
	'*': (operator.mul,2),
	'/': (operator.truediv,2),
	'o': (lambda expr: print(chr(expr_eval(expr[1])),end=""),1),
	'O': (lambda expr: print(int(expr_eval(expr[1])),end=""),1),
	'p': (lambda stack:stacks[stack][-1],2),
	'P': (lambda stack:stacks[stack].pop(),2),
	'i': (input_func, 0),
	'w': (noop, 1),
	'W': (noop, 1),
	'f': (noop, 1),
	'F': (noop, 0),
	'g': (noop, 1),
	'.': (noop, 1),
}

if __name__ == "__main__":
	if len(argv) > 1:
		with open(argv[1]) as f:
			s = f.read()[:-1]
	else:
		s = input()
	
		
	s = parse(s)
	if "-d" in argv:
		print(s)

	while in_ptr < len(s):
		c = s[in_ptr]
		pars = s[in_ptr:in_ptr+ops[c][1]+1]
		if "-d" in argv:
			print(c,pars,stacks,in_ptr)
		match c:
			# operators
			case c if c in "+-*/":
				stacks['\"'].append(ops[c][0](expr_eval(s[in_ptr+1]),expr_eval(s[in_ptr+2])))

			# stack operations
			case c if c in "pP":
				stack_push(s[in_ptr+2], ops[c][0](s[in_ptr+1]))

			# oO - output
			# i - input
			# F - endif
			# . comment
			case c if c in "ioOF.":
				ops[c][0](pars)

			# while loops, and if
			case c if c in 'wf':
				if expr_eval(s[in_ptr+1]) == 0:
					in_ptr = jumps[in_ptr]+1
			case 'W':
				if expr_eval(s[in_ptr+1]) != 0:
					in_ptr = jumps[in_ptr]-ops[c][1]-1

			case 'g':
				in_ptr = expr_eval(s[in_ptr+1])

			# end program
			case 'q':
				break

			case _:
				print(f"unknown command {ord(c)} {c}")
				exit(1)

		in_ptr += ops[c][1]+1
