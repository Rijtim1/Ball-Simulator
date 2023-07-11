Based on the requirements, here are the core classes, functions, and methods that will be necessary:

1. `Ball` class:
   - Properties:
     - `position`: the current position of the ball
     - `velocity`: the current velocity of the ball
     - `radius`: the radius of the ball
     - `color`: the color of the ball
   - Methods:
     - `update`: updates the position and velocity of the ball based on gravity and collisions
     - `draw`: draws the ball on the screen

2. `Simulation` class:
   - Properties:
     - `balls`: a list of all the balls in the simulation
     - `debug_mode`: a flag indicating whether debug information should be displayed
   - Methods:
     - `add_ball`: adds a new ball to the simulation
     - `update`: updates the position and velocity of all the balls in the simulation
     - `draw`: draws all the balls on the screen
     - `toggle_debug_mode`: toggles the debug mode flag

3. `Window` class:
   - Properties:
     - `width`: the width of the window
     - `height`: the height of the window
   - Methods:
     - `create`: creates the window using Pygame
     - `handle_events`: handles user input events
     - `clear`: clears the window
     - `update`: updates the window display
     - `close`: closes the window

Now let's proceed with creating the necessary files and implementing the code.

**ball.py**
