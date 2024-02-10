import pygame
import sys
from tkinter import Tk, filedialog
from source.views.constants import WIDTH, HEIGHT, WHITE, BUTTON_COLOR, BLACK
from source.state.view_manager import ViewManager


class Start:
    def __init__(self, display: pygame.surface.Surface, view_manager: ViewManager):
        self.display = display
        self.view_manager = view_manager

    def run(self) -> None:
        """
        Start view
        :return:  None
        """
        self.display.fill(WHITE)
        self._draw_buttons()
        self._draw_text()
        self._event_handler()

    def _draw_buttons(self) -> None:
        """
        Draws UI buttons
        :return: None
        """
        pygame.draw.rect(self.display, BUTTON_COLOR, [WIDTH // 2 - 250 / 2, HEIGHT // 4, 250, 70])  # Open editor
        pygame.draw.rect(self.display, BUTTON_COLOR,
                         [WIDTH // 2 - 250 / 2, HEIGHT // 4 + (70 + 15) * 1, 250, 70])  # Read image
        pygame.draw.rect(self.display, BUTTON_COLOR,
                         [WIDTH // 2 - 250 / 2, HEIGHT // 4 + (70 + 15) * 2, 250, 70])  # Read shape

    def _draw_text(self) -> None:
        """
        Displays text on UI buttons
        :return: None
        """
        smallfont = pygame.font.SysFont('Bahnschrift', 18)
        open_editor_text = smallfont.render('Open editor', True, BLACK)
        load_background_text = smallfont.render('Load background', True, BLACK)
        load_shape_text = smallfont.render('Load shape', True, BLACK)

        self.display.blit(open_editor_text, (WIDTH // 2 - 250 / 2 + 75, HEIGHT // 4 + 25))
        self.display.blit(load_background_text, (WIDTH // 2 - 250 / 2 + 55, HEIGHT // 4 + (70 + 15) * 1 + 25))
        self.display.blit(load_shape_text, (WIDTH // 2 - 250 / 2 + 75, HEIGHT // 4 + (70 + 15) * 2 + 25))

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and \
                        WIDTH // 2 - 250 / 2 <= mouse[0] <= WIDTH // 2 - 250 / 2 + 250 and \
                        HEIGHT // 4 <= mouse[1] <= HEIGHT // 4 + 70:
                    self.view_manager.set_state('edit')
                elif event.button == 1 and \
                        WIDTH // 2 - 250 / 2 + 75 <= mouse[0] <= WIDTH // 2 - 250 / 2 + 75 + 250 and \
                        HEIGHT // 4 + (70 + 15) * 1 <= mouse[1] <= HEIGHT // 4 + (70 + 15) * 1 + 70:
                    bg_path = Start._open_file_dialog('image')
                    self.view_manager.set_bg_path(bg_path)
                elif event.button == 1 and \
                        WIDTH // 2 - 250 / 2 + 75 <= mouse[0] <= WIDTH // 2 - 250 / 2 + 75 + 250 and \
                        HEIGHT // 4 + (70 + 15) * 2 <= mouse[1] <= HEIGHT // 4 + (70 + 15) * 2 + 70:
                    shape_path = Start._open_file_dialog('json')
                    self.view_manager.set_shape_path(shape_path)

    @staticmethod
    def _open_file_dialog(ftype: str) -> str:
        """
        Function for loading background and shape from a file
        :param ftype: specifies whether we load background(image) or shape(json)
        :return: path to a file
        """
        file_type = {
            'json': ("JSON files", "*.json"),
            'image': ("Image files", "*.png;*.jpg;*.jpeg;*.gif")
        }
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(filetypes=[file_type[ftype]])
        root.destroy()
        return file_path
