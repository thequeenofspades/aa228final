import random

class SemiRandomAgent():
	def __init__(self, environment, values):
		self.env = environment
		self.values = values

	def run(self, ntrials):
		totaltotal = 0
		for i in range(ntrials):
			done = False
			state = self.env.reset()
			totalreward = 0
			while done == False:
				maxValues = []
				for a in self.env.action_space:
					nextStates = self.env.next(state, a)
					value = 0
					for nextState in nextStates:
						if self.values.has_key(nextState) and self.values[nextState] != None:
							value = value + self.env.T(state, a, nextState)*self.values[nextState]
					maxValues.append(value)
				action = maxValues.index(max(maxValues))
				state, reward, done = self.env.step(state, action)
				totalreward = totalreward + reward
			totaltotal = totaltotal + totalreward
		print "Average reward over", ntrials, "episodes:", float(totaltotal)/ntrials