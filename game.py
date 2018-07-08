import time
import random
import sys
import pygame
import math
import pickle
import threading
from copy import deepcopy
from connectfour import ConnectFour
from min_max_agent import Min_Max_Agent
from MCTS_agent import MCTS_Agent

# Defining global variables
pygame.init()
myfont = pygame.font.SysFont("monospace", 25)
myfont2 = pygame.font.SysFont("monospace", 25)

FPS = 30
fpsClock = pygame.time.Clock()
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 800
vOffset = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Connect Four')

# Defining a variety of colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BROWN = (237, 222, 185)
BRIGHTBLUE = (0, 50, 255)
YELLOW = (255, 255, 25)
GREEN = (8, 122, 21)

# Used to simplify drawing of the board
pieces = [WHITE, RED, BLACK, GREY]
names = ['nil', 'Red', 'Black', 'Nobody']

# Checks if the user has quit the game
def checkForQuit(events):
    for event in events:
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

# Checks if a coordinate is inside of a rectangle      
def intersects(x, y, rect):
    if x < rect[0]:
        return False
    if x > rect[0] + rect[2]:
        return False
    if y < rect[1]:
        return False
    if y > rect[1] + rect[3]:
        return False
    return True


# Draws the current state of the board
def draw_board(cf):
    pygame.draw.rect(screen, YELLOW, [0, vOffset, SCREEN_WIDTH, SCREEN_HEIGHT - vOffset])
    for x in range(7):
        for y in range(6):
            piece = cf.board.spaces[y][x]
            pygame.draw.circle(screen, pieces[piece], [75 + 100 * x, vOffset + 75 + 100 * y], 45)

# Visualizes which moves are available to play
def draw_possible(moves, h_move, col):
    for x in range(7):
        if moves[x] != 0:
            if x == h_move:
                color = col
            else:
                color = GREY
            pygame.draw.circle(screen, color, [75 + 100 *x, 50], 45)

# Highlights a game piece with a green circle
def highlight_piece(x, y):
    pygame.draw.circle(screen, GREEN, [75 + 100 * x, vOffset + 75 + 100 * y], 45, 5)

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

# Determines which column the x coordinate belongs to
def hovered_move(x):
    return clamp(math.floor(x / 100), 0, 6)

def draw_thinking():
    time = pygame.time.get_ticks()
    x = math.sin(time / 1000) * SCREEN_WIDTH / 3
    pygame.draw.circle(screen, BRIGHTBLUE, [int(SCREEN_WIDTH / 2 + x), 50], 25)

# Draws text at a position
def draw_text(txt, pos, color):
    surf = myfont.render(txt, False, color)
    screen.blit(surf, pos)

# Thread for the agent decide function
# Necessary because agent.decide takes a long time, and allows
# for playing an animation in the mean time
def agentDecide(agent, cf, decision):
    agentsCF = deepcopy(cf)
    ret = agent.decide(agentsCF)
    decision.append(ret)

# Plays a game against the agent
def one_player(player, bot, algorithm):
    cf = ConnectFour()
    prev_x = -2
    prev_y = -2
    firstClick = False
    firstRun = True
    decision = []
    if algorithm == "MCTS":
        agent = MCTS_Agent(900, bot)
    else:
        agent = Min_Max_Agent(5, bot)
    while True:
        # Draw the board, and get events
        screen.fill(WHITE)
        draw_board(cf)
        highlight_piece(prev_x, prev_y)
        events = pygame.event.get()
        checkForQuit(events)

        if cf.winner == 0:
            draw_text(names[cf.whos_turn] + "'s turn", (25, SCREEN_HEIGHT - 50), BRIGHTBLUE)

            # Players turn
            if cf.whos_turn == player:
                # Determine which column the mouse is hovering over
                (x,y) = pygame.mouse.get_pos()
                h_move = hovered_move(x)
                # Draw available moves
                moves = cf.board.available_moves()
                color = pieces[cf.whos_turn]
                draw_possible(moves, h_move, color)
                # Check for mouse click, if player is hovering a valid move
                if moves[h_move] > 0:
                    (m1, m2, m3) = pygame.mouse.get_pressed()
                    if m1 and firstClick:
                        firstClick = False
                        prev_y, prev_x = cf.make_move(h_move)
                    if not m1:
                        firstClick = True
            else:
                # Begins the thread if not already
                if firstRun:
                    agentThread = threading.Thread(target=agentDecide, args=(agent, cf, decision))
                    agentThread.start()
                    firstRun = False
                # Waiting for thread to finish
                elif decision != []:
                    prev_y, prev_x = cf.make_move(decision[0])
                    decision = []
                    firstRun = True
                # Plays the thinking animation
                else:
                    draw_thinking()
        # When someone has won the game
        else:
            pygame.draw.rect(screen, pieces[cf.winner], [0, 0, SCREEN_WIDTH, vOffset])
            draw_text(names[cf.winner] + " Wins the game press r to reset", (25, 25), BRIGHTBLUE)
        # Check for reset key being pressed
        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                cf.reset()
                return


        pygame.display.flip()

# Runs a two player game
def two_player():
    # Initialize game
    cf = ConnectFour()
    prev_x = -2
    prev_y = -2
    firstClick = False
    while True:
        # Draw the board
        screen.fill(WHITE)
        draw_board(cf)
        highlight_piece(prev_x, prev_y)

        # quit events
        events = pygame.event.get()
        checkForQuit(events)

        if cf.winner == 0:
            draw_text(names[cf.whos_turn] + "'s turn", (25, SCREEN_HEIGHT - 50), BRIGHTBLUE)
            # Get and draw the column the mouse is hovering
            (x,y) = pygame.mouse.get_pos()
            h_move = hovered_move(x)
            # Draw available moves
            moves = cf.board.available_moves()
            color = pieces[cf.whos_turn]
            draw_possible(moves, h_move, color)
            # If player is hovering a valid move check for click
            if moves[h_move] > 0:
                pygame.event.get()
                (m1, m2, m3) = pygame.mouse.get_pressed()
                if m1 and firstClick:
                    firstClick = False
                    # Makes the move
                    prev_y, prev_x = cf.make_move(h_move)
                if not m1:
                    firstClick = True
        # When someone has won the game
        else:
            pygame.draw.rect(screen, pieces[cf.winner], [0, 0, SCREEN_WIDTH, vOffset])
            draw_text(names[cf.winner] + " Wins the game press r to reset", (25, 25), BRIGHTBLUE)
        # Check for reset key being pressed
        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                cf.reset()
                return


        pygame.display.flip()
	

# Displays a menu to the player, and determines what game mode they choose
def menu():
    decision = 0
    while decision == 0:
        events = pygame.event.get()
        checkForQuit(events)
        screen.fill(GREY)

        # Define rectangles for the buttons
        rect_width = 200
        rect_height = 100
        twopbut = [SCREEN_WIDTH / 2 - rect_width / 2, 100, rect_width, rect_height]
        onepbut = [SCREEN_WIDTH / 2 - rect_width / 2, 300, rect_width, rect_height]
        onepbut2 = [SCREEN_WIDTH / 2 - rect_width / 2, 500, rect_width, rect_height]
        # Draw the buttons
        pygame.draw.rect(screen, BRIGHTBLUE, twopbut)
        pygame.draw.rect(screen, BRIGHTBLUE, onepbut)
        pygame.draw.rect(screen, BRIGHTBLUE, onepbut2)
        draw_text("vs MCTS", [onepbut[0] + 15, onepbut[1] + 15], BLACK)
        draw_text("vs Min Max", [onepbut2[0] + 15, onepbut2[1] + 15], BLACK)
        draw_text("Two Player", [twopbut[0] + 15, twopbut[1] + 15], BLACK)
        # Check if the buttons were clicked on
        (x,y) = pygame.mouse.get_pos()
        (m1, m2, m3) = pygame.mouse.get_pressed()
        if m1 and intersects(x, y, twopbut):
            decision = 2
        elif m1 and intersects(x, y, onepbut):
            decision = 1
        elif m1 and intersects(x, y, onepbut2):
            decision = 3
        pygame.display.flip()
    return decision


def main():
    while True:
        state = menu()
        if state == 1 or state == 3:
            # Randomly determine colors
            if random.random() > 0.5:
                player = 1
                bot = 2
            else:
                player = 2
                bot = 1
            if state == 1:
                one_player(player, bot, "MCTS")
            else:
                one_player(player, bot, "minmax")
        elif state == 2:
            two_player()

main()