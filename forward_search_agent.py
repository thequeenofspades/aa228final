import time

class ForwardSearchAgent():
	def __init__(self, env):
		self.env = env

	def run(self, ntrials, depth, discount):
		totaltotal = 0
		starttime = time.time()
		for i in range(ntrials):
			done = False
			state = self.env.reset()
			totalreward = 0
			while done == False:
				action, value = self.selectAction(state, depth, discount)
				state, reward, done = self.env.step(state, action)
				totalreward = totalreward + reward
			totaltotal = totaltotal + totalreward
		print "Average reward over", ntrials, "episodes:", float(totaltotal)/ntrials
		print "Took", time.time() - starttime, "for", ntrials, "trials"

	def selectAction(self, state, depth, discount):
		if depth == 0:
			return (None, 0)
		action, value = (None, None)
		for a in self.env.action_space:
			v = self.env.R(state, a)
			nextStates = self.env.next(state, a)
			for next in nextStates:
				ap, vp = self.selectAction(next, depth - 1, discount)
				v = v + discount*self.env.T(state, a, next)*vp
			if v > value:
				action, value = (a, v)
		return (action, value)