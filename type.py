import pygame
import sys
import json
from math import tan, radians

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1400, 275
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
JUMP_ON_LETTER = 300

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bezier Curve Editor")
clock = pygame.time.Clock()


def tilt(points, shear_factor):
    sheared_points = [(x + y * shear_factor, y) for x, y in points]
    return sheared_points


def make_cursive(side):
    straight_letters = all_letters.copy()
    for letter_id in range(len(all_letters)):
        for control_points_id in range(len(all_letters[letter_id])):
            deg = tan(radians(side * -15))
            all_letters[letter_id][control_points_id] = tilt(all_letters[letter_id][control_points_id], deg)
    return straight_letters


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


begin_from = 40


# podawać kopię letter lub wczytywać każdorazowo
def draw_letter(letter, shift_y, scale, shift_x=0):
    global begin_from
    prev_begin_from.append(begin_from)
    max_right = 0
    max_left = WIDTH
    for curve_id in range(len(letter)):
        for point_id in range(len(letter[curve_id])):
            if letter[curve_id][point_id][0] < max_left:
                max_left = letter[curve_id][point_id][0]
            elif letter[curve_id][point_id][0] > max_right:
                max_right = letter[curve_id][point_id][0]

            letter[curve_id][point_id][0] = letter[curve_id][point_id][0] * scale + shift_x
            letter[curve_id][point_id][1] = letter[curve_id][point_id][1] * scale + shift_y

    max_left *= scale
    diff = begin_from - max_left
    max_right = max_right * scale + diff
    for curve_id in range(len(letter)):
        for point_id in range(len(letter[curve_id])):
            letter[curve_id][point_id][0] += diff
    begin_from = max_right + 5 + shift_x
    all_letters.append(letter.copy())
    return prev_begin_from


letter = open('letters_json/a.json')
a = json.load(letter)
all_letters = []
letters_copy = []

adjust_p = ['a', 'ą', 'b', 'c', 'ć',
            'd', 'e', 'ę', 'h', 'i',
            'k', 'l', 'ł', 'm', 'n',
            'ń', 'o', 'ó', 'u', 'r',
            's', 'ś', 't', 'w', 'x',
            'z', 'ź', 'ż']

cursive = 1
running = True
pointer_type = 10
pointer_shift = -75
prev_letter_max_right = 0
prev_begin_from = []
last_letter = []

while running:
    screen.fill(WHITE)
    #
    # # dolna linia pomocnicza
    # pygame.draw.line(screen, BLACK, (0, HEIGHT - 105), (WIDTH, HEIGHT - 105))
    #
    # # górna linia pomocnicza
    # pygame.draw.line(screen, BLACK, (0, HEIGHT - 190), (WIDTH, HEIGHT - 190))

    pygame.draw.line(screen, BLACK, (begin_from, 30), (begin_from, HEIGHT-100))
    pygame.draw.line(screen, BLACK, (begin_from + 1, 30), (begin_from + 1, HEIGHT-100))

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                print(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(all_letters) > 0:
                    all_letters.pop(-1)
                    begin_from = prev_begin_from.pop(-1)
                    if len(last_letter) > 1:
                        last_letter.pop(-1)
            elif event.key == pygame.K_TAB:
                make_cursive(cursive)
                cursive *= -1
            elif keys[pygame.K_z] and keys[pygame.K_RALT]:
                letter = open('letters_json/ż.json')
                z = json.load(letter)
                if last_letter and last_letter[-1] == 'j':
                    draw_letter(z, 0, .38, -15)
                else:
                    draw_letter(z, 0, .38)
                last_letter.append('ż')
            elif keys[pygame.K_x] and keys[pygame.K_RALT]:
                letter = open('letters_json/ź.json')
                z = json.load(letter)
                if last_letter and last_letter[-1] == 'j':
                    draw_letter(z, 0, .38, -15)

                else:
                    draw_letter(z, 0, .38)
                last_letter.append('j')
            elif keys[pygame.K_e] and keys[pygame.K_RALT]:
                letter = open('letters_json/ę.json')
                e = json.load(letter)
                if last_letter and last_letter[-1] == 'j':
                    draw_letter(e, 46, .27, -2)
                else:
                    draw_letter(e, 46, .27)
                last_letter.append('ę')
            elif keys[pygame.K_a] and keys[pygame.K_RALT]:
                letter = open('letters_json/ą.json')
                a = json.load(letter)
                draw_letter(a, 44, .29)
                last_letter.append('ą')
            elif keys[pygame.K_o] and keys[pygame.K_RALT]:
                letter = open('letters_json/ó.json')
                o = json.load(letter)
                draw_letter(o, 9, .39)
                last_letter.append('ó')
            elif keys[pygame.K_l] and keys[pygame.K_RALT]:
                letter = open('letters_json/ł.json')
                l = json.load(letter)
                if last_letter and last_letter[-1] == 'j':
                    draw_letter(l, -25, .4, -20)
                else:
                    draw_letter(l, -25, .4, -15)
                last_letter.append('ł')
            elif keys[pygame.K_s] and keys[pygame.K_RALT]:
                letter = open('letters_json/ś.json')
                s = json.load(letter)
                draw_letter(s, 25, .33)
                last_letter.append('ś')
            elif keys[pygame.K_c] and keys[pygame.K_RALT]:
                letter = open('letters_json/ć.json')
                c = json.load(letter)
                if last_letter and last_letter[-1] == 'j':
                    draw_letter(c, 50, .25, -5)
                else:
                    draw_letter(c, 50, .25)
                last_letter.append('ć')
            elif keys[pygame.K_n] and keys[pygame.K_RALT]:
                letter = open('letters_json/ń.json')
                n = json.load(letter)
                draw_letter(n, 18, .37)
                last_letter.append('ń')
            elif event.key == pygame.K_SPACE:
                all_letters.append([])
                prev_begin_from.append(begin_from)
                begin_from += 50
                last_letter.append('j')
            elif event.key == pygame.K_a:
                letter = open('letters_json/a.json')
                a = json.load(letter)
                draw_letter(a, 40, .3)
                last_letter.append('a')
            elif event.key == pygame.K_b:
                letter = open('letters_json/b.json')
                b = json.load(letter)
                draw_letter(b, 4, .32)
                last_letter.append('b')
            elif event.key == pygame.K_c:
                letter = open('letters_json/c.json')
                c = json.load(letter)
                if last_letter and last_letter[-1] == 'j':
                    draw_letter(c, 50, .25, -5)
                else:
                    draw_letter(c, 50, .25)
                last_letter.append('c')
            elif event.key == pygame.K_d:
                letter = open('letters_json/d.json')
                d = json.load(letter)
                if last_letter and last_letter[-1] == 'j':
                    draw_letter(d, -2, .36, -2)
                else:
                    draw_letter(d, -2, .36)
                last_letter.append('d')
            elif event.key == pygame.K_e:
                letter = open('letters_json/e.json')
                e = json.load(letter)
                if last_letter and last_letter[-1] == 'j':
                    draw_letter(e, 46, .27, -2)
                else:
                    draw_letter(e, 46, .27)
                last_letter.append('e')
            elif event.key == pygame.K_f:
                letter = open('letters_json/f.json')
                f = json.load(letter)
                if last_letter and last_letter[-1] == 'j':
                    draw_letter(f, -8, .5, -10)
                else:
                    draw_letter(f, -8, .5)
                last_letter.append('f')
            elif event.key == pygame.K_g:
                letter = open('letters_json/g.json')
                g = json.load(letter)
                if last_letter and last_letter[-1] == 'j':
                    draw_letter(g, 18, .5, -5)
                else:
                    draw_letter(g, 18, .5)
                last_letter.append('g')
            elif event.key == pygame.K_h:
                letter = open('letters_json/h.json')
                h = json.load(letter)
                draw_letter(h, -60, .5)
                last_letter.append('h')
            elif event.key == pygame.K_i:
                letter = open('letters_json/i.json')
                i = json.load(letter)
                draw_letter(i, -30, 0.45)
                last_letter.append('i')
            elif event.key == pygame.K_j:
                letter = open('letters_json/j.json')
                j = json.load(letter)
                if len(all_letters) == 0:
                    begin_from += 40
                draw_letter(j, -110, 0.8, -35)
                last_letter.append('j')
            elif event.key == pygame.K_k:
                letter = open('letters_json/k.json')
                k = json.load(letter)
                draw_letter(k, -40, .5)
                last_letter.append('k')
            elif event.key == pygame.K_l:
                letter = open('letters_json/l.json')
                l = json.load(letter)
                draw_letter(l, -25, .4)
                last_letter.append('l')
            elif event.key == pygame.K_m:
                letter = open('letters_json/m.json')
                m = json.load(letter)
                if last_letter and last_letter[-1] in ['a', 'n']:
                    draw_letter(m, 18, 0.37, -8)
                else:
                    draw_letter(m, 18, 0.37)
                last_letter.append('m')
            elif event.key == pygame.K_n:
                letter = open('letters_json/n.json')
                n = json.load(letter)
                draw_letter(n, 18, .37)
                last_letter.append('n')
            elif event.key == pygame.K_o:
                letter = open('letters_json/o.json')
                o = json.load(letter)
                draw_letter(o, 9, .39)
                last_letter.append('o')
            elif event.key == pygame.K_p:
                letter = open('letters_json/p.json')
                p = json.load(letter)
                if len(all_letters) == 0:
                    begin_from += 40
                if last_letter and last_letter[-1] == 'j':
                    draw_letter(p, -5, 0.52, -20)
                elif last_letter and last_letter[-1] in adjust_p:
                    draw_letter(p, -5, 0.52, -35)
                else:
                    draw_letter(p, -5, 0.52)
                last_letter.append('p')
            elif event.key == pygame.K_q:
                letter = open('letters_json/q.json')
                q = json.load(letter)
                draw_letter(q, 15, 0.5)
                last_letter.append('q')
            elif event.key == pygame.K_r:
                letter = open('letters_json/r.json')
                r = json.load(letter)
                draw_letter(r, 25, .33)
                last_letter.append('r')
            elif event.key == pygame.K_s:
                letter = open('letters_json/s.json')
                s = json.load(letter)
                draw_letter(s, 25, .33)
                last_letter.append('s')
            elif event.key == pygame.K_t:
                letter = open('letters_json/t.json')
                t = json.load(letter)
                if last_letter and last_letter[-1] == 'j':
                    draw_letter(t, -32, .45, -15)
                elif last_letter and last_letter[-1] in ['b', 'o']:
                    draw_letter(t, -32, .45)
                else:
                    draw_letter(t, -32, .45, -10)
                last_letter.append('t')
            elif event.key == pygame.K_u:
                letter = open('letters_json/u.json')
                u = json.load(letter)
                draw_letter(u, 20, .35)
                last_letter.append('u')
            elif event.key == pygame.K_v:
                letter = open('letters_json/v.json')
                v = json.load(letter)
                draw_letter(v, 23, .35)
                last_letter.append('v')
            elif event.key == pygame.K_w:
                letter = open('letters_json/w.json')
                w = json.load(letter)
                draw_letter(w, 18, .37)
                last_letter.append('w')
            elif event.key == pygame.K_x:
                letter = open('letters_json/x.json')
                x = json.load(letter)
                if last_letter and last_letter[-1] == 'j':
                    draw_letter(x, 10, .38, -20)
                else:
                    draw_letter(x, 10, .38)
                last_letter.append('x')
            elif event.key == pygame.K_y:
                letter = open('letters_json/y.json')
                y = json.load(letter)
                draw_letter(y, 5, .52)
                last_letter.append('y')
            elif event.key == pygame.K_z:
                letter = open('letters_json/z.json')
                z = json.load(letter)
                draw_letter(z, 0, .38)
                last_letter.append('z')

    # Draw Bezier curve using de Casteljau's algorithm
    for all_curves in all_letters:
        for control_points_id in range(len(all_curves)):
            if len(all_curves[control_points_id]) >= 2:
                for t in range(0, 20 * len(all_curves[control_points_id]) + 1):
                    t /= 20 * len(all_curves[control_points_id])
                    p = de_casteljau(t, all_curves[control_points_id])
                    pygame.draw.circle(screen, BLACK, (int(p[0]), int(p[1])), 1)

    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
