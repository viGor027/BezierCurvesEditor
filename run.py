import sys
import pygame
from views.edit import Edit
from views.start import Start
from state.state_manager import StateManager
from views.constants import WIDTH, HEIGHT, FPS


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Bezier Curve Editor")

        self.state_manager = StateManager("start")
        self.start = Start(self.screen, self.state_manager)
        self.edit = Edit(self.screen, self.state_manager)

        self.states = {"start": self.start, "edit": self.edit}

    def run(self):
        """
        runtime loop
        :return: None
        """
        bg_path = None
        shape_path = None
        while True:
            self.states[self.state_manager.get_state()].run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    runtime = Main()
    runtime.run()
