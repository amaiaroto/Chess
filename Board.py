import Pieces


class Board:
    def __init__(self, grid_cx_ry: tuple[int, int], screen, pg,
                 fen="RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr"):
        self.valid = None
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
    def readFEN(fen):
        """
        :param fen: fen string, see https://www.chess.com/terms/fen-chess for explanation
        :return:
        """
        state = {}
        rp = 8
        rows = fen.split('/')
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
        return state

    def printASCII(self):
        board = ""

        for r in range(8, 0, -1):
            ar = ""
            for c in range(1, 9):
                lc = Board.get_letter_from_index(c)
                ar += self.state[r][lc] if self.state[r][lc] is not None else '.'

            board += ar + "\n"

        board = ' ' + ' '.join(list(board))
        print(board)
        return board

    def get_piece_at(self, c, r):
        """

        :param c: 1 based
        :param r: 1 based
        :return:
        """
        return self.state[r][Board.get_letter_from_index(c)]
        # return self.state[list(self.state.keys())[(x - self.bx) // self.cw]][
        #     {k: v for k, v in self.state.items()}[alphabet_real[(y - self.by) // self.ch]]]

    def get_cell(self, x, y):
        c, r = (x - self.bx) // self.cw, (y - self.by) // self.ch
        return c + 1, r + 1

    def get_cell_center(self, c, r):
        return (c - 1) * self.cw + self.cw // 2, (self.rows - r) * self.ch + self.ch // 2

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
        # if piece_name is None:
        #     piece_name = Pieces.Piece.create_piece(self.get_piece_at(*self.get_cell(x, y)), x, y) if self.get_piece_at(
        #         *self.get_cell(x, y)) is not None else str
        #     piece_name = piece_name()
        #
        # """
        # mark in a field of this class the list of valid moves available for the piece in the cell
        # under x,y
        #
        # :param x:
        # :param y:
        # :return:
        # """
        # c, r = self.get_cell(x, y)
        # piece = Pieces.Piece.create_piece(piece_name if isinstance(piece_name, str) else piece_name.get_name(), c,
        #                                   r)
        # moves = piece.get_valid_moves()
        # self.valid = moves
        # print(self.valid)

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

                if self.state[r][lc] is not None:
                    icon = self.pg.font.Font('DejaVuSans.ttf', square_size).render(
                        self.state[r][lc].get_icon(), True,
                        (255, 255, 255) if self.state[r][lc].is_white() else (0, 0, 0))

                    self.screen.blit(icon, (square_size * c, square_size * r))

                if self.valid:
                    for p in self.valid:
                        center = self.get_cell_center(*p)
                        self.pg.draw.circle(self.screen, (180, 180, 180), center, self.cw // 3)

        # if self.moves is not None:
        #     for move in self.moves:
        #         draw circle at move
