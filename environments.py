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

'''
This environment adds an additional layer of complexity to SimpleStealth. There is no longer a detection
level given as a percentage; instead the state includes the distance between the agent and the patrolling
enemy. The agent receives rewards for sticking close to the enemy but remaining undetected, while the enemy has
a higher chance of detecting the agent the closer the agent gets. As in SimpleStealth, the agent receives a bonus
for remaining undetected for 100 time steps, and a penalty for detection, but these bonuses and penalties have been increased.

The size of the state space increases to 101*100*2 = 20,200.

The distance ranges from 0 meters to 100 meters. The base detection rate at each time step is equal to 100-distance%, but can
be affected by use of the "hide" action. At each time step, the agent receives a reward of (100-distance)/10. Hiding carries the usual
penalty of -1.

The penalty for detection is -25, and the reward for remaining undetected is +25.

There are now 4 actions. The agent can move closer, decreasing the distance by 1, or move farther away, increasing the distance by 1.
The agent can remain still, which does not change the distance or the detection rate.
The agent can also hide, which does not affect the distance but decreases the rate of detection by 50%.
'''

class ComplexStealth():
	def __init__(self):
		self.state_space = []
		for i in range(0,101):
			for j in range(0,100):
				for k in range(0,2):
					self.state_space.append((i,j,k))
		self.action_space = range(0,4)
		self.T = self.transitionProbability
		self.R = self.reward

	def transitionProbability(self, state, action, nextstate):
		detectionRate = (100 - state[0])/float(100)
		if action == 3:
			detectionRate = detectionRate/2
		distance = state[0]
		if action == 0:
			distance = max([0, distance - 1])
		if action == 1:
			distance = min([100, distance + 1])
		if nextstate[0] == distance and nextstate[1] == state[1] + 1:
			if nextstate[2] == 1:
				return detectionRate
			elif nextstate[2] == 0:
				return 1 - detectionRate
		else:
			return 0

	def reward(self, state, action):
		if state[2] == 1:
			return -25
		if state[1] == 99:
			return 25
		r = (100-state[0])/float(10)
		if action == 3:
			r = r - 1
		return r

	def done(self, state, action):
		if state[1] == 99 or state[2] == 1:
			return True
		else:
			return False

	def step(self, state, action):
		detected = 0
		rand = random.random()
		detectionRate = (100-state[0])/float(100)
		if action == 3:
			detectionRate = detectionRate/2
		distance = state[0]
		if action == 0:
			distance = max([0, distance - 1])
		elif action == 1:
			distance = min([100, distance + 1])
		if rand < detectionRate:
			detected = 1
		return ((distance, state[1] + 1, detected), self.reward(state, action), self.done(state, action))

	def reset(self):
		return (random.choice(range(0,101)), 0, 0)

	def next(self, state, action):
		nextStates = []
		distance = state[0]
		if action == 0:
			distance = max([0, distance - 1])
		elif action == 1:
			distance = min([100, distance + 1])
		return [(distance, state[1]+1, 0), (distance, state[1]+1, 1)]