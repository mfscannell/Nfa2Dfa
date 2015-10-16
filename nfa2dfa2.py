#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#	Gehrig Keane
#	2727430
#	665: Project 1
#	NFA to DFA conversion
#	Functional Line Count = 85
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from sets import Set
from collections import deque
import copy

# nfa_states:
#	[0]	-> index
#	[1]	-> a set
#	[2]	-> b set
#	[3]	-> E set

dfa_headers, dfa_moves = [], []
unmarked_states = deque()
dfa_state = 1;

def E_closure(states, s, i):
	closure = copy.deepcopy(s)
	temp = copy.deepcopy(closure)
	q = deque()
	#Push initial E states into queue
	for x in closure:
		var = int(temp.pop())
		q.append(var)
	while len(q) != 0:
		tmp = q.popleft()
		#Get states[i] for queued current state
		tmp_state = states[int(tmp)-1];
		#Gather said states E values and modify the queue
		#	access queued state at [3] -> E values
		for x in tmp_state[3]:
			if int(x) != 0:
				closure.add(x)
				q.append(int(x))
	if i != "0":
		closure.update(str(i))
	return closure

def print_set(s, pre, post):
	print (str(pre) + '{' + ','.join(sorted(copy.deepcopy(s), key=int)) + '}' + str(post))

def gss(s, pre = "", post = ""):
	return str(str(pre) + '{' + ','.join(sorted(copy.deepcopy(s), key=int)) + '}' + str(post))

#	states = list of all states
#	s = set of states to move on
#	i = indicie for a or b position (line 53)
def move(states, s, i):
	move_set = Set()
	for e in s:
		temp = states[int(e)-1]
		for f in temp[i]:
			if int(f) != 0:
				move_set.add(f)
	return move_set

ini_states = raw_input("\nInitial State: ")
fin_states = raw_input("\nFinal States: ")
tot_states = int(raw_input("\nTotal States: "))

print ("\nState\ta\tb\tE"),
nfa_states = [str(i+1)+"\t"+raw_input("\n"+str(i+1)+"\t") for i in range(tot_states)]
nfa_states = [x.replace("{}", "0").replace("{", "").replace("}", "").split("\t") for x in nfa_states]
nfa_states = [[Set(s[x].split(',')) if x > 0 else int(s[x]) for x in range(len(s))] for s in nfa_states]

# Calculate the E-closure for the initial state
closure = E_closure(nfa_states, nfa_states[0][3], nfa_states[0][0])
print_set(closure,"\nE-closure(IO) = "," = " + str(dfa_state))
# Mark first state
dfa_headers.append(closure)
unmarked_states.append(closure)
i = 1
while len(unmarked_states) != 0:
	temp = unmarked_states.popleft()
	temp_move = [0,0]
	print ("\nMark " + str(i))
	i += 1

	temp_a = move(nfa_states, temp, 1)
	temp_a_clos = E_closure(nfa_states, temp_a, "0")
	if len(temp_a_clos) != 0:
		if temp_a_clos not in dfa_headers:
			dfa_headers.append(temp_a_clos)
			unmarked_states.append(temp_a_clos)
			dfa_state += 1
		temp_move[0] = dfa_state
		print_set(temp, '', ' --a--> ' + gss(temp_a))
		print ("E-closure" + gss(temp_a) + " = " + gss(temp_a_clos) + " = " + str(dfa_state))

	temp_b = move(nfa_states, temp, 2)
	temp_b_clos = E_closure(nfa_states, temp_b, "0")
	if len(temp_b_clos) != 0:
		if temp_b_clos not in dfa_headers:
			dfa_headers.append(temp_b_clos)
			unmarked_states.append(temp_b_clos)
			dfa_state += 1
		temp_move[1] = dfa_state
		print_set(temp, '', ' --b--> ' + gss(temp_b))
		print ("E-closure" + gss(temp_b) + " = " + gss(temp_b_clos) + " = " + str(dfa_state))
	dfa_moves.append(temp_move)

print ("\n" + str(dfa_headers))
print ("\nInitial State: ")
print ("Final States: ")
print ("State\ta\tb")
dfa_moves = [['' if int(x)==0 else x for x in i] for i in dfa_moves]
for i in range(len(dfa_headers)):
	print (str(i+1) + "\t{" + str(dfa_moves[i][0]) + "}\t{" + str(dfa_moves[i][1]) + "}")
