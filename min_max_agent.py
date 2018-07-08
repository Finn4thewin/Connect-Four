from copy import deepcopy

class Min_Max_Agent:
		def __init__(self, depth, player):
			self.depth = depth
			self.player = player

		def decide(self, cf):
			root = Min_Max_Tree(self.depth, deepcopy(cf), "max", self.player)
			best = root.determine_values()
			a_moves = cf.a_moves()
			return a_moves[root.child_values.index(best)]



class Min_Max_Tree:
	def __init__(self, depth, cf, max_min, player):
		if depth == 0 or cf.winner != 0:
			self.leaf = True
			self.value = cf.heuristic(player)
		else:
			self.leaf = False
			self.value = -99999
		self.children = []
		self.max_min = max_min
		self.cf = cf
		self.a_moves = self.cf.a_moves()
		self.depth = depth
		if not self.leaf:
			for move in self.a_moves:
				new_cf = deepcopy(self.cf)
				new_cf.make_move(move)
				if self.max_min == "max":
					self.children.append(Min_Max_Tree(depth - 1, new_cf, "min", player))
				else:
					self.children.append(Min_Max_Tree(depth - 1, new_cf, "max", player))

	def determine_values(self):
		if self.leaf or self.value != -99999:
			return self.value
		else:
			self.child_values = []
			for child in self.children:
				self.child_values.append(child.determine_values())
			if self.max_min == "max":
				self.value = max(self.child_values)
			else:
				self.value = min(self.child_values)

		return self.value

