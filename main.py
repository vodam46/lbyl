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

def stack_push(num,stack): # expr: str
	if stack not in stacks: # expr[0]
		stacks[stack] = []
	stacks[stack].append(num)

def expr_eval(expr: str):
	if expr[1] not in "0123456789":
		out = int(stacks[expr[1]].pop())
	else:
		out = int(expr[1])
	return out

def input_func(expr: str):
	global input_str
	if input_str == "":
		input_str = stdin.readline()
	if input_str != "":
		stacks["\""].append(ord(input_str[0]))
		input_str = input_str[1:]
	else:
		stacks["\""].append(0)

def goto(expr: str):
	global in_ptr
	in_ptr = expr_eval(expr)

ops: dict[str,tuple[Callable,int]] = {
	'+': (operator.add,2),
	'-': (operator.sub,2),
	'*': (operator.mul,2),
	'/': (operator.truediv,2),
	'o': (lambda expr: print(chr(expr_eval(expr)),end=""),1),
	'O': (lambda expr: print(int(expr_eval(expr)),end=""),1),
	'p': (lambda expr:stacks[expr[0]][-1],2),
	'P': (lambda expr:stacks[expr[0]].pop(),2),
	'i': (input_func, 0),
	'w': (noop, 1),
	'W': (noop, 1),
	'f': (noop, 1),
	'F': (noop, 0),
	'g': (goto, 1),
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
				stacks['\"'].append(ops[c][0](expr_eval(pars),expr_eval(pars[::2])))

			# stack operations
			case c if c in "pP":
				stack_push(ops[c][0](s[in_ptr+1]), s[in_ptr+2])
				# ops[c][0](pars)

			# oO - output
			# i - input
			# F - endif
			# . comment
			case c if c in "ioOF.g":
				ops[c][0](pars)

			# while loops, and if
			case c if c in 'wf':
				if expr_eval(pars) == 0:
					in_ptr = jumps[in_ptr]+1
			case 'W':
				if expr_eval(pars) != 0:
					in_ptr = jumps[in_ptr]-ops[c][1]-1

			# end program
			case 'q':
				break

			case _:
				print(f"unknown command {ord(c)} {c}")
				exit(1)

		in_ptr += ops[c][1]+1
