import pprint

import Pieces

toggle = False


class Board:
    def __init__(self, grid_cx_ry: tuple[int, int], screen, pg,
                 fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQWBNR"):
        self.valid = None
        self.picked_piece: Pieces.Piece
        self.picked_piece = None
        self.black_color = (80, 43, 17)
        self.white_color = (203, 198, 172)
        self.columns, self.rows = grid_cx_ry
        self.pg = pg
        self.screen = screen
        self.turn = True
        self.state = self.readFEN(fen)
        self.bx = 0
        self.by = 0
        self.cw = 0
        self.ch = 0
        self.moves_made: list[tuple] = []
        self.raw_fen = fen

    """add fields to store the left x, top y, cell width and cell height
    then implement a method that gets as input the mouse coordinates (every time you click left button)
    and returns the coordinates of the clicked cell.
    
    implement a method in board that receives the cell coordinates as input and returns the valid moves from that location.
    
    change the color (turn) in the board to a boolean as in pieces.
    
    """

    @staticmethod
    def get_letter_from_index(index):
        return chr(96 + index)

    @staticmethod
    def readFEN(fen, sep='/'):
        """
        :param sep: separator
        :param fen: fen string, see https://www.chess.com/terms/fen-chess for explanation
        :return: a {{}} of classes
        """
        # fen = ''.join(list(list(fen).__reversed__())) # flip the board
        state = {}
        rp = 8
        rows = fen.split(sep)
        # meta = {'r': BlackRook, 'n': BlackKnight, 'b': BlackBishop, 'q': BlackQueen,
        #         'k', BlackKing, 'p':BlackPawn, 'R': WhiteRook, 'N': WhiteKnight, 'B': WhiteBishop,
        # 'Q': WhiteQueen, 'K': WhiteKing, 'P': WhitePawn}
        for row in rows:
            cp = 1
            for col in row:
                current_row = state.get(rp)
                if current_row is None:
                    current_row = {Board.get_letter_from_index(k): None for k in range(1, 9)}
                    state[rp] = current_row
                if col.isdigit():
                    cp += int(col)
                else:
                    current_row[Board.get_letter_from_index(cp)] = Pieces.Piece.create_piece(col, col=cp, row=rp)
                    cp += 1
            rp -= 1
        return {k: state[k] for k in list(reversed(state.keys()))}

    @staticmethod
    def fromFEN(state: dict, sep='/'):
        """
        :param state:
        :param sep: separator
        :return: raw FEN
        """
        fen = ''
        s = 0
        for v in state.values():
            s = 0
            for x in v.values():
                if x is not None:
                    fen += str(s) if s else ''
                    fen += x.get_name()
                else:
                    s += 1
            fen += sep if v != 8 else ''
        return fen

    def printASCII(self):
        print('\n' * 16)
        board = ""

        for r in range(8, 0, -1):
            ar = ""
            for c in range(1, 9):
                lc = Board.get_letter_from_index(c)
                ar += self.state[r][lc].get_name() if self.state[r][lc] is not None else '.'

            board += ar + "\n"

        board = ' ' + ' '.join(list(board))
        print(board, end='')
        return board

    def get_piece_at(self, c, r):
        """

        :param c: 1 based
        :param r: 1 based
        :return:
        """
        try:
            assert r != 0 and c != 0

            if c > 8:
                raise KeyError

            return self.state[r][Board.get_letter_from_index(c)]

        except AssertionError:
            return None

        except KeyError:
            return None

        # return self.state[list(self.state.keys())[(x - self.bx) // self.cw]][
        #     {k: v for k, v in self.state.items()}[alphabet_real[(y - self.by) // self.ch]]]

    def go_to(self, c, r, piece):
        """
        :param c:
        :param r:
        :param piece: this is going to be moved from piece.row/col to c,r
        :return:
        """
        self.state[piece.row][Board.get_letter_from_index(piece.col)] = None
        self.state[r][Board.get_letter_from_index(c)] = piece
        self.raw_fen = self.fromFEN(self.state)
        piece.go_to(c, r)
        self.turn = not self.turn

    def get_cell(self, x, y):
        """
        :param x: point x
        :param y: point y
        :return: cell location on board
        """
        c, r = (x - self.bx) // self.cw + 1, self.rows - (y - self.by) // self.ch
        return c, r

    def get_cell_center(self, c, r):
        return (c - 1) * self.cw + self.cw // 2 + self.bx, (self.rows - r) * self.ch + self.ch // 2 + self.by

    def is_valid_cell(self, c, r):
        return 0 < c <= self.columns and 0 < r <= self.rows

    def flag_valid_moves(self, x: int, y: int):
        """
        :param x: mouse click position
        :param y:
        :return: list of pairs of positons (row, column) for all valid places the clicked piece can go
        """
        c, r = self.get_cell(x, y)
        piece = self.get_piece_at(c, r)

        if piece is not None:
            self.valid = piece.get_valid_moves(self)

            return self.valid

        return None

    def draw(self):
        square_size = min(self.screen.get_width(), self.screen.get_height()) // (max(self.rows, self.columns) + 2)

        for c in range(1, self.columns + 1):
            lc = Board.get_letter_from_index(c)

            for r in range(1, self.rows + 1):
                x, y = square_size * c, square_size * r

                if c + r == 2:
                    self.bx, self.by = x, y
                    self.cw = square_size
                    self.ch = square_size

                self.pg.draw.rect(self.screen, self.white_color if (c + r) % 2 == 0 else self.black_color,
                                  self.pg.Rect(x, y, square_size, square_size))

                real_r = (self.rows - r) + 1

                for f in self.raw_fen:
                    for i in f:
                        if 'k' not in i:
                            f.replace('K', 'W')

                        elif 'K' not in i:
                            f.replace('k', 'w')

                # self.state = self.readFEN(self.raw_fen)

                if self.state[real_r][lc] is not None:
                    icon = self.pg.font.Font('DejaVuSans.ttf', square_size).render(
                        self.state[real_r][lc].get_icon(), True,
                        (255, 255, 255) if self.state[real_r][lc].is_white() else (0, 0, 0))

                    self.screen.blit(icon, (square_size * c, square_size * r))

                self.moves_made.extend(self.valid if self.valid is not None else [])

                if self.valid:
                    for p in self.valid:
                        center = self.get_cell_center(*p)
                        self.pg.draw.circle(self.screen, (180, 180, 180), center, self.cw // 3)

        # if self.moves is not None:
        #     for move in self.moves:
        #         draw circle at move

    def handle_click(self, x, y):
        c, r = self.get_cell(x, y)
        piece: Pieces.Piece = self.get_piece_at(c, r)
        has_valid_moves = self.valid is not None and len(self.valid) > 0

        if piece is None and not has_valid_moves:
            pass

        elif piece is None and has_valid_moves:
            if (c, r) in self.valid:
                self.go_to(c, r, self.picked_piece)
            self.valid = []
            self.picked_piece = None

        elif piece is not None and not has_valid_moves:
            self.valid = piece.get_valid_moves(self)
            self.picked_piece = piece

        else:
            # Yes & Yes

            if (c, r) not in self.valid:
                if piece == self.picked_piece:
                    self.valid = []
                    self.picked_piece = None

                else:
                    self.valid = piece.get_valid_moves(self)
                    self.picked_piece = piece
            else:
                self.go_to(c, r, self.picked_piece)
                self.valid = []

    def move(self, mouse_pos: tuple[int, int]):
        global toggle
        toggle = not toggle
        if self.get_piece_at(*self.get_piece_at(*mouse_pos)):
            self.get_piece_at(*self.get_cell(*mouse_pos)).go_to(*self.get_cell(*mouse_pos))


# if self.picked_piece.get_valid_moves(self, self):
#     for c in self.picked_piece.get_valid_moves(self, self):
#         if cell == c:
#             self.picked_piece.go_to(*cell)
#             break\

"""
Perfect | Oki | Bad | Worst |
________________________________________________________
do this | idk | idk | isdrk |
# yay
# im done
# todo: done
"""
