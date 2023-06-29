""""
TODO
rename commands
move all repeatable logic into functions
rewrite in C
get EOF for input

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

not implemented commands:
	dDrc
"""

from sys import argv, stdin
import operator
from typing import Callable

in_ptr: int = 0
input_str = ""
stacks: dict[str,list[int]] = {
	'\"': [],	# default stack
}

def noop():
	pass
ops: dict[str,tuple[Callable,int]] = {
	'+': (operator.add,2),
	'-': (operator.sub,2),
	'*': (operator.mul,2),
	'/': (operator.truediv,2),
	'o': (chr,1),
	'O': (int,1),
	'p': (lambda stack:stacks[stack][-1],2),
	'P': (lambda stack:stacks[stack].pop(),2),
	'i': (noop, 0),
	'w': (noop, 1),
	'W': (noop, 1),
	'f': (noop, 1),
	'F': (noop, 0),
	'g': (noop, 1),
	'#': (noop, 1),
}

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
			jumps[jump] = i
		i += ops[c][1]+1
	return s

def stack_push(stack,num):
	if stack not in stacks:
		stacks[stack] = []
	stacks[stack].append(num)

def expr_eval(expr: str):
	if expr not in "0123456789":
		out = int(stacks[expr].pop())
	else:
		out = int(expr)
	return out

if __name__ == "__main__":
	if len(argv) > 1:
		with open(argv[1]) as f:
			s = f.read()[:-1]
	else:
		s = input()
	
		
	s = parse(s)

	while in_ptr < len(s):
		c = s[in_ptr]
		# print(s[in_ptr:in_ptr+ops[c][1]+1], stacks)
		match c:
			# operators
			case c if c in "+-*/":
				stacks['\"'].append(ops[c][0](expr_eval(s[in_ptr+1]),expr_eval(s[in_ptr+2])))

			# stack operations
			case c if c in "pP":
				stack_push(s[in_ptr+2], ops[c][0](s[in_ptr+1]))

			# output
			case c if c in "oO":
				print(ops[c][0](expr_eval(s[in_ptr+1])), end="")

			# input
			case 'i':
				if input_str == "":
					input_str = stdin.readline()
				if input_str != "":
					stack_push('\"', ord(input_str[0]))
					input_str = input_str[1:]
				else:
					stack_push('\"', 0)

			# while loops, and if
			case c if c in 'wf':
				if expr_eval(s[in_ptr+1]) == 0:
					in_ptr = jumps[in_ptr]
			case 'W':
				if expr_eval(s[in_ptr+1]) != 0:
					in_ptr = jumps[in_ptr]

			case 'g':
				in_ptr = expr_eval(s[in_ptr+1])

			# end program
			case 'q':
				break

			# noop
			case c if c in 'F':
				pass
			case '#':
				pass

			case _:
				print(f"unknown command {ord(c)} {c}")
				exit(1)

		in_ptr += ops[c][1]+1
