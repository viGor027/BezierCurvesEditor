from dataclasses import dataclass


@dataclass
class StateManager:
    state: str
    background_path: str | None = None
    shape_path: str | None = None

    def get_state(self):
        """
        Returns current state
        :return: str
        """
        return self.state

    def set_state(self, new_state: str, bg_path: str | None = None, shape_path: str | None = None):
        """
        :param new_state: new state of editor
        :param bg_path: path to the background that will be loaded in editor
        :param shape_path: path to the shape that will be loaded in editor
        :return: None
        """
        self.state = new_state
        self.background_path = bg_path
        self.shape_path = shape_path
