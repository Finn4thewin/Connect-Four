import random
from copy import deepcopy

# An agent that uses Monte Carlo Tree search to determine which move to play
class Agent:
	def __init__(self, i, p):
		self.max_games = i
		self.player = p

		# Stores the win count for player 1, 2, and 0
		# 0 being draw, at each game state
		self.results = dict()

	# Determines which move to make based on winrates
	# of moves in random games. Simulates a max_games 
	# number of games for each possible first move.
	def decide(self, cf):
		# Will store the win rate of each move
		rates = []
		# Simulate all of the games for each available move
		a_moves = cf.a_moves()
		for i in range(self.max_games):
			for move in a_moves:
				cfn = deepcopy(cf)
				rate = self.sim_game(cfn, move)
		# One last simulation, this time saving the win rates
		for move in a_moves:
			cfn = deepcopy(cf)
			rate = self.sim_game(cfn, move)
			rates.append(rate[self.player-1] / sum(rate))
		return a_moves[rates.index(max(rates))]

	# Randomly plays one game, knowing only the first move to make
	# updates results dict of each states win loss draw
	# Returns the win counts of making the first move
	def sim_game(self, cf, first_move):
		# Stores each state visited
		states = []

		cf.make_move(first_move)
		states.append(cf.key())
		# Randomly plays the game
		while cf.winner == 0:
			a_moves = cf.a_moves()
			random.shuffle(a_moves)
			cf.make_move(a_moves[0])
			states.append(cf.key())
		# Updates the win rate at each of the states visited
		default_list = [0,0,0]
		for state in states:
			self.results[state] = self.results.get(state, default_list)
			self.results[state][cf.winner-1] += 1
		return self.results[states[0]]
