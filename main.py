import pygame
import sys
import json

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ACTIVE_POINT_COLOR = (202, 3, 252)
ACTIVE_CURVE_COLOR = (3, 252, 177)
BUTTON_INACTIVE_COLOR = (158, 5, 56)
BUTTON_COLOR = (3, 252, 181)
CONTROL_POINT_RADIUS = 3

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


# Function to find the index of the closest control point
def find_closest_point(mouse_pos, current_curve=None):
    min_distance = float('inf')
    closest_index = None
    curve_id = None
    if current_curve:
        for i, point in enumerate(all_curves[current_curve]):
            distance = ((mouse_pos[0] - point[0]) ** 2 + (mouse_pos[1] - point[1]) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_index = i
        return closest_index, current_curve
    else:
        for arr_id, control_points in enumerate(all_curves):
            for i, point in enumerate(control_points):
                distance = ((mouse_pos[0] - point[0]) ** 2 + (mouse_pos[1] - point[1]) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_index = i
                    curve_id = arr_id
        return closest_index, curve_id


smallfont = pygame.font.SysFont('Corbel', 14)

text = smallfont.render('Nowa prosta', True, BLACK)
text2 = smallfont.render('Siatka', True, BLACK)
text3 = smallfont.render('Zapisz', True, BLACK)
text4 = smallfont.render('Zmien prostą', True, BLACK)
text5 = smallfont.render('Edycja On ', True, BLACK)
text6 = smallfont.render('Edycja Off', True, BLACK)
text7 = smallfont.render('Wyswietl litere', True, BLACK)

letter_img = pygame.image.load('letters_raw_extracted/p.png')

# Main game loop
running = True
dragging = False
dragged_point_index = None
dragged_point_curve_id = None
draw_grid = True
edit = False
show_letter = True

current_curve_id = 0
prev_edited_curve_id = None

# read curves from file
# f = open('test.json')
# f = open('letters_json/p.json')
# all_curves = json.load(f)
# current_curve_id = len(all_curves) - 1
# prev_edited_curve_id = len(all_curves) - 2

# start with no curves
all_curves = [[]]

target_img_size = None
target_img_rect = None

img_x, img_y = 0, 0

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
                current_curve_id += 1
                all_curves.append([])
            elif event.button == 1 and 95 <= mouse[0] <= 170 and 10 <= mouse[1] <= 50:  # kliknieto "siatka"
                draw_grid = not draw_grid
            elif event.button == 1 and 10 <= mouse[0] <= 85 and 60 <= mouse[1] <= 100:  # kliknieto "zapisz"
                with open('p.json', 'w', encoding='utf-8') as f:
                    json.dump(all_curves, f, ensure_ascii=False, indent=4)
            elif event.button == 1 and 95 <= mouse[0] <= 170 and 60 <= mouse[1] <= 100:  # kliknieto "zmien prosta"
                edit = True
            elif event.button == 1 and 10 <= mouse[0] <= 170 and 110 <= mouse[1] <= 150:  # kliknieto "tryb edycji"
                if current_curve_id is not None:
                    prev_edited_curve_id = current_curve_id
                    current_curve_id = None
                else:
                    current_curve_id = prev_edited_curve_id
            elif event.button == 1 and 10 <= mouse[0] <= 170 and 160 <= mouse[1] <= 200:
                show_letter = not show_letter
            elif event.button == 1 and current_curve_id is not None:  # Left mouse button
                if len(all_curves) == 0:
                    all_curves.append([])
                    current_curve_id += 1
                    prev_edited_curve_id += 1
                all_curves[current_curve_id].append(event.pos)
            elif event.button == 3 and current_curve_id is not None:  # Right mouse button
                closest_index, closest_curve_id = find_closest_point(event.pos)
                if closest_index is not None:
                    dragging = True
                    dragged_point_index = closest_index
                    dragged_point_curve_id = closest_curve_id
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Right mouse button
                dragging = False
                dragged_point_index = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and current_curve_id is not None:
                closest_index, closest_curve_id = find_closest_point(pygame.mouse.get_pos(), current_curve_id)
                if closest_curve_id is not None and closest_index is not None:
                    all_curves[closest_curve_id].pop(closest_index)
                    if len(all_curves[current_curve_id]) == 0:
                        all_curves.pop(current_curve_id)
                        prev_edited_curve_id = len(all_curves) - 2
                        current_curve_id = len(all_curves) - 1
            elif event.key == pygame.K_e and edit:
                prev_edited_curve_id = current_curve_id
                _, current_curve_id = find_closest_point(pygame.mouse.get_pos())
                edit = False
            elif event.key == pygame.K_i:
                img_x, img_y = pygame.mouse.get_pos()
            elif event.key == pygame.K_n:

                if (prev_edited_curve_id is None and len(all_curves[current_curve_id]) > 0) or \
                   (prev_edited_curve_id is not None and len(all_curves[prev_edited_curve_id]) > 0):

                    point_to_copy = all_curves[current_curve_id][-1]
                    prev_edited_curve_id = current_curve_id
                    current_curve_id = len(all_curves)
                    all_curves.append([])
                    all_curves[current_curve_id].append(all_curves[prev_edited_curve_id][-1])

    mouse = pygame.mouse.get_pos()
    pygame.draw.rect(screen, BUTTON_COLOR, [10, 10, 75, 40])  # nowa prosta button
    if draw_grid:  # siatka button
        pygame.draw.rect(screen, BUTTON_COLOR, [95, 10, 75, 40])
    else:
        pygame.draw.rect(screen, BUTTON_INACTIVE_COLOR, [95, 10, 75, 40])
    pygame.draw.rect(screen, BUTTON_COLOR, [10, 60, 75, 40])  # zapisz button
    pygame.draw.rect(screen, BUTTON_COLOR, [95, 60, 75, 40])  # edytuj button
    if current_curve_id is not None:  # tryb edycji button
        pygame.draw.rect(screen, BUTTON_COLOR, [10, 110, 160, 40])
    else:
        pygame.draw.rect(screen, BUTTON_INACTIVE_COLOR, [10, 110, 160, 40])

    if show_letter:
        pygame.draw.rect(screen, BUTTON_COLOR, [10, 160, 160, 40])
    else:
        pygame.draw.rect(screen, BUTTON_INACTIVE_COLOR, [10, 160, 160, 40])

    if dragging and pygame.mouse.get_pressed()[2]:  # Right mouse button held down
        all_curves[dragged_point_curve_id][dragged_point_index] = pygame.mouse.get_pos()

    # Draw control points
    if current_curve_id is not None:
        for control_points_id in range(len(all_curves)):
            for point_id in range(len(all_curves[control_points_id])):
                if control_points_id == current_curve_id:
                    pygame.draw.circle(screen, ACTIVE_POINT_COLOR, all_curves[control_points_id][point_id],
                                       CONTROL_POINT_RADIUS)
                else:
                    pygame.draw.circle(screen, BLACK, all_curves[control_points_id][point_id], CONTROL_POINT_RADIUS)

    # Draw Bezier curve using de Casteljau's algorithm
    for control_points_id in range(len(all_curves)):
        if len(all_curves[control_points_id]) >= 2:
            for t in range(0, 80*len(all_curves[control_points_id])+1):
                t /= 80 * len(all_curves[control_points_id])
                p = de_casteljau(t, all_curves[control_points_id])
                if control_points_id == current_curve_id:
                    pygame.draw.circle(screen, ACTIVE_CURVE_COLOR, (int(p[0]), int(p[1])), 1)
                else:
                    pygame.draw.circle(screen, BLACK, (int(p[0]), int(p[1])), 1)

    screen.blit(text, (12, 23))
    screen.blit(text2, (12 + 105, 23))
    screen.blit(text3, (12 + 15, 23 + 50))
    screen.blit(text4, (12 + 83, 23 + 50))
    if current_curve_id is not None:
        screen.blit(text5, (12 + 48, 23 + 100))
    else:
        screen.blit(text6, (12 + 48, 23 + 100))
    screen.blit(text7, (12 + 39, 23 + 150))

    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
