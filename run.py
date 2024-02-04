import pygame
from views.edit import Edit
from views.start import Start
from state.view_manager import ViewManager
from state.edit_ui_manager import EditUIState
from views.constants import WIDTH, HEIGHT, FPS
from logic.shape import Shape


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Bezier Curve Editor")

        self.edit_ui_state_manager = EditUIState()
        self.shape = Shape()

        self.view_manager = ViewManager("start")
        self.start = Start(self.screen, self.view_manager)
        self.edit = Edit(self.screen, self.view_manager)

        self.views = {"start": self.start, "edit": self.edit}

    def run(self):
        """
        runtime loop
        :return: None
        """
        while True:
            self.views[self.view_manager.get_state()].run()
            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    runtime = Main()
    runtime.run()
