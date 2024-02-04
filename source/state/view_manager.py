from dataclasses import dataclass


@dataclass
class ViewManager:
    state: str
    background_path: str | None = None
    shape_path: str | None = None

    def get_state(self):
        """
        Returns current state
        :return: str
        """
        return self.state

    def set_state(self, new_state: str):
        """
        :param new_state: new state of editor
        :return: None
        """
        self.state = new_state

    def set_bg_path(self, bg_path: str):
        """
        :param bg_path: path to the background that will be loaded in editor
        :return: None
        """
        self.background_path = bg_path

    def set_shape_path(self, shape_path):
        """
        :param shape_path: path to the shape that will be loaded in editor
        :return: None
        """
        self.shape_path = shape_path
