import pygame
import sys
from views.constants import BLACK
from state.state_manager import StateManager


class Edit:
    def __init__(self, display: pygame.surface.Surface, state_manager: StateManager):
        self.display = display
        self.state_manager = state_manager

    def run(self):
        self.display.fill(BLACK)
        print(self.state_manager.state)
        print(self.state_manager.background_path)
        print(self.state_manager.shape_path)
        pygame.quit()
        sys.exit()