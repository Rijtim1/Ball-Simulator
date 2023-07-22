# Documentation

## ballSprite.py

The `ballSprite.py` file contains the `BallSprite` class that extends the `pygame.sprite.Sprite` class to provide functionality for a sprite representing a ball.

**Classes**

- `BallSprite`
  - **Attributes**
    - `ball`: An object of the `Ball` class representing a ball
    - `image`: A `pygame.Surface` object that represents the image of the sprite
    - `rect`: A `pygame.Rect` object representing the rectangular area of the image
  - **Methods**
    - `__init__(self, ball)`: Initializes a new `BallSprite` object
    - `update(self)`: Updates the `rect` attribute of the sprite

## ball.py

The `ball.py` file contains the `Ball` class that represents a ball object.

**Classes**

- `Ball`
  - **Attributes**
    - `position`: A `numpy` array representing the position of the ball
    - `velocity`: A `numpy` array representing the velocity of the ball
    - `radius`: An integer representing the radius of the ball
    - `radius_squared`: An integer representing the square of the radius of the ball
    - `color`: A tuple representing the RGB color of the ball
    - `damping`: A float representing the damping factor of the ball's motion
    - `random_values`: A dictionary for storing random values
  - **Methods**
    - `__init__(self, position, velocity, radius, color)`: Initializes a new `Ball` object
    - `get_random_value(self, key: str, probability: float, value_range: tuple) -> float`: Gets a random value for the given key
    - `update(self, gravity, dt, width, height)`: Updates the position and velocity of the ball
    - `handle_collisions(self, width, height)`: Handles collisions of the ball with the edges of the window
    - `draw(self, surface)`: Draws the ball on the given surface

## main.py

The `main.py` file is the entry point for the simulation. It initializes the `Window` and `Simulation` objects and runs the simulation loop.

**Functions**

- `main()`: The main function for running the simulation

## quadtree.py

The `quadtree.py` file contains the `QuadTree` class that implements a quadtree for spatial partitioning to improve performance when checking for collisions.

**Classes**

- `QuadTree`
  - **Attributes**
    - `bounds`: A tuple representing the bounding rectangle of the quadtree
    - `capacity`: An integer representing the maximum number of objects that can be stored in the quadtree before it subdivides
    - `balls`: A list of `Ball` objects in the quadtree
    - `children`: A list of child `QuadTree` objects
  - **Methods**
    - `__init__(self, bounds, capacity=4)`: Initializes a new `QuadTree` object
    - `insert(self, ball)`: Inserts a ball into the quadtree
    - `subdivide(self)`: Subdivides the quadtree into four children
    - `in_bounds(self, position)`: Checks whether a position is within the bounds of the quadtree
    - `get_collidable_balls(self, ball)`: Gets a list of balls that could potentially collide with the given ball

## simulation.py

The `simulation.py` file contains the `Simulation` class that handles the simulation of balls.

**Classes**

- `Simulation`
  - **Attributes**
    - `balls`: A list of `Ball` objects
    - `gravity`: A `numpy` array representing the gravity in the simulation
    - `dt`: A float representing the time step for the simulation
    - `height`: An integer representing the height of the window
    - `width`: An integer representing the width of the window
    - `debug_mode`: A boolean representing whether the debug mode is active
    - `first_ball_added`: A boolean representing whether the first ball has been added
    - `collision_sound`: A `pygame.mixer.Sound` object representing the sound that plays when balls collide
    - `number_collisions`: An integer representing the number of collisions that have occurred
    - `quad_tree`: A `QuadTree` object for spatial partitioning
  - **Methods**
    - `__init__(self)`: Initializes a new `Simulation` object
    - `add_ball(self, ball: Ball)`: Adds a ball to the simulation
    - `update(self)`: Updates the simulation
    - `update_ball(self, ball)`: Updates a ball in the simulation
    - `draw(self, surface)`: Draws the simulation on the given surface
    - `toggle_debug_mode(self)`: Toggles the debug mode
    - `check_collisions(self)`: Checks for collisions between balls
    - `is_collision(self, ball1, ball2)`: Checks whether two balls are colliding
    - `resolve_collision(self, ball1, ball2)`: Resolves a collision between two balls

## window.py

The `window.py` file contains the `Window` class that handles the creation and updating of the window.

**Classes**

- `Window`
  - **Attributes**
    - `width`: An integer representing the width of the window.
    - `height`: An integer representing the height of the window.
    - `screen`: A `pygame.Surface` object representing the window's main display area.
    - `mouse_start_pos`: A tuple representing the position of the mouse when the left button is first pressed.
    - `mouse_start_time`: An integer representing the time when the left mouse button is first pressed.
    - `is_running`: A boolean indicating whether the window's main loop is currently running.
    - `simulation`: An instance of the `Simulation` class that handles the simulation logic.
  - **Methods**
    - `__init__(self, width: int, height: int, simulation: Simulation)`: Constructor method that initializes a new `Window` object.
    - `run(self)`: Starts the window's main event loop.
    - `handle_events(self)`: Handles the user input and system events.
    - `draw(self)`: Draws the window and all contained elements, including the simulation.
    - `draw_text(self, text: str, position: Tuple[int, int], color: Tuple[int, int, int] = (255, 255, 255))`: Renders the provided text on the window at the given position and color.
    - `get_font(self, name: Optional[str], size: int)`: Returns a `pygame.Font` object for the given font name and size. If no name is provided, the default system font will be used.
    - `create_ball(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int])`: Creates a new `Ball` object based on the start and end positions of the mouse and adds it to the simulation.
    - `quit(self)`: Stops the window's main event loop, effectively closing the window.
