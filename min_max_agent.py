from copy import deepcopy

#Interfaces with min-max tree and decides the best move to do in a given state
class Min_Max_Agent:
		def __init__(self, depth, player):
			self.depth = depth
			self.player = player

		# Uses the Min_Max_Tree to find the best move, and translates it into a move
		# the board uses
		def decide(self, cf):
			root = Min_Max_Tree(self.depth, deepcopy(cf), "max", self.player)
			best = root.determine_values(float("-inf"), float("inf"))
			a_moves = cf.a_moves()
			return a_moves[root.child_values.index(best)]


# Builds the Tree, and implements the Min_Max algorithm with
# Alpha Beta pruning
class Min_Max_Tree:
	def __init__(self, depth, cf, max_min, player):
		if depth == 0 or cf.winner != 0:
			self.leaf = True
			self.value = cf.heuristic(player)
		else:
			self.leaf = False
		self.child_values = []
		self.max_min = max_min
		# cf is an instance of the class ConnectFour
		self.cf = cf
		self.a_moves = self.cf.a_moves()
		self.depth = depth
		self.player = player

	# Min-Max with Alpha Beta 
	def determine_values(self, a, b):
		if self.leaf:
			return self.value

		if self.max_min == "max":
			v = float("-inf")
			for move in self.a_moves:
				# Generating the Child
				new_cf = deepcopy(self.cf)
				new_cf.make_move(move)
				child = Min_Max_Tree(self.depth - 1, new_cf, "min", self.player)
				# Recurse into the child
				child_v = child.determine_values(a, b)
				# Necessary for determining best move, after min-max finishes
				self.child_values.append(child_v)

				#Alpha Beta logic
				v = max(v, child_v)
				a = max(a, v)
				if a >= b:
					break # Pruned
			return v
		else:
			v = float("inf")
			for move in self.a_moves:
				# Generating the Child
				new_cf = deepcopy(self.cf)
				new_cf.make_move(move)
				child = Min_Max_Tree(self.depth - 1, new_cf, "max", self.player)
				# Recurse into the child
				child_v = child.determine_values(a, b)
				# Necessary for determining best move, after min-max finishes
				self.child_values.append(child_v)

				#Alpha Beta Logic
				v = min(v, child_v)
				b = min(b, v)
				if a >= b:
					break # Pruned
			return v

