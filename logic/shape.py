import json


class Shape:
    def __init__(self):
        self._shape: list[list] = []
        self._current_curve_id: int = -1
        self._prev_edited_curve: list = []

    def new_curve(self):
        """
        Adds another curve to the shape on click of a user
        :return: None
        """
        if len(self._shape) > 0 and not self._shape[-1]:
            self._current_curve_id = len(self._shape) - 1
        else:
            self._shape.append([])
            self._prev_edited_curve.append(self._current_curve_id)
            self._current_curve_id += 1

    def add_point(self, point: tuple):
        """
        :param point: point to be added to curve
        :return: None
        """
        if self._current_curve_id != -1:
            self._shape[self._current_curve_id].append(point)

    def update_point(self, point_id: int, pos: tuple):
        """
        Updates dragged point cords.
        :param point_id: id of a point on currently edited curve that is being dragged
        :param pos: new position of a point on current curve with id point_id
        :return:  None
        """
        self._shape[self._current_curve_id][point_id] = [pos[0], pos[1]]

    def save(self, directory: str):
        """
        :param directory: the place where the json file with the shape will be saved, including name of the file and
        *.extension
        :return: None
        """
        with open(directory, 'w', encoding='utf-8') as f:
            json.dump(self._shape, f, ensure_ascii=False, indent=4)

    def get_closest_point(self, mouse_pos: tuple, through_all: bool = False):
        """
        :param through_all:  If true find the closest point from all the curves,
                             else find the closest point on currently edited curve
        :param mouse_pos: position of a mouse
        :return: id of closest point to the mouse on currently edited curve if through_all is True,
                 else id of closest point to the mouse from all the curves
        """
        if through_all:
            return self._search_through_all_curves(mouse_pos)

        if self._current_curve_id == -1:
            return None, -1

        min_distance = float('inf')
        closest_point_id = None
        for i, point in enumerate(self._shape[self._current_curve_id]):
            distance = ((mouse_pos[0] - point[0]) ** 2 + (mouse_pos[1] - point[1]) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_point_id = i
        return closest_point_id, self._current_curve_id

    def _search_through_all_curves(self, mouse_pos: tuple):
        """
        :param mouse_pos: position of a mouse
        :return: id of closest point to the mouse from all the curves and id of its curve
        """
        closest_point_id = None
        closest_curve_id = None
        min_distance = float('inf')
        for curve_id, curve in enumerate(self._shape):
            for point_id, point in enumerate(curve):
                distance = ((mouse_pos[0] - point[0]) ** 2 + (mouse_pos[1] - point[1]) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_point_id = point_id
                    closest_curve_id = curve_id
        return closest_point_id, closest_curve_id

    def switch_curve(self, mouse_pos: tuple):
        """
        Changes the currently edited curve to a different one
        :param mouse_pos: position of a mouse
        :return: None
        """
        closest_point_id, closest_curve_id = self._search_through_all_curves(mouse_pos)
        self._prev_edited_curve.append(self._current_curve_id)
        self._current_curve_id = closest_curve_id

    def delete_point(self, mouse_pos: tuple):
        """
        deletes a point from currently edited curve
        :param mouse_pos:  position of mouse
        :return: None
        """
        closest_point_id, currently_edited_curve_id = self.get_closest_point(mouse_pos)
        if currently_edited_curve_id != -1:
            self._shape[currently_edited_curve_id].pop(closest_point_id)
            if len(self._shape[currently_edited_curve_id]) == 0:
                self._shape.pop(currently_edited_curve_id)
                self._current_curve_id = self._prev_edited_curve.pop(-1)

    def c0_connection(self):
        """
        Creates new curve with its first point same as last point of current curve
        :return: None
        """
        if self._current_curve_id != -1:
            point_to_be_copied = self._shape[self._current_curve_id][-1]
            self.new_curve()
            self.add_point(point_to_be_copied)

    def load_shape(self, shape: list[list]):
        """
        Loads shape to object
        :param shape: list of curves of loaded json file
        :return:
        """
        self._shape = shape
        self._prev_edited_curve.extend([i for i in range(len(shape) - 1)])
        self._current_curve_id = len(shape) - 1

    def get_current_curve_id(self):
        """
        :return: id of a currently edited curve
        """
        return self._current_curve_id

    def get_shape(self):
        """
        :return: array of curves that make up a shape.
        """
        return self._shape
