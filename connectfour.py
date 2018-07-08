

# Handles all of the game logic, except for taking turns.
class Board:
    def __init__(self):
        self.spaces = list()
        for i in range(6):
            self.spaces.append([0,0,0,0,0,0,0])

    def reset(self):
        self.spaces = list()
        for i in range(6):
            self.spaces.append([0,0,0,0,0,0,0])

    # Checks if space in board is available to place a new piece there
    # If not recursively checks the space above it
    def recurs_move(self, x, i, p):
        if self.spaces[i][x] == 0:
            self.spaces[i][x] = p
            return i, x
        elif i == 0:
            return -1, -1
        else:
            return self.recurs_move(x, i-1, p)

    # Starts the recusive placement checking at the bottom of the board
    def move(self, x, p):
        return self.recurs_move(x, 5, p)

    # Determines which columns a player can make a move in
    # returns a 1 or 0 for each column, 1 is open
    def available_moves(self):
        moves = list()
        for space in self.spaces[0]:
            if space == 0:
                moves.append(1)
            else:
                moves.append(0)
        return moves

    # Version of available moves that is more efficient for the agent to use
    # returns a list of what columns are open
    def a_moves(self):
        moves = list()
        i = 0
        for space in self.spaces[0]:
            if space == 0:
                moves.append(i)
            i+=1
        return moves

    # Checks if there is a set of winning pieces at x, y
    def check_spot(self, x, y, di):
        rcount = 0
        bcount = 0
        if di == 'up':
            if y > 2:
                factors = [-1, 0] # Check in negative y direction
            else:
                return 0
        elif di == 'down':
            return self.check_spot(x, y + 3, 'up')
        elif di == 'left':
            if x > 2:
                factors = [0, -1] # Check in negative x direction
            else:
                return 0
        elif di == 'right':
            return self.check_spot(x + 3, y, 'left')
        elif di == 'dur':
            if x < 4 and y > 2:
                factors = [-1, 1] # Check in  negative y, positive x direction
            else:
                return 0
        elif di == 'dul':
            if y > 2 and x > 2:
                factors = [-1, -1] # Check in negative y, negative x direction
            else:
                return 0
        elif di == 'ddr':
            return self.check_spot(x + 3, y + 3, 'dul')
        elif di == 'ddl':
            return self.check_spot(x + 3, y - 3, 'dur') 

        for i in range(4):
            if self.spaces[y + i * factors[0]][x + i * factors[1]] == 1:
                rcount = rcount + 1
            elif self.spaces[y + i * factors[0]][x + i * factors[1]] == 2:
                bcount = bcount + 1
        if rcount == 4:
            return 1
        elif bcount == 4:
            return 2
        return 0

    # Checks if someone has won the  game yet
    def check_winner(self):
        ret = 0
        a_moves = self.available_moves()

        # Checks for a draw first
        draw = True
        for move in a_moves:
            if move != 0:
                draw = False
        if draw:
            return 3

        # Check if one of the players have won
        for i in range(6):
            for j in range(7):
                for d in ['up', 'left', 'dur', 'dul']:
                    r = self.check_spot(j, i, d)
                    if r > ret:
                        return r
        return ret

# Primary purpose is to manage who's turn it is
# Otherwise just acts as an interface to the board
class ConnectFour:
    def __init__(self):
        self.board = Board()
        self.whos_turn = 1
        self.winner = 0
    def reset(self):
        self.board.reset()
        self.whos_turn = 1
        self.winner = 0
    def make_move(self, x):
        y, x = self.board.move(x, self.whos_turn)
        if y != -1:
            self.winner = self.board.check_winner()
            if self.whos_turn == 1:
                self.whos_turn = 2
            else:
                self.whos_turn = 1
            return y, x
        else:
            return y, x

    def a_moves(self):
        return self.board.a_moves()

    # Returns a unique key for the current state of the board.
    def key(self):
        s = ""
        for row in self.board.spaces:
            for col in row:
                s = s + str(col)
        return str(int(s))

