import pygame
import sys
from tkinter import Tk, filedialog
from views.constants import WIDTH, HEIGHT, WHITE, BUTTON_COLOR, BLACK
from state.state_manager import StateManager


class Start:
    def __init__(self, display: pygame.surface.Surface, state_manager: StateManager):
        self.display = display
        self.state_manager = state_manager

    def run(self):
        """
        Start view
        :return:  None
        """
        self.display.fill(WHITE)
        self._draw_buttons()
        self._draw_text()

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('mouse')
                if event.button == 1 and \
                        WIDTH // 2 - 250 / 2 <= mouse[0] <= WIDTH // 2 - 250 / 2 + 250 and \
                        HEIGHT // 4 <= mouse[1] <= HEIGHT // 4 + 70:
                    # open editor
                    print(bg_path, shape_path)
                    self.state_manager.set_state('edit', bg_path, shape_path)
                elif event.button == 1 and \
                        WIDTH // 2 - 250 / 2 + 75 <= mouse[0] <= WIDTH // 2 - 250 / 2 + 75 + 250 and \
                        HEIGHT // 4 + (70 + 15) * 1 <= mouse[1] <= HEIGHT // 4 + (70 + 15) * 1 + 70:
                    # load background
                    bg_path = Start._open_file_dialog('image')
                    print(bg_path)
                elif event.button == 1 and \
                        WIDTH // 2 - 250 / 2 + 75 <= mouse[0] <= WIDTH // 2 - 250 / 2 + 75 + 250 and \
                        HEIGHT // 4 + (70 + 15) * 2 <= mouse[1] <= HEIGHT // 4 + (70 + 15) * 2 + 70:
                    # load_shape
                    shape_path = Start._open_file_dialog('json')
                    print(shape_path)

    def _draw_buttons(self):
        pygame.draw.rect(self.display, BUTTON_COLOR, [WIDTH // 2 - 250 / 2, HEIGHT // 4, 250, 70])  # Open editor
        pygame.draw.rect(self.display, BUTTON_COLOR,
                         [WIDTH // 2 - 250 / 2, HEIGHT // 4 + (70 + 15) * 1, 250, 70])  # Read image
        pygame.draw.rect(self.display, BUTTON_COLOR,
                         [WIDTH // 2 - 250 / 2, HEIGHT // 4 + (70 + 15) * 2, 250, 70])  # Read shape

    def _draw_text(self):
        smallfont = pygame.font.SysFont('Bahnschrift', 18)
        open_editor_text = smallfont.render('Open editor', True, BLACK)
        load_background_text = smallfont.render('Load background', True, BLACK)
        load_shape_text = smallfont.render('Load shape', True, BLACK)

        self.display.blit(open_editor_text, (WIDTH // 2 - 250 / 2 + 75, HEIGHT // 4 + 25))
        self.display.blit(load_background_text, (WIDTH // 2 - 250 / 2 + 55, HEIGHT // 4 + (70 + 15) * 1 + 25))
        self.display.blit(load_shape_text, (WIDTH // 2 - 250 / 2 + 75, HEIGHT // 4 + (70 + 15) * 2 + 25))

    @staticmethod
    def _open_file_dialog(ftype: str):
        """
        Function for loading background and shape from file
        :param ftype:
        :return:
        """
        file_type = {
            'json': ("JSON files", "*.json"),
            'image': ("Image files", "*.png;*.jpg;*.jpeg;*.gif")
        }
        root = Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(filetypes=[file_type[ftype]])
        root.destroy()  # Close the Tkinter window
        return file_path
