import json
import pygame
import sys
from source.views.constants import BLACK, RED, WHITE, \
    BUTTON_COLOR, BUTTON_INACTIVE_COLOR, \
    ACTIVE_POINT_COLOR, ACTIVE_CURVE_COLOR, CONTROL_POINT_RADIUS, \
    WIDTH, HEIGHT
from source.state.view_manager import ViewManager
from source.state.edit_ui_manager import EditUIState
from source.logic.shape import Shape
from source.logic.faster_drawing_alg import bezier
from source.logic.optimize_sampling import get_optimized_moments, get_optimized_moments_experimental


class Edit:
    def __init__(self, display: pygame.surface.Surface, view_manager: ViewManager):
        self.display = display
        self.view_manager = view_manager
        self.shape = Shape()
        self.ui_state = EditUIState()

    def run(self) -> None:
        """
        Editing view
        :return: None
        """
        self.display.fill(WHITE)
        self._draw_grid()
        self._draw_buttons()
        self._draw_text()
        self._bg_handler(self.view_manager.background_path)
        self._shape_handler(self.view_manager.shape_path)
        self._event_handler()
        self._draw_control_points()
        self._draw_curves()

    def _event_handler(self) -> None:
        """
        Handles detecting and running appropriate actions for events
        :return: None
        """
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and 10 <= mouse[0] <= 85 and 10 <= mouse[1] <= 50:
                    self.shape.new_curve()
                elif event.button == 1 and 95 <= mouse[0] <= 170 and 10 <= mouse[1] <= 50:
                    self.ui_state.draw_grid = not self.ui_state.draw_grid
                elif event.button == 1 and 10 <= mouse[0] <= 85 and 60 <= mouse[1] <= 100:
                    self.shape.save('nowa.json')
                elif event.button == 1 and 95 <= mouse[0] <= 170 and 60 <= mouse[1] <= 100:
                    self.ui_state.edit = not self.ui_state.edit
                elif event.button == 1 and 10 <= mouse[0] <= 170 and 120 <= mouse[1] <= 150:
                    self.ui_state.show_background = not self.ui_state.show_background
                elif event.button == 1 and self.ui_state.edit:
                    self.shape.add_point(event.pos)
                elif event.button == 3 and self.ui_state.edit:
                    closest_index = self.shape.get_closest_point(event.pos)[0]
                    if closest_index is not None:
                        self.ui_state.dragging = True
                        self.ui_state.dragged_point_index = closest_index
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.ui_state.dragging = False
                    self.ui_state.dragged_point_index = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.ui_state.edit:
                    self.shape.delete_point(pygame.mouse.get_pos())
                elif event.key == pygame.K_e:
                    self.shape.switch_curve(pygame.mouse.get_pos())
                elif event.key == pygame.K_n:
                    self.shape.c0_connection()
                elif event.key == pygame.K_2:
                    self.shape.c2_connection(mouse)

        if self.ui_state.dragging and pygame.mouse.get_pressed()[2]:
            self.shape.update_point(self.ui_state.dragged_point_index, pygame.mouse.get_pos())

    def _bg_handler(self, bg_path: str | None) -> None:
        """
        Handles loading background
        :param bg_path: path to background
        :return: None
        """
        if self.ui_state.show_background and bg_path:
            bg = pygame.image.load(bg_path)
            self.display.blit(bg, (0, 0))

    def _shape_handler(self, shape_path: str | None) -> None:
        """
        Handles loading shape
        :param shape_path: path to json file containing shape
        :return: None
        """
        if shape_path and not self.ui_state.shape_loaded:
            json_with_shape = open(shape_path)
            shape_to_be_loaded = json.load(json_with_shape)
            self.shape.load_shape(shape_to_be_loaded)
            self.ui_state.shape_loaded = True

    def _draw_grid(self) -> None:
        """
        Draws helper lines
        :return:
        """
        if self.ui_state.draw_grid:
            pygame.draw.line(self.display, BLACK, (WIDTH / 2 - 1, 0), (WIDTH / 2 - 1, HEIGHT))
            pygame.draw.line(self.display, BLACK, (WIDTH / 2 + 1, 0), (WIDTH / 2 + 1, HEIGHT))

            pygame.draw.line(self.display, BLACK, (0, HEIGHT / 2 - 1), (WIDTH, HEIGHT / 2 - 1))
            pygame.draw.line(self.display, BLACK, (0, HEIGHT / 2 + 1), (WIDTH, HEIGHT / 2 + 1))

            for i in range(0, WIDTH, 20):
                if i == 180 or i == 620:
                    pygame.draw.line(self.display, RED, (i, 0), (i, HEIGHT))
                else:
                    pygame.draw.line(self.display, BLACK, (i, 0), (i, HEIGHT))

            for i in range(0, HEIGHT, 20):
                if i == 20 or i == 460 or i == 580:
                    pygame.draw.line(self.display, RED, (0, i), (WIDTH, i))
                else:
                    pygame.draw.line(self.display, BLACK, (0, i), (WIDTH, i))

    def _draw_buttons(self) -> None:
        """
        Draws UI buttons
        :return: None
         """
        # New curve button
        pygame.draw.rect(self.display, BUTTON_COLOR, [10, 10, 75, 40])

        # Grid button
        if self.ui_state.draw_grid:
            pygame.draw.rect(self.display, BUTTON_COLOR, [95, 10, 75, 40])
        else:
            pygame.draw.rect(self.display, BUTTON_INACTIVE_COLOR, [95, 10, 75, 40])

        # Save button
        pygame.draw.rect(self.display, BUTTON_COLOR, [10, 60, 75, 40])

        # Edit button
        if self.ui_state.edit:
            pygame.draw.rect(self.display, BUTTON_COLOR, [95, 60, 75, 40])
        else:
            pygame.draw.rect(self.display, BUTTON_INACTIVE_COLOR, [95, 60, 75, 40])

        # Show bg button
        if self.ui_state.show_background:
            pygame.draw.rect(self.display, BUTTON_COLOR, [10, 110, 160, 40])
        else:
            pygame.draw.rect(self.display, BUTTON_INACTIVE_COLOR, [10, 110, 160, 40])

    def _draw_text(self) -> None:
        """
        Displays text on UI buttons
        :return: None
        """
        smallfont = pygame.font.SysFont('Bahnschrift', 14)

        new_curve = smallfont.render('New curve', True, BLACK)
        grid = smallfont.render('Grid', True, BLACK)
        save = smallfont.render('Save', True, BLACK)
        edit_on = smallfont.render('Edit On ', True, BLACK)
        edit_off = smallfont.render('Edit Off', True, BLACK)
        show_background = smallfont.render('Show background', True, BLACK)

        self.display.blit(new_curve, (12, 23))
        self.display.blit(grid, (12 + 105, 23))
        self.display.blit(save, (12 + 15, 23 + 50))
        if self.ui_state.edit:
            self.display.blit(edit_on, (12 + 95, 23 + 50))
        else:
            self.display.blit(edit_off, (12 + 95, 23 + 50))
        self.display.blit(show_background, (12 + 30, 23 + 100))

    def _draw_control_points(self) -> None:
        """
        Draws control points of curves making up the shape
        :return: None
        """
        shape = self.shape.get_shape()
        if self.ui_state.edit:
            for control_points_id in range(len(shape)):
                for point_id in range(len(shape[control_points_id])):
                    if control_points_id == self.shape.get_current_curve_id():
                        pygame.draw.circle(self.display, ACTIVE_POINT_COLOR, shape[control_points_id][point_id],
                                           CONTROL_POINT_RADIUS)
                    else:
                        pygame.draw.circle(self.display, BLACK,
                                           shape[control_points_id][point_id], CONTROL_POINT_RADIUS)

    def _draw_curves(self) -> None:
        """
        Draws all curves from shape
        :return: None
        """
        shape = self.shape.get_shape()
        for control_points_id in range(len(shape)):
            if len(shape[control_points_id]) >= 2:
                curve = bezier(shape[control_points_id], [1 for _ in range(len(shape[control_points_id]))])
                for t in get_optimized_moments(shape[control_points_id]):
                    p = curve(t)
                    if control_points_id == self.shape.get_current_curve_id() and self.ui_state.edit:
                        pygame.draw.circle(self.display, ACTIVE_CURVE_COLOR, (int(p[0]), int(p[1])), 1)
                    else:
                        pygame.draw.circle(self.display, BLACK, (int(p[0]), int(p[1])), 1)
