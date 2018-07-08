# Connect-Four
Simple Connect-Four game, with a MCTS agent to play against

Usage
```
python game.py
```


### agent.py

The agent object, decides on a move to take based on random simulation of games.

### connectfour.py

Handles all of the logic related to the game rules. Such as when the game is won, and the current state of the game board.

### game.py

Handles all of the visualization, and human interaction. Contains an instance of ConnectFour, and the agent. Uses the Pygame library.