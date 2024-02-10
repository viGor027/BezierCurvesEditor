import pygame
from dataclasses import dataclass, field
from source.views.constants import WIDTH, HEIGHT, TYPE_WIDTH, TYPE_HEIGHT


@dataclass
class ViewManager:
    state: str
    background_path: str | None = None
    shape_path: str | None = None
    _prev_state: str | None = None
    _window_size: dict = field(default_factory=lambda: {'start': (WIDTH, HEIGHT),
                                                        'edit': (WIDTH, HEIGHT),
                                                        'type': (TYPE_WIDTH, TYPE_HEIGHT)})

    def get_state(self) -> str:
        """
        Returns current state
        :return: str
        """
        return self.state

    def set_state(self, new_state: str) -> None:
        """
        :param new_state: new state of editor
        :return: None
        """
        self.state = new_state

    def set_bg_path(self, bg_path: str) -> None:
        """
        :param bg_path: path to the background that will be loaded in editor
        :return: None
        """
        self.background_path = bg_path

    def set_shape_path(self, shape_path) -> None:
        """
        :param shape_path: path to the shape that will be loaded in editor
        :return: None
        """
        self.shape_path = shape_path

    def set_window_size(self) -> pygame.surface.Surface | None:
        if self._prev_state != self.state:
            self._prev_state = self.state
            return pygame.display.set_mode(self._window_size[self.state])
        else:
            return None
