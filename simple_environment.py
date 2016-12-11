'''
This environment is a simple stealth game. The agent will be trained to hide from a single
patrolling enemy.

There are 101*100 states, representing levels of detection as a percentage from 0-100 and timesteps from 0-99.

The action space consists of two actions: move or hide.

Every time the agent chooses to move, there is a 10% chance that the detection level will decrease by 5,
a 30% chance that the detection level will stay the same, a 40% chance
that it will increase by 5, and a 20% chance that it will increase by 10.

Every time the agent chooses to hide, there is a 70% chance that the detection level decreases by 5,
a 20% chance that it decreases by 10, and a 10% chance that it stays the same.

If the detection level reaches 100, the game ends and the agent receives a -10 reward.

If the agent remains undetected for 100 time steps, the game ends and the agent receives a +10 reward.
Taking the hide action from any state results in a -1 reward. Moving results in a 0 reward.
'''

import random

class SimpleStealth():
	def __init__(self):
		self.state_space = []
		for i in range(0,101):
			for j in range(0,100):
				self.state_space.append((i,j))
		self.action_space = range(0,2)
		self.T = self.transitionProbability
		self.R = self.reward

	def transitionProbability(self, state, action, nextstate):
		if action == 0: #move
			if nextstate[0] - state[0] == -5:
				return 0.1
			elif nextstate[0] - state[0] == 0:
				return 0.3
			elif nextstate[0] - state[0] == 5:
				return 0.4
			elif nextstate[0] - state[0] == 10:
				return 0.2
			else:
				return 0
		else: #hide
			if nextstate[0] - state[0] == -10:
				return 0.2
			elif nextstate[0] - state[0] == -5:
				return 0.7
			elif nextstate[0] - state[0] == 0:
				return 0.1
			else:
				return 0

	def reward(self, state, action):
		if state[0] == 100:
			return -10
		elif state[1] == 99:
			return 10
		else:
			if action == 0:
				return -1
			else:
				return 0

	def done(self, state, action):
		if state[0] == 100 or state[1] == 99:
			return True
		else:
			return False

	def step(self, state, action):
		next = None
		rand = random.random()
		if action == 0:
			if rand < 0.1:
				next = max([0, state[0] - 5])
			elif rand < 0.4:
				next = state[0]
			elif rand < 0.8:
				next = min([100, state[0] + 5])
			else:
				next = min([100, state[0] + 10])
		else:
			if rand < 0.2:
				next = max([0, state[0] - 10])
			elif rand < 0.9:
				next = max([0, state[0] - 5])
			else:
				next = state[0]
		return ((next, state[1] + 1), self.reward(state, action), self.done(state, action))

	def reset(self):
		return (random.choice(range(0,101)), 0)

	def next(self, state, action):
		nextStates = []
		if state[1] < 99:
			if action == 0:
				if state[0] - 5 >= 0:
					nextStates.append(state[0]-5)
				if state[0] + 5 <= 100:
					nextStates.append(state[0]+5)
				if state[0] + 10 <= 100:
					nextStates.append(state[0]+10)
			else:
				if state[0] - 10 >= 0:
					nextStates.append(state[0]-10)
				if state[0] - 5 >= 0:
					nextStates.append(state[0]-5)
			nextStates.append(state[0])
		return [(nextState, state[1]+1) for nextState in nextStates]