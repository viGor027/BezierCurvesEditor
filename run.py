import pygame
from source.views.edit import Edit
from source.views.start import Start
from source.views.type import Type
from source.state.view_manager import ViewManager
from source.state.edit_ui_manager import EditUIState
from source.views.constants import WIDTH, HEIGHT, FPS
from source.logic.shape import Shape


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
        self.type = Type(self.screen, self.view_manager)

        self.views = {"start": self.start, "edit": self.edit, "type": self.type}

    def run(self) -> None:
        """
        runtime loop
        :return: None
        """
        while True:
            self.views[self.view_manager.get_state()].run()
            if screen := self.view_manager.set_window_size():
                self.screen = screen
            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    runtime = Main()
    runtime.run()
