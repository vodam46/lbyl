#!/usr/bin/env python
""""
TODO
rename commands
rewrite in C (?)
typehint everything

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
from typing import Callable

in_ptr: int = 0
input_str: str = ""
stacks: dict[str,list[int]] = {
	'\"': [],	# default stack
}

def noop(expr:str) -> None:
	pass

jumps: dict[int,int] = {}

def parse(s: str) -> str:
	s = ''.join(c for c in s if c not in  " \n\t")

	while_arr: list[int] = []
	if_arr: list[int] = []
	i: int = 0
	jump: int = 0
	while i < len(s):
		c: str = s[i]
		if c == 'w':
			while_arr.append(i)
		elif c == 'W':
			jump = while_arr.pop()
			jumps[jump] = i
			jumps[i] = jump - ops[c][1]-1
		elif c == 'f':
			if_arr.append(i)
		elif c == 'F':
			jump = if_arr.pop()
			jumps[jump] = i-1
		i += ops[c][1]+1
	return s

def stack_push(num: int,stack: str):
	if stack not in stacks:
		stacks[stack] = [num]
		return
	stacks[stack].append(num)

def expr_eval(expr: str):
	if "-d" in argv:
		print("expr:",expr)
	if expr in "0123456789":
		out = int(expr)
	else:
		out = int(stacks[expr].pop())
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

def cond_jump(cond, expr):
	global in_ptr
	if cond(expr_eval(expr[1])):
		in_ptr = jumps[in_ptr]

def goto(expr: str):
	global in_ptr
	in_ptr = expr_eval(expr[1])

ops: dict[str,tuple[Callable[[str],None],int]] = {
	'+': (lambda expr: stacks['\"'].append(expr_eval(expr[1])+expr_eval(expr[2])),2),
	'-': (lambda expr: stacks['\"'].append(expr_eval(expr[1])-expr_eval(expr[2])),2),
	'*': (lambda expr: stacks['\"'].append(expr_eval(expr[1])*expr_eval(expr[2])),2),
	'/': (lambda expr: stacks['\"'].append(int(expr_eval(expr[1])/expr_eval(expr[2]))),2),
	'o': (lambda expr: print(chr(expr_eval(expr[1])),end=""),1),
	'O': (lambda expr: print(int(expr_eval(expr[1])),end=""),1),
	'p': (lambda expr: stack_push(stacks[expr[1]][-1],expr[2]),2),
	'P': (lambda expr: stack_push(stacks[expr[1]].pop(),expr[2]),2),
	'i': (input_func, 0),
	'w': (lambda expr: cond_jump(lambda e:e==0,expr), 1),
	'W': (lambda expr: cond_jump(lambda e:e!=0,expr), 1),
	'f': (lambda expr: cond_jump(lambda e:e==0,expr), 1),
	'F': (noop, 0),
	'g': (goto, 1),
	'.': (noop, 1),
	'q': (lambda expr: exit(0), 0),
}

if __name__ == "__main__":
	s: str = ""
	if len(argv) > 1:
		with open(argv[1]) as f:
			s = f.read()[:-1]
	else:
		s = input()
	
		
	s = parse(s)
	if "-d" in argv:
		print(s)

	while in_ptr < len(s):
		c: str = s[in_ptr]
		pars: str = s[in_ptr:in_ptr+ops[c][1]+1]
		if "-d" in argv:
			print(c,pars,stacks,in_ptr)
		if c in ops:
			ops[c][0](pars)

		else:
			print(f"unknown command {ord(c)} {c}")
			exit(1)

		in_ptr += ops[c][1]+1
