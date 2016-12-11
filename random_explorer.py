'''
The RandomExplorer class takes random actions for N trials on the chosen environment
and reports back the values it discovered for each state it explored. It calculates these values
by propagating the final reward at the end of each trial back over the states that led
to that reward, with the given discount. The final values stored in self.values are the average
values for each state over all trials in which that state was visited.
'''

import random

class RandomExplorer():
	def __init__(self, environment, discount, ntrials):
		self.env = environment
		self.discount = discount
		self.n = ntrials
		self.values = {}
		self.U = self.getValues
		self.vals = self.getValuesAsMap

	def explore(self):
		newvalues = {}
		for i in range(self.n):
			state = self.env.reset()
			totalreward = 0
			done = False
			explored = [state]
			while done == False:
				action = random.choice(self.env.action_space)
				next, reward, done = self.env.step(state, action)
				totalreward = totalreward + reward
				explored.append(next)
				state = next
			decay = 1
			for j in range(1, len(explored) + 1):
				curr = explored[len(explored)-j]
				newvalues[curr] = decay*totalreward
				decay = self.discount*decay
		for state in newvalues.keys():
			if self.values.has_key(state):
				self.values[state]['value'] = (self.values[state]['value'] + newvalues[state]) / (self.values[state]['visited'] + 1)
				self.values[state]['visited'] = self.values[state]['visited'] + 1
			else:
				self.values[state] = {'visited': 1, 'value': newvalues[state]}

	def getValues(self, state):
		if self.values.has_key(state):
			return self.values[state]['value']
		else:
			return None

	def getValuesAsMap(self):
		vals = {}
		for key in self.values.keys():
			vals[key] = self.values[key]['value']
		return vals