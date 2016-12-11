import environments as e
import random_agent as ra
import random_explorer as re
import semi_random_agent as sra
import algorithms as alg
import policy_agent as pa
import forward_search_agent as fsa

EXPLORE_DISCOUNT = 0.9
EXPLORE_TRIALS = 1000
LAVI_DISCOUNT = 0.9
LAVI_CUTOFF = 500
TEST_TRIALS = 1000
FS_DISCOUNT = 0.9
FS_DEPTH = 2

env = e.ComplexStealth()
explorer = re.RandomExplorer(env, EXPLORE_DISCOUNT, EXPLORE_TRIALS)
explorer.explore()

print "Running random agent..."
agent = ra.RandomAgent(env)
agent.run(TEST_TRIALS)

print "Running semirandom agent using exploration values only..."
agent = sra.SemiRandomAgent(env, explorer.vals())
agent.run(TEST_TRIALS)

print "Running forward search agent..."
agent = fsa.ForwardSearchAgent(env)
agent.run(TEST_TRIALS, FS_DEPTH, FS_DISCOUNT)

print "Running local approximation value iteration..."
values = alg.localApproximationValueIteration(env, explorer.vals(), LAVI_DISCOUNT, LAVI_CUTOFF)
policy = alg.policy(env, values, 0.9)

print "Running agent using LAVI values..."
agent = pa.PolicyAgent(env, policy)
agent.run(TEST_TRIALS)