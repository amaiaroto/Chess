import Pieces

toggle = False


class Board:
    def __init__(self, grid_cx_ry: tuple[int, int], screen, pg,
                 fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        self.valid = None
        self.picked_piece: Pieces.Piece
        self.picked_piece = None
        self.black_color = (80, 43, 17)
        self.white_color = (203, 198, 172)
        self.columns, self.rows = grid_cx_ry
        self.pg = pg
        self.screen = screen
        self.turn = True
        self.state = self.readFEN(self, fen)
        self.bx = 0
        self.by = 0
        self.cw = 0
        self.ch = 0
        self.moves_made: list[tuple] = []
        self.raw_fen = fen
        self.jail = {True: {}, False: {}}
        self.won = self.has_won()  # None, white, or black (true or false)
        self.pieces = self.get_pieces()

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
    def readFEN(self, fen, sep='/'):
        """
        :param self: self
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
                    current_row[Board.get_letter_from_index(cp)] = Pieces.Piece.create_piece(col, cp, rp, self)
                    cp += 1
            rp -= 1
        return {k: state[k] for k in list(reversed(state.keys()))}

    # @staticmethod
    # def fromFEN(state: dict, sep='/'):
    #     """
    #     :param state:
    #     :param sep: separator
    #     :return: raw FEN
    #     """
    #     fen = ''
    #     s = 0
    #     for v in state.values():
    #         s = 0
    #         for x in v.values():
    #             if x is not None:
    #                 fen += str(s) if s else ''
    #                 fen += x.get_name()
    #             else:
    #                 s += 1
    #         fen += sep if v != 8 else ''
    #     return fen

    def printASCII(self):
        print('\n' * 16)
        print(self.turn)
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

    @staticmethod
    def get_color_name(color):
        return 'white' if color else 'black'

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
        eaten_piece: Pieces.Piece = self.state[r][Board.get_letter_from_index(c)]

        assert eaten_piece is None or eaten_piece.color != piece.color

        if eaten_piece is not None:
            jail_for_color = self.jail[eaten_piece.color]
            count_of_eaten_piece = jail_for_color.get(eaten_piece.get_name(), 0)
            jail_for_color[eaten_piece.get_name()] = count_of_eaten_piece + 1
            self.won = self.has_won()
            # remove piece from self.pieces set for the color of piece
            print(self.jail)

        self.state[piece.row][Board.get_letter_from_index(piece.col)] = None
        self.state[r][Board.get_letter_from_index(c)] = piece
        # self.raw_fen = self.fromFEN(self.state)
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

                # for f in self.raw_fen:
                #     for i in f:
                #         if 'k' not in i:
                #             f.replace('K', 'W')
                #
                #         elif 'K' not in i:
                #             f.replace('k', 'w')

                # self.state = self.readFEN(self.raw_fen)

                get_icon = lambda p: \
                    (Pieces.Piece.get_piece_icon('W' if p.color else 'w')) if (isinstance(p, Pieces.King) and
                                                                               self.won == p.color) else p.get_icon()
                get_icon = lambda p: p.get_icon()

                if self.state[real_r][lc] is not None:
                    icon = self.pg.font.SysFont('Segoe UI Symbol', square_size - 10).render(
                        get_icon(self.state[real_r][lc]), True,
                        (255, 255, 255) if self.state[real_r][lc].is_white() else (0, 0, 0))

                    self.screen.blit(icon, (square_size * c + 3, square_size * r - 8))

                self.moves_made.extend(self.valid if self.valid is not None else [])

                if self.picked_piece is not None and self.picked_piece.moves:
                    for p in self.picked_piece.moves:
                        center = self.get_cell_center(*p)
                        self.pg.draw.circle(self.screen, (180, 180, 180), center, self.cw // 3)

        # if self.moves is not None:
        #     for move in self.moves:
        #         draw circle at move

    def handle_click(self, x, y):
        c, r = self.get_cell(x, y)
        piece: Pieces.Piece = self.get_piece_at(c, r)
        print(piece)
        try:
            has_valid_moves = self.picked_piece.moves and len(self.picked_piece.moves)

        except AttributeError:
            has_valid_moves = False
        print(has_valid_moves)
        if piece is None and not has_valid_moves:
            pass

        elif piece is None and has_valid_moves:
            if (c, r) in self.picked_piece.moves:
                self.go_to(c, r, self.picked_piece)
            self.picked_piece.moves = set()
            self.picked_piece = None

        elif piece is not None and not has_valid_moves:
            self.picked_piece = piece
            self.picked_piece.get_valid_moves(self)

        else:
            if (c, r) not in self.picked_piece.moves:
                if piece == self.picked_piece:
                    self.picked_piece.moves = set()
                    self.picked_piece = None

                else:
                    self.picked_piece.moves = piece.get_valid_moves(self)
                    self.picked_piece = piece
            else:
                self.go_to(c, r, self.picked_piece)
                self.picked_piece.moves = set()

    def has_won(self):
        for color, jail in self.jail.items():
            if 'k' in jail or 'K' in jail:
                return not color
        return None

    def get_pieces(self):
        re: dict = {True: set(), False: set()}
        x: Pieces.Piece

        print(self.state)

        for i in self.state.values():
            for x in i.values():
                if x is not None:
                    re[x.color].add(x)

        return re

    def get_king(self, color: bool):
        all_pieces = self.get_pieces()[color]

        for i in all_pieces:
            if type(i) == Pieces.King:
                return i

        raise Pieces.PieceError('No king found')
