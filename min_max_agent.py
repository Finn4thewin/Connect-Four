from copy import deepcopy

class Min_Max_Agent:
		def __init__(self, depth, player):
			self.depth = depth
			self.player = player

		def decide(self, cf):
			root = Min_Max_Tree(self.depth, deepcopy(cf), "max", self.player)
			best = root.determine_values(float("-inf"), float("inf"))
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
		self.child_values = []
		self.max_min = max_min
		self.cf = cf
		self.a_moves = self.cf.a_moves()
		self.depth = depth
		self.player = player

	def determine_values(self, a, b):
		if self.leaf or self.value != -99999:
			return self.value

		if self.max_min == "max":
			v = float("-inf")
			for move in self.a_moves:
				new_cf = deepcopy(self.cf)
				new_cf.make_move(move)
				child = Min_Max_Tree(self.depth - 1, new_cf, "min", self.player)
				child_v = child.determine_values(a, b)
				self.child_values.append(child_v)
				v = max(v, child_v)
				a = max(a, v)
				if a >= b:
					break
			return v
		else:
			v = float("inf")
			for move in self.a_moves:
				new_cf = deepcopy(self.cf)
				new_cf.make_move(move)
				child = Min_Max_Tree(self.depth - 1, new_cf, "max", self.player)
				child_v = child.determine_values(a, b)
				self.child_values.append(child_v)
				v = min(v, child_v)
				b = min(b, v)
				if a >= b:
					break
			return v

