import os
import sys
from contextlib import redirect_stdout
from enum import Enum
import keyboard as kb
import pieces
from board import Board
from board import Mate
from bots import bot0
from bots import bot1

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.debug("LOGGING INITIATED")

with redirect_stdout(open(os.devnull, "w")):
    import pygame as pg

pg.init()
pg.mixer.init()

bg_color = (183, 255, 183)
title_screen = True
rect = pg.rect.Rect(0, 0, 0, 0)
sound = pg.mixer.Sound("click_sfx.mp3")
screen: pg.Surface = pg.display.set_mode((800, 800), pg.RESIZABLE)
button_font = pg.font.Font("NotoSansSymbols-Bold.ttf", 72)
button_font2 = pg.font.SysFont("Segoe UI Symbol", 52)
pg.display.set_icon(pg.image.load("chess-icon.png"))
pg.display.set_caption("Chess — Play chess against a smart AI!")


class State(Enum):
    # -state field that is an enumeration of 4 values: init, game, exit, checkmate
    # -components list: this contains the list of graphical elements that need to \
    # be drawn in the current state
    #
    # add an init method that sets the state to init and adds the \
    # play/quit and horse graphical elements to the component list
    #
    # add a draw method that loops over the list of components and draws them.
    state = Enum("state", [("value_1", 1), ("value_2", 2)])


class Button:
    def __init__(self, x: int, y: int, w: int, h: int, text: str, font: pg.Font,
                 color: tuple[int, int, int], hover_color: tuple[int, int, int]):
        self.rect = pg.Rect(x, y, w, h)
        self.text = font.render(self.parse(text), True, (0, 0, 0))
        self.color = color
        self.hover_color = hover_color

    def draw(self, surface: pg.Surface):
        """
        Draw the button on the screen
        :param surface: The Surface to draw on
        """

        mouse = pg.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse) else self.color
        pg.draw.rect(surface, current_color, self.rect, border_radius=12)

        text_rect = self.text.get_rect(center=self.rect.center)
        surface.blit(self.text, text_rect)

    def clicked(self) -> bool:
        """
        get and return the cursor
        if the cursor is touching the button, return True and True
        :return:
        """

        mouse = pg.mouse.get_pos()
        return self.rect.collidepoint(mouse) and pg.mouse.get_pressed()[0]

    @staticmethod
    def parse(text: str, hint: str | list = "[]") -> str:
        result = ""
        co = False

        for c in text:
            con = False

            if c == "\\":
                con = True

            if c == hint[0] and not con:
                co = True

            if c == hint[1] and co:
                co = False
                continue

            if not co:
                result += c

        return result


checkmate = True


class Popup:
    def __init__(self, color, surface):
        global checkmate

        if checkmate:
            width = 500
            height = 300
            pg.draw.rect(surface, (57, 57, 58),
                         pg.Rect(surface.get_width() // 2 - width // 2, surface.get_height() // 2 - height // 2, width,
                                 height),
                         border_radius=10)
            text = pg.font.Font(None, 37).render(f"Checkmate!\n{ {True: "White", False: "Black"}[color]} wins!", True,
                                                 (245, 245, 245))
            ok_button = Button(surface.get_width() // 2 - width // 4, surface.get_height() // 2 - 30, width // 2,
                               height // 4,
                               "OK", button_font, (0, 255, 0), (0, 205, 0))
            exit_button = Button(surface.get_width() // 2 - width // 4, surface.get_height() // 1.70 - 15, width // 2,
                                 height // 4,
                                 "EXIT", button_font, (255, 0, 0), (205, 0, 0))

            surface.blit(text,
                         (surface.get_width() // 2 - text.get_width() // 2, surface.get_height() // 2 - height // 2.5))
            ok_button.draw(surface)
            exit_button.draw(surface)

            if exit_button.clicked():
                exit_chess()

            if ok_button.clicked():
                checkmate = False


stalemate = True


class Popup2:
    def __init__(self, surface):
        global stalemate

        if stalemate:
            width = 500
            height = 300
            pg.draw.rect(surface, (57, 57, 58),
                         pg.Rect(surface.get_width() // 2 - width // 2, surface.get_height() // 2 - height // 2, width,
                                 height),
                         border_radius=10)
            text = pg.font.Font(None, 37).render(f"Stalemate!\nIt's a draw!", True,
                                                 (245, 245, 245))
            ok_button = Button(surface.get_width() // 2 - width // 4, surface.get_height() // 2 - 30, width // 2,
                               height // 4,
                               "OK", button_font, (0, 255, 0), (0, 205, 0))
            exit_button = Button(surface.get_width() // 2 - width // 4, surface.get_height() // 1.70 - 15, width // 2,
                                 height // 4,
                                 "EXIT", button_font, (255, 0, 0), (205, 0, 0))

            surface.blit(text,
                         (surface.get_width() // 2 - text.get_width() // 2, surface.get_height() // 2 - height // 2.5))
            ok_button.draw(surface)
            exit_button.draw(surface)

            if exit_button.clicked():
                exit_chess()

            if ok_button.clicked():
                stalemate = False


fen = Board.starting_position()
board = Board()
player_color = True


def exit_chess(code: int | str = 0):
    pg.quit()
    board.printASCII()
    sys.exit(code)


def start_chess() -> bool:
    global board, title_screen, player_color, checkmate

    title_screen = False
    checkmate = True
    board = Board((8, 8), screen, pg, fen, player_color, [bot0.Bot0, bot1.Bot1][1])

    return title_screen


# create the UI state

while True:
    # State.draw()

    for event in pg.event.get():
        if not title_screen and event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            # state.handle_click(x,y)
            board.handle_click(x, y)

        if event.type == pg.QUIT:
            exit_chess()

        screen.fill(bg_color)

        if title_screen:
            if kb.is_pressed("esc"):
                exit_chess()

            if kb.is_pressed("shift+alt+b"):
                print(board.exportFEN())

            text = pg.font.Font("DejaVuSans.ttf", 138)

            chars = [text.render(i, False, (0, 0, 0) if "Ch♞s".index(i) % 2 == 0 else (255, 255, 255)) for i in
                     list("Ch♞s")]
            chars.append(text.render("s", False, (0, 0, 0)))
            txt = list("Ch♞ss")

            play_button = Button(305, 400, 190, 100, "PLAY", button_font,
                                 (0, 255, 0), (0, 205, 0))
            quit_button = Button(305, 525, 190, 100, "QUIT", button_font,
                                 (255, 0, 0), (205, 0, 0))
            white_color_button = Button(20, 20, 50, 50, "", button_font,
                                        (255, 255, 255), (250, 250, 250))
            black_color_button = Button(80, 20, 50, 50, "", button_font,
                                        (0, 0, 0), (5, 5, 5))

            play_button.draw(screen)
            quit_button.draw(screen)
            white_color_button.draw(screen)
            black_color_button.draw(screen)

            if play_button.clicked() or kb.is_pressed("enter"):
                state = board.state
                start_chess()

            elif quit_button.clicked():
                exit_chess()

            elif white_color_button.clicked():
                player_color = True

            elif black_color_button.clicked():
                player_color = False

            text_pos = (800 - sum(t.get_width() for t in chars)) // 2
            for t in chars:
                if chars.index(t) == txt.index("♞"):
                    rect = [t.get_rect(), text_pos]

                screen.blit(t, (text_pos, 300 - t.get_rect().centery))
                text_pos += t.get_size()[0] // 1.1

            if pg.rect.Rect(340, 220, 124, 161).collidepoint(pg.mouse.get_pos()) and event.type == pg.MOUSEBUTTONDOWN:
                sound.play()
        else:

            if kb.is_pressed("shift+alt+b"):
                print(board.exportFEN())

            back_button = Button(10, 10, 53, 53, "\u21A9[↩]", button_font2,
                                 (255, 0, 0), (200, 0, 0))
            back_button.draw(screen)
            board.draw()
            jail = board.get_jail()
            font = pg.font.SysFont("Segoe UI Symbol", 50)

            pos = (80, 0)
            screen.blit(
                font.render(" ".join([pieces.piece_icons[i] for i in jail[True].keys()]), True, (255, 255, 255)),
                pos)

            pos = (80, 720)
            screen.blit(
                font.render(" ".join([pieces.piece_icons[i] for i in jail[False]]), True, (0, 0, 0)),
                pos)

            mate = board.checkmate()
            if mate:
                if mate == Mate.checkmate:
                    Popup(not board.turn, screen)

                elif mate == Mate.stalemate:
                    Popup2(screen)

            if back_button.clicked() or kb.is_pressed("esc"):
                title_screen = True

        pg.display.flip()
