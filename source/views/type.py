import pygame
import json
import sys
from source.state.view_manager import ViewManager
from source.logic.shape import Shape
from source.logic.caption import Caption
from source.views.constants import BLACK, WHITE, TYPE_HEIGHT
from source.logic.faster_drawing_alg import bezier
from source.logic.optimize_sampling import calc_distance


class Type:
    def __init__(self, display: pygame.surface.Surface, view_manager: ViewManager):
        self.display = display
        self.view_manager = view_manager
        self.caption = Caption()

    def run(self) -> None:
        """
        Typing view
        :return: None
        """
        self.display.fill(WHITE)
        self._draw_line()
        self._event_handler()
        self._draw_letters()

    def _draw_line(self) -> None:
        """
        Draws line that points current typing place
        :return: None
        """
        pygame.draw.line(self.display, BLACK,
                         (self.caption.begin_from, 30), (self.caption.begin_from, TYPE_HEIGHT - 100))
        pygame.draw.line(self.display, BLACK,
                         (self.caption.begin_from + 1, 30), (self.caption.begin_from + 1, TYPE_HEIGHT - 100))

    def _draw_letters(self) -> None:
        """
        Draws all letters from caption
        :return: None
        """
        for letter in self.caption.letters:
            shape = letter
            for control_points_id in range(len(shape)):
                if len(shape[control_points_id]) >= 2:
                    curve = bezier(shape[control_points_id], [1 for _ in range(len(shape[control_points_id]))])
                    dist = int(calc_distance(shape[control_points_id]))
                    for t in range(int(.8 * dist) + 1):
                        t /= .8 * dist
                        p = curve(t)
                        pygame.draw.circle(self.display, BLACK, (int(p[0]), int(p[1])), 1)

    def _event_handler(self) -> None:
        """
        Handles detecting clicking of a key
        :return: None
        """
        wrapper = Shape()
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    print(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.caption.letters) > 0:
                        self.caption.letters.pop(-1)
                        self.caption.begin_from = self.caption.prev_begin_from.pop(-1)
                        if len(self.caption.last_letter) > 1:
                            self.caption.last_letter.pop(-1)
                elif event.key == pygame.K_TAB:
                    self.caption.make_cursive(self.caption.cursive)
                    self.caption.cursive *= -1
                elif keys[pygame.K_z] and keys[pygame.K_RALT]:
                    letter = open('resources/letters_json/ż.json')
                    z = wrapper.load_shape(json.load(letter))
                    if self.caption.last_letter and self.caption.last_letter[-1] == 'j':
                        self.caption.adjust_single_letter(z, 0, .38, -15)
                    else:
                        self.caption.adjust_single_letter(z, 0, .38)
                    self.caption.last_letter.append('ż')
                elif keys[pygame.K_x] and keys[pygame.K_RALT]:
                    letter = open('resources/letters_json/ź.json')
                    z = wrapper.load_shape(json.load(letter))
                    if self.caption.last_letter and self.caption.last_letter[-1] == 'j':
                        self.caption.adjust_single_letter(z, 0, .38, -15)

                    else:
                        self.caption.adjust_single_letter(z, 0, .38)
                    self.caption.last_letter.append('j')
                elif keys[pygame.K_e] and keys[pygame.K_RALT]:
                    letter = open('resources/letters_json/ę.json')
                    e = wrapper.load_shape(json.load(letter))
                    if self.caption.last_letter and self.caption.last_letter[-1] == 'j':
                        self.caption.adjust_single_letter(e, 46, .27, -2)
                    else:
                        self.caption.adjust_single_letter(e, 46, .27)
                    self.caption.last_letter.append('ę')
                elif keys[pygame.K_a] and keys[pygame.K_RALT]:
                    letter = open('resources/letters_json/ą.json')
                    a = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(a, 44, .29)
                    self.caption.last_letter.append('ą')
                elif keys[pygame.K_o] and keys[pygame.K_RALT]:
                    letter = open('resources/letters_json/ó.json')
                    o = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(o, 9, .39)
                    self.caption.last_letter.append('ó')
                elif keys[pygame.K_l] and keys[pygame.K_RALT]:
                    letter = open('resources/letters_json/ł.json')
                    l = wrapper.load_shape(json.load(letter))
                    if self.caption.last_letter and self.caption.last_letter[-1] == 'j':
                        self.caption.adjust_single_letter(l, -25, .4, -20)
                    elif self.caption.last_letter and self.caption.last_letter[-1] in self.caption.adjust_ly:
                        self.caption.adjust_single_letter(l, -25, .4, -25)
                    else:
                        self.caption.adjust_single_letter(l, -25, .4, -15)
                    self.caption.last_letter.append('ł')
                elif keys[pygame.K_s] and keys[pygame.K_RALT]:
                    letter = open('resources/letters_json/ś.json')
                    s = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(s, 25, .33)
                    self.caption.last_letter.append('ś')
                elif keys[pygame.K_c] and keys[pygame.K_RALT]:
                    letter = open('resources/letters_json/ć.json')
                    c = wrapper.load_shape(json.load(letter))
                    if self.caption.last_letter and self.caption.last_letter[-1] == 'j':
                        self.caption.adjust_single_letter(c, 50, .25, -5)
                    else:
                        self.caption.adjust_single_letter(c, 50, .25)
                    self.caption.last_letter.append('ć')
                elif keys[pygame.K_n] and keys[pygame.K_RALT]:
                    letter = open('resources/letters_json/ń.json')
                    n = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(n, 18, .37)
                    self.caption.last_letter.append('ń')
                elif event.key == pygame.K_SPACE:
                    self.caption.letters.append([])
                    self.caption.prev_begin_from.append(self.caption.begin_from)
                    self.caption.begin_from += 50
                    self.caption.last_letter.append('j')
                elif event.key == pygame.K_a:
                    letter = open('resources/letters_json/a.json')
                    a = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(a, 40, .3)
                    self.caption.last_letter.append('a')
                elif event.key == pygame.K_b:
                    letter = open('resources/letters_json/b.json')
                    b = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(b, 4, .32)
                    self.caption.last_letter.append('b')
                elif event.key == pygame.K_c:
                    letter = open('resources/letters_json/c.json')
                    c = wrapper.load_shape(json.load(letter))
                    if self.caption.last_letter and self.caption.last_letter[-1] == 'j':
                        self.caption.adjust_single_letter(c, 50, .25, -5)
                    else:
                        self.caption.adjust_single_letter(c, 50, .25)
                    self.caption.last_letter.append('c')
                elif event.key == pygame.K_d:
                    letter = open('resources/letters_json/d.json')
                    d = wrapper.load_shape(json.load(letter))
                    if self.caption.last_letter and self.caption.last_letter[-1] == 'j':
                        self.caption.adjust_single_letter(d, -2, .36, -2)
                    else:
                        self.caption.adjust_single_letter(d, -2, .36)
                    self.caption.last_letter.append('d')
                elif event.key == pygame.K_e:
                    letter = open('resources/letters_json/e.json')
                    e = wrapper.load_shape(json.load(letter))
                    if self.caption.last_letter and self.caption.last_letter[-1] == 'j':
                        self.caption.adjust_single_letter(e, 46, .27, -2)
                    else:
                        self.caption.adjust_single_letter(e, 46, .27)
                    self.caption.last_letter.append('e')
                elif event.key == pygame.K_f:
                    letter = open('resources/letters_json/f.json')
                    f = wrapper.load_shape(json.load(letter))
                    if self.caption.last_letter and self.caption.last_letter[-1] == 'j':
                        self.caption.adjust_single_letter(f, -8, .5, -10)
                    else:
                        self.caption.adjust_single_letter(f, -8, .5)
                    self.caption.last_letter.append('f')
                elif event.key == pygame.K_g:
                    letter = open('resources/letters_json/g.json')
                    g = wrapper.load_shape(json.load(letter))
                    if self.caption.last_letter and self.caption.last_letter[-1] == 'j':
                        self.caption.adjust_single_letter(g, 18, .5, -5)
                    else:
                        self.caption.adjust_single_letter(g, 18, .5)
                    self.caption.last_letter.append('g')
                elif event.key == pygame.K_h:
                    letter = open('resources/letters_json/h.json')
                    h = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(h, -60, .5)
                    self.caption.last_letter.append('h')
                elif event.key == pygame.K_i:
                    letter = open('resources/letters_json/i.json')
                    i = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(i, -30, 0.45)
                    self.caption.last_letter.append('i')
                elif event.key == pygame.K_j:
                    letter = open('resources/letters_json/j.json')
                    j = wrapper.load_shape(json.load(letter))
                    if len(self.caption.letters) == 0:
                        self.caption.begin_from += 40
                    self.caption.adjust_single_letter(j, -110, 0.8, -35)
                    self.caption.last_letter.append('j')
                elif event.key == pygame.K_k:
                    letter = open('resources/letters_json/k.json')
                    k = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(k, -40, .5)
                    self.caption.last_letter.append('k')
                elif event.key == pygame.K_l:
                    letter = open('resources/letters_json/l.json')
                    l = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(l, -25, .4)
                    self.caption.last_letter.append('l')
                elif event.key == pygame.K_m:
                    letter = open('resources/letters_json/m.json')
                    m = wrapper.load_shape(json.load(letter))
                    if self.caption.last_letter and self.caption.last_letter[-1] in ['a', 'n']:
                        self.caption.adjust_single_letter(m, 18, 0.37, -8)
                    else:
                        self.caption.adjust_single_letter(m, 18, 0.37)
                    self.caption.last_letter.append('m')
                elif event.key == pygame.K_n:
                    letter = open('resources/letters_json/n.json')
                    n = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(n, 18, .37)
                    self.caption.last_letter.append('n')
                elif event.key == pygame.K_o:
                    letter = open('resources/letters_json/o.json')
                    o = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(o, 9, .39)
                    self.caption.last_letter.append('o')
                elif event.key == pygame.K_p:
                    letter = open('resources/letters_json/p.json')
                    p = wrapper.load_shape(json.load(letter))
                    if len(self.caption.letters) == 0:
                        self.caption.begin_from += 40
                    if self.caption.last_letter and self.caption.last_letter[-1] == 'j':
                        self.caption.adjust_single_letter(p, -5, 0.52, -20)
                    elif self.caption.last_letter and self.caption.last_letter[-1] in self.caption.adjust_p:
                        self.caption.adjust_single_letter(p, -5, 0.52, -35)
                    else:
                        self.caption.adjust_single_letter(p, -5, 0.52)
                    self.caption.last_letter.append('p')
                elif event.key == pygame.K_q:
                    letter = open('resources/letters_json/q.json')
                    q = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(q, 15, 0.5)
                    self.caption.last_letter.append('q')
                elif event.key == pygame.K_r:
                    letter = open('resources/letters_json/r.json')
                    r = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(r, 25, .33)
                    self.caption.last_letter.append('r')
                elif event.key == pygame.K_s:
                    letter = open('resources/letters_json/s.json')
                    s = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(s, 25, .33)
                    self.caption.last_letter.append('s')
                elif event.key == pygame.K_t:
                    letter = open('resources/letters_json/t.json')
                    t = wrapper.load_shape(json.load(letter))
                    if self.caption.last_letter and self.caption.last_letter[-1] == 'j':
                        self.caption.adjust_single_letter(t, -32, .45, -15)
                    elif self.caption.last_letter and self.caption.last_letter[-1] in ['b', 'o']:
                        self.caption.adjust_single_letter(t, -32, .45)
                    else:
                        self.caption.adjust_single_letter(t, -32, .45, -10)
                    self.caption.last_letter.append('t')
                elif event.key == pygame.K_u:
                    letter = open('resources/letters_json/u.json')
                    u = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(u, 20, .35)
                    self.caption.last_letter.append('u')
                elif event.key == pygame.K_v:
                    letter = open('resources/letters_json/v.json')
                    v = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(v, 23, .35)
                    self.caption.last_letter.append('v')
                elif event.key == pygame.K_w:
                    letter = open('resources/letters_json/w.json')
                    w = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(w, 18, .37)
                    self.caption.last_letter.append('w')
                elif event.key == pygame.K_x:
                    letter = open('resources/letters_json/x.json')
                    x = wrapper.load_shape(json.load(letter))
                    if self.caption.last_letter and self.caption.last_letter[-1] == 'j':
                        self.caption.adjust_single_letter(x, 10, .38, -20)
                    else:
                        self.caption.adjust_single_letter(x, 10, .38)
                    self.caption.last_letter.append('x')
                elif event.key == pygame.K_y:
                    letter = open('resources/letters_json/y.json')
                    y = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(y, 5, .52)
                    self.caption.last_letter.append('y')
                elif event.key == pygame.K_z:
                    letter = open('resources/letters_json/z.json')
                    z = wrapper.load_shape(json.load(letter))
                    self.caption.adjust_single_letter(z, 0, .38)
                    self.caption.last_letter.append('z')
