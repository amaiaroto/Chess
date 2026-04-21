print('Imports:')
import keyboard as kb

print('"keyboard": OK')
import os

print('"os": OK')
import sys

print('"sys": OK')
from contextlib import redirect_stdout
from board import Board

print('"board": OK')

bg_color = (183, 255, 183)
title_screen = True

with redirect_stdout(open(os.devnull, 'w')):
    import pygame as pg

print('"pygame": OK')

pg.init()
pg.mixer.init()

rect = pg.rect.Rect(0, 0, 0, 0)
sound = pg.mixer.Sound('click_sfx.mp3')
screen = pg.display.set_mode((800, 800))
button_font = pg.font.Font('NotoSansSymbols-Bold.ttf', 72)
button_font2 = pg.font.SysFont('Segoe UI Symbol', 52)
pg.display.set_icon(pg.image.load('chess-icon.png'))
pg.display.set_caption('Chess — Play chess against a smart AI!')


class Button:
    def __init__(self, x: int, y: int, w: int, h: int, text: str, font: pg.Font,
                 color: tuple[int, int, int], hover_color: tuple[int, int, int]):
        self.rect = pg.Rect(x, y, w, h)
        self.text = font.render(self.parse(text), True, (0, 0, 0))
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen: pg.Surface):
        """
        Draw the button on the screen
        :param screen: The Surface to draw on
        """

        mouse = pg.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse) else self.color
        pg.draw.rect(screen, current_color, self.rect, border_radius=12)

        text_rect = self.text.get_rect(center=self.rect.center)
        screen.blit(self.text, text_rect)

    def clicked(self) -> bool:
        """
        get and return the cursor
        if the cursor is touching the button, return True and True
        :return:
        """

        mouse = pg.mouse.get_pos()
        return self.rect.collidepoint(mouse) and pg.mouse.get_pressed()[0]

    @staticmethod
    def parse(text: str, hint: str | list = '[]') -> str:
        result = ''
        co = False

        for c in text:
            con = False

            if c == '\\':
                con = True

            if c == hint[0] and not con:
                co = True

            if c == hint[1] and co:
                co = False
                continue

            if not co:
                result += c

        return result


class Popup:
    def __init__(self, color, screen):
        pg.draw.rect(screen, (57, 57, 58),
                     pg.Rect(screen.get_width() / 2 - 250, screen.get_height() / 2 - 150, 500, 300), border_radius=10)
        text = pg.font.Font(None, 37).render('Checkmate!', True, (245, 245, 245))
        screen.blit(text, (screen.get_width() / 2 - 28, screen.get_height() / 2))


fen = Board.starting_position()

board = Board((8, 8), screen, pg, '3qkbnr/3pp2p/6Q1/8/4B3/6K1/8/8 b')


def exit_chess(code: int | str = 0):
    pg.quit()
    board.printASCII()
    sys.exit(code)


def start_chess() -> bool:
    global title_screen

    title_screen = False

    return title_screen


while True:
    for event in pg.event.get():
        if not title_screen and event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            board.handle_click(x, y)

        if event.type == pg.QUIT:
            exit_chess()

        screen.fill(bg_color)

        if title_screen:
            if kb.is_pressed('esc'):
                exit_chess()

            if kb.is_pressed('shift+alt+b'):
                board.printASCII()

            text = pg.font.Font('DejaVuSans.ttf', 138)

            chars = [text.render(i, False, (0, 0, 0) if 'Ch♞s'.index(i) % 2 == 0 else (255, 255, 255)) for i in
                     list('Ch♞s')]
            chars.append(text.render('s', False, (0, 0, 0)))
            txt = list('Ch♞ss')

            play_button = Button(305, 400, 190, 100, 'PLAY', button_font,
                                 (0, 255, 0), (0, 205, 0))
            quit_button = Button(305, 525, 190, 100, 'QUIT', button_font,
                                 (255, 0, 0), (205, 0, 0))
            play_button.draw(screen)
            quit_button.draw(screen)

            if play_button.clicked() or kb.is_pressed('enter'):

                state = board.state
                start_chess()
            elif quit_button.clicked():
                exit_chess()

            text_pos = (800 - sum(t.get_width() for t in chars)) // 2
            for t in chars:
                if chars.index(t) == txt.index('♞'):
                    rect = [t.get_rect(), text_pos]

                screen.blit(t, (text_pos, 300 - t.get_rect().centery))
                text_pos += t.get_size()[0] // 1.1

            if pg.rect.Rect(340, 220, 124, 161).collidepoint(pg.mouse.get_pos()) and event.type == pg.MOUSEBUTTONDOWN:
                sound.play()
            Popup(1, screen)
        else:
            if kb.is_pressed('shift+alt+b'):
                board.printASCII()

            back_button = Button(10, 10, 53, 53, '\u21A9[↩]', button_font2,
                                 (255, 0, 0), (200, 0, 0))
            back_button.draw(screen)
            board.draw()

            if back_button.clicked() or kb.is_pressed('esc'):
                title_screen = True

        pg.display.flip()
