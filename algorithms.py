import time

def localApproximationValueIteration(env, values, discount, cutoff):
	done = False
	t = 0
	starttime = time.time()
	overalldistance = [0 for x in values.keys()[0]]
	count = 0
	while done == False and t < cutoff:
		newvalues = {}
		changed = False
		state_i = 0
		for state in env.state_space:
			state_i = state_i + 1
			if state_i % 100 == 0 and t == 0:
				print ".",
			vals = []
			for action in env.action_space:
				total = env.R(state, action)
				nextStates = env.next(state, action)
				for nextState in nextStates:
					neighbor = nearestNeighbor(nextState, values)
					if neighbor != nextState:
						count = count + 1
						for i in range(len(neighbor)):
							overalldistance[i] = overalldistance[i] + abs(neighbor[i]-nextState[i])
					total = total + discount*env.T(state, action, nextState)*values[neighbor]
				vals.append(total)
			newvalues[state] = max(vals)
			if values.has_key(state) == False or values[state] != newvalues[state]:
				changed = True
		if changed == False:
			done = True
		values = newvalues
		t = t + 1
		if t != 0:
			print ".",
	print "Took", time.time() - starttime, "to run", t, "iterations"
	print "Avg distance between value and found neighbor:", [float(x)/count for x in overalldistance]
	return values

def nearestNeighbor(state, values):
	if values.has_key(state):
		return state
	states = values.keys()
	return min(states, key=lambda x: reduce(lambda y, z: y + abs(x[z] - state[z]), range(len(state)), 0))

def policy(env, values, discount):
	pol = {}
	for state in env.state_space:
		actionValues = [0 for action in env.action_space]
		for action in env.action_space:
			actionValues[action] = env.R(state, action)
			nextStates = env.next(state, action)
			for next in nextStates:
				if values.has_key(next):
					actionValues[action] = actionValues[action] + discount*env.T(state, action, next)*values[next]
		pol[state] = actionValues.index(max(actionValues))
	return pol