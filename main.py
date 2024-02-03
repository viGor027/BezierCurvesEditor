import pygame
import sys
from shape import Shape
from views.constants import WIDTH, HEIGHT, FPS, WHITE, BLACK,\
    ACTIVE_POINT_COLOR, ACTIVE_CURVE_COLOR, BUTTON_INACTIVE_COLOR, \
    BUTTON_COLOR, CONTROL_POINT_RADIUS

# Initialize Pygame
pygame.init()

# Constants


# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bezier Curve Editor")
clock = pygame.time.Clock()



# Function to perform de Casteljau's algorithm
def de_casteljau(t, points):
    if len(points) == 1:
        return points[0]
    else:
        new_points = []
        for i in range(len(points) - 1):
            x = (1 - t) * points[i][0] + t * points[i + 1][0]
            y = (1 - t) * points[i][1] + t * points[i + 1][1]
            new_points.append((x, y))
        return de_casteljau(t, new_points)


smallfont = pygame.font.SysFont('Corbel', 14)

text = smallfont.render('Nowa prosta', True, BLACK)
text2 = smallfont.render('Siatka', True, BLACK)
text3 = smallfont.render('Zapisz', True, BLACK)
text5 = smallfont.render('Edycja On ', True, BLACK)
text6 = smallfont.render('Edycja Off', True, BLACK)
text7 = smallfont.render('Wyswietl litere', True, BLACK)

letter_img = pygame.image.load('letters_raw_extracted/n.png')
# letter_img = pygame.image.load('dummy_background.png')

# Main game loop
running = True
dragging = False
dragged_point_index = None
draw_grid = True
edit = True
show_letter = True

current_curve_id = 0
prev_edited_curve_id = None

letter = Shape()

# read curves from file
# f = open('letters_json/n.json')
# all_curves = json.load(f)
# current_curve_id = len(all_curves) - 1
# prev_edited_curve_id = len(all_curves) - 2

# start with no curves
all_curves = [[]]

target_img_size = None
target_img_rect = None

img_x, img_y = 0, 0
print(type(screen))
while running:
    screen.fill(WHITE)
    if show_letter:
        screen.blit(letter_img, (img_x, img_y))

    if draw_grid:
        pygame.draw.line(screen, (0, 0, 0), (WIDTH / 2 - 1, 0), (WIDTH / 2 - 1, HEIGHT))
        pygame.draw.line(screen, (0, 0, 0), (WIDTH / 2 + 1, 0), (WIDTH / 2 + 1, HEIGHT))

        pygame.draw.line(screen, (0, 0, 0), (0, HEIGHT / 2 - 1), (WIDTH, HEIGHT / 2 - 1))
        pygame.draw.line(screen, (0, 0, 0), (0, HEIGHT / 2 + 1), (WIDTH, HEIGHT / 2 + 1))

        for i in range(0, WIDTH, 20):
            if i == 180 or i == 620:
                pygame.draw.line(screen, (220, 20, 60), (i, 0), (i, HEIGHT))
            else:
                pygame.draw.line(screen, (0, 0, 0), (i, 0), (i, HEIGHT))

        for i in range(0, HEIGHT, 20):
            if i == 20 or i == 460 or i == 580:
                pygame.draw.line(screen, (220, 20, 60), (0, i), (WIDTH, i))
            else:
                pygame.draw.line(screen, (0, 0, 0), (0, i), (WIDTH, i))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and 10 <= mouse[0] <= 85 and 10 <= mouse[1] <= 50:  # kliknięto "Nowa prosta"
                letter.new_curve()
            elif event.button == 1 and 95 <= mouse[0] <= 170 and 10 <= mouse[1] <= 50:  # kliknieto "siatka"
                draw_grid = not draw_grid
            elif event.button == 1 and 10 <= mouse[0] <= 85 and 60 <= mouse[1] <= 100:  # kliknieto "zapisz"
                letter.save('nowa.json')
            elif event.button == 1 and 95 <= mouse[0] <= 170 and 60 <= mouse[1] <= 100:  # kliknieto "tryb edycji"
                edit = not edit
            elif event.button == 1 and 10 <= mouse[0] <= 170 and 120 <= mouse[1] <= 150:
                show_letter = not show_letter
            elif event.button == 1 and edit:  # Left mouse button
                letter.add_point(event.pos)
            elif event.button == 3 and edit:  # Right mouse button
                closest_index = letter.get_closest_point(event.pos)[0]
                if closest_index is not None:
                    dragging = True
                    dragged_point_index = closest_index
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Right mouse button
                dragging = False
                dragged_point_index = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and edit:
                letter.delete_point(pygame.mouse.get_pos())
            elif event.key == pygame.K_e:
                letter.switch_curve(pygame.mouse.get_pos())
            elif event.key == pygame.K_i:
                img_x, img_y = pygame.mouse.get_pos()
            elif event.key == pygame.K_n:
                letter.c0_connection()

    mouse = pygame.mouse.get_pos()
    pygame.draw.rect(screen, BUTTON_COLOR, [10, 10, 75, 40])  # nowa prosta button
    if draw_grid:  # siatka button
        pygame.draw.rect(screen, BUTTON_COLOR, [95, 10, 75, 40])
    else:
        pygame.draw.rect(screen, BUTTON_INACTIVE_COLOR, [95, 10, 75, 40])
    pygame.draw.rect(screen, BUTTON_COLOR, [10, 60, 75, 40])  # zapisz button
    # pygame.draw.rect(screen, BUTTON_COLOR, [95, 60, 75, 40])  # edytuj button
    if edit:  # tryb edycji button
        pygame.draw.rect(screen, BUTTON_COLOR, [95, 60, 75, 40])
    else:
        pygame.draw.rect(screen, BUTTON_INACTIVE_COLOR, [95, 60, 75, 40])

    if show_letter:
        pygame.draw.rect(screen, BUTTON_COLOR, [10, 110, 160, 40])
    else:
        pygame.draw.rect(screen, BUTTON_INACTIVE_COLOR, [10, 110, 160, 40])

    if dragging and pygame.mouse.get_pressed()[2]:  # Right mouse button held down
        print(dragged_point_index)
        letter.update_point(dragged_point_index, pygame.mouse.get_pos())

    shape = letter.get_shape()
    # Draw control points
    if edit:
        for control_points_id in range(len(shape)):
            for point_id in range(len(shape[control_points_id])):
                if control_points_id == letter.get_current_curve_id() and edit:
                    pygame.draw.circle(screen, ACTIVE_POINT_COLOR, shape[control_points_id][point_id],
                                       CONTROL_POINT_RADIUS)
                else:
                    pygame.draw.circle(screen, BLACK, shape[control_points_id][point_id], CONTROL_POINT_RADIUS)

    # Draw Bezier curve using de Casteljau's algorithm
    for control_points_id in range(len(shape)):
        if len(shape[control_points_id]) >= 2:
            for t in range(0, 80*len(shape[control_points_id])+1):
                t /= 80 * len(shape[control_points_id])
                p = de_casteljau(t, shape[control_points_id])
                if control_points_id == letter.get_current_curve_id() and edit:
                    pygame.draw.circle(screen, ACTIVE_CURVE_COLOR, (int(p[0]), int(p[1])), 1)
                else:
                    pygame.draw.circle(screen, BLACK, (int(p[0]), int(p[1])), 1)

    screen.blit(text, (12, 23))
    screen.blit(text2, (12 + 105, 23))
    screen.blit(text3, (12 + 15, 23 + 50))
    if edit:
        #  [95, 60, 75, 40]
        screen.blit(text5, (12 + 95, 23 + 50))
    else:
        screen.blit(text6, (12 + 95, 23 + 50))
    screen.blit(text7, (12 + 39, 23 + 100))

    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
