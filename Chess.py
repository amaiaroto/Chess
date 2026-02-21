# Credits and Attributes
# credit to rizal2109 on flaticon.com for chess-icon.png
# credit to all the authors of the unused assets

import keyboard as kb
import os
import sys
from contextlib import redirect_stdout

from Board import Board

bg_color = (183, 255, 183)
title_screen = True
board = None

with redirect_stdout(open(os.devnull, 'w')):
    import pygame as pg

from Screen import Screen
from Pieces import Piece

pg.init()

screen = Screen(pg, 800, 800).screen
button_font = pg.font.Font('static/NotoSansSymbols-Bold.ttf', 72)
button_font2 = pg.font.SysFont('Segoe UI Symbol', 52)
pg.display.set_icon(pg.image.load('chess-icon.png'))
pg.display.set_caption('Chess')


class Button:
    def __init__(self, x, y, w, h, text, font, color, hover_color):
        self.rect = pg.Rect(x, y, w, h)
        self.text = font.render(self.parse(text), True, (0, 0, 0))
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse = pg.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse) else self.color
        pg.draw.rect(screen, current_color, self.rect, border_radius=8)

        # center text inside button
        text_rect = self.text.get_rect(center=self.rect.center)
        screen.blit(self.text, text_rect)

    def clicked(self):
        """
        get and return the cursor
        if the cursor is touching the button, return True and True
        :return:
        """

        mouse = pg.mouse.get_pos()
        return self.rect.collidepoint(mouse) and pg.mouse.get_pressed()[0]

    def parse(self, text: str, hint: str | list = '[]'):
        result = ''
        con = False

        for c in text:
            if c == '\\':
                con = True

            if c == hint[0] and not con:
                ...

        return text


def exit_chess(code: int | str = 0):
    pg.quit()
    sys.exit(code)


def start_chess():
    global title_screen
    title_screen = False
    return title_screen


while True:
    for event in pg.event.get():
        if not title_screen and event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            print(board.flag_valid_moves(x, y))

        if event.type == pg.QUIT:
            exit_chess()

    screen.fill(bg_color)

    if title_screen:
        if kb.is_pressed('esc'):
            exit_chess()

        if kb.is_pressed('shift+alt+backspace'):
            ...

        text = pg.font.Font('DejaVuSans.ttf', 138)

        chars = [text.render(i, False, (0, 0, 0) if 'Ch♞s'.index(i) % 2 == 0 else (255, 255, 255)) for i in
                 list('Ch♞s')]
        chars.append(text.render('s', False, (0, 0, 0)))

        play_button = Button(305, 400, 190, 100, 'PLAY', button_font,
                             (0, 255, 0), (0, 205, 0))
        quit_button = Button(305, 525, 190, 100, 'QUIT', button_font,
                             (255, 0, 0), (205, 0, 0))
        play_button.draw(screen)
        quit_button.draw(screen)

        if play_button.clicked() or kb.is_pressed('enter'):
            board = Board((8, 8), screen, pg)
            start_chess()

        elif quit_button.clicked():
            exit_chess()

        text_pos = (800 - sum(t.get_width() for t in chars)) // 2
        for t in chars:
            screen.blit(t, (text_pos, 300 - t.get_rect().centery))
            text_pos += t.get_size()[0] // 1.1

    else:
        back_button = Button(10, 10, 53, 53, '\u21A9', button_font2, (255, 0, 0), (200, 0, 0))
        back_button.draw(screen)
        board.draw()

        if back_button.clicked() or kb.is_pressed('esc'):
            title_screen = True

    pg.display.flip()
