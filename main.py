# main.py
from simulation import Simulation
from window import Window

# Constants
WIDTH = 800
HEIGHT = 600

def main():
    window = Window(WIDTH, HEIGHT)
    window.create()
    simulation = Simulation()
    running = True
    while running:
        running = window.handle_events(simulation)

        # Update simulation
        simulation.update()

        # Clear window
        window.clear()
        # Draw simulation
        screen = window.get_screen()
        simulation.draw(screen)

        # Update window
        window.update()

    window.close()

if __name__ == "__main__":
    main()
