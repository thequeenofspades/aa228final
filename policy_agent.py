class PolicyAgent():
	def __init__(self, env, policy):
		self.env = env
		self.policy = policy

	def run(self, ntrials):
		totaltotal = 0
		for i in range(ntrials):
			done = False
			state = self.env.reset()
			totalreward = 0
			while done == False:
				action = self.policy[state]
				state, reward, done = self.env.step(state, action)
				totalreward = totalreward + reward
			totaltotal = totaltotal + totalreward
		print "Average reward over", ntrials, "episodes:", float(totaltotal)/ntrials