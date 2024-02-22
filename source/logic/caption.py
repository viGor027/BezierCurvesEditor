from source.logic.shape import Shape
from source.views.constants import TYPE_WIDTH
from math import tan, radians


class Caption:
    """
    Class managing a caption for text rendering.

    Attributes:
        letters (list): List containing shapes of individual letters.
        begin_from (int): Starting position for rendering the next letter.
        prev_begin_from (list): List storing previous starting positions.
        cursive (int): Flag indicating whether cursive style is enabled (1) or disabled (0).
        adjust_p (list): List of letters to be adjusted in the y-axis for better visual appearance.
        adjust_ly (list): List of letters to be adjusted in the y-axis for cursive style.
    """
    def __init__(self):
        self.letters = []
        self.begin_from = 40
        self.prev_begin_from = []
        self.last_letter = []
        self.cursive = 1
        self.adjust_p = ['a', 'ą', 'b', 'c', 'ć',
                         'd', 'e', 'ę', 'h', 'i',
                         'k', 'l', 'ł', 'm', 'n',
                         'ń', 'o', 'ó', 'u', 'r',
                         's', 'ś', 't', 'w', 'x',
                         'z', 'ź', 'ż']

        self.adjust_ly = ['a', 'ą', 'b', 'c', 'ć',
                          'd', 'e', 'ę', 'h',
                          'k', 'm', 'n', 'y',
                          'ń', 'o', 'ó', 'u', 'r',
                          's', 'ś', 't', 'w', 'x',
                          'z', 'ź', 'ż']

    def adjust_single_letter(self, letter_shape: Shape, shift_y: int, scale: float, shift_x: int = 0) -> None:
        """
        :param letter_shape: Shape object containing letter.
        :param shift_y: y-axis shift.
        :param scale: value which will be used to scale letter.
        :param shift_x: x-axis shift.
        :return: None
        """
        self.prev_begin_from.append(self.begin_from)
        max_right = 0
        max_left = TYPE_WIDTH
        letter = letter_shape.get_shape()
        for curve_id in range(len(letter)):
            for point_id in range(len(letter[curve_id])):
                if letter[curve_id][point_id][0] < max_left:
                    max_left = letter[curve_id][point_id][0]
                elif letter[curve_id][point_id][0] > max_right:
                    max_right = letter[curve_id][point_id][0]

                letter[curve_id][point_id][0] = letter[curve_id][point_id][0] * scale + shift_x
                letter[curve_id][point_id][1] = letter[curve_id][point_id][1] * scale + shift_y

        max_left *= scale
        diff = self.begin_from - max_left
        max_right = max_right * scale + diff
        for curve_id in range(len(letter)):
            for point_id in range(len(letter[curve_id])):
                letter[curve_id][point_id][0] += diff
        self.begin_from = max_right + 5 + shift_x
        self.letters.append(letter)

    @staticmethod
    def tilt(points: list, shear_factor: float) -> list[list]:
        """
        Affinity transformation for cursive.
        :param points: list of control points.
        :param shear_factor: determines the slope level.
        :return:
        """
        sheared_points = [[x + y * shear_factor, y] for x, y in points]
        return sheared_points

    def make_cursive(self, side: int) -> None:
        """
        :param side: value indicating if cursive is "on" or "off".
        :return: None
        """
        for letter_id in range(len(self.letters)):
            for control_points_id in range(len(self.letters[letter_id])):
                deg = tan(radians(side * -15))
                self.letters[letter_id][control_points_id] = self.tilt(self.letters[letter_id][control_points_id], deg)
