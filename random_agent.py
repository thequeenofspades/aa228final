import random

class RandomAgent():
	def __init__(self, environment):
		self.environment = environment

	def run(self, ntrials):
		totaltotal = 0
		for i in range(ntrials):
			done = False
			state = self.environment.reset()
			totalreward = 0
			while done == False:
				action = random.choice(self.environment.action_space)
				state, reward, done = self.environment.step(state, action)
				totalreward = totalreward + reward
			totaltotal = totaltotal + totalreward
		print "Average reward over", ntrials, "episodes:", float(totaltotal)/ntrials