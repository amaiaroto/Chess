import Pieces
import Undo

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
        self.state = self.readFEN(fen)
        self.bx = 0
        self.by = 0
        self.cw = 0
        self.ch = 0
        self.moves_made: list[tuple] = []
        self.raw_fen = fen
        self.jail = {True: {}, False: {}}
        self.won = self.has_won()  # None, white, or black (true or false)
        self.pieces = self.get_pieces()
        self.history: list[Undo.UndoMove] = []

    """add fields to store the left x, top y, cell width and cell height
    then implement a method that gets as input the mouse coordinates (every time you click left button)
    and returns the coordinates of the clicked cell.
    
    implement a method in board that receives the cell coordinates as input and returns the valid moves from that location.
    
    change the color (turn) in the board to a boolean as in pieces.
    
    """

    @staticmethod
    def get_letter_from_index(index) -> str:
        return chr(96 + index)

    @staticmethod
    def readFEN(fen, sep='/') -> dict:
        """
        :param sep: separator
        :param fen: fen string, see https://www.chess.com/terms/fen-chess for explanation
        :return: a {{}} of classes
        """

        state = {}
        rp = 8
        rows = fen.split(sep)

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

    def printASCII(self) -> str:
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

    def exportFEN(self) -> str:
        fen = ""
        for r in range(8, 0, -1):
            num = 0
            ar = ""
            for c in range(1, 9):
                lc = Board.get_letter_from_index(c)

                if self.state[r][lc] is not None:
                    if num != 0:
                        ar += str(num)

                    ar += self.state[r][lc].get_name()
                    num = 0

                else:
                    num += 1

            if num != 0:
                ar += str(num)

            fen += ar + '/'

        return fen[:-1]

    @staticmethod
    def get_color_name(color) -> str:
        return 'white' if color else 'black'

    def get_piece_at(self, c, r) -> Pieces.Piece | None:
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

    def modify_pos(self, c, r, piece) -> dict:
        self.state[r][self.get_letter_from_index(c)] = piece
        return self.state

    def undo_go_to(self, move_info: Undo.UndoMove):
        move_info.sp.go_to(*move_info.sp_pos)
        r, c = move_info.sp_pos
        piece = move_info.sp

        self.state[r][self.get_letter_from_index(c)] = piece
        eaten_piece = move_info.piece_at_target
        self.state[move_info.pos_of_piece_at_target[0]][
            Board.get_letter_from_index(move_info.pos_of_piece_at_target[1])] = eaten_piece

        if not move_info.lw:
            if eaten_piece is not None:
                jail_for_color = self.jail[eaten_piece.color]
                assert eaten_piece.get_name() in jail_for_color
                count_of_eaten_piece = jail_for_color[eaten_piece.get_name()]
                jail_for_color[eaten_piece.get_name()] = count_of_eaten_piece - 1
                self.won = self.has_won()

    def go_to(self, c, r, piece, lw=False) -> Undo.UndoMove:
        """
        :param c: c
        :param r: r
        :param lw: lightweight
        :param piece: this piece is going to be moved from piece.row/col to c,r
        :return:
        """

        eaten_piece: Pieces.Piece = self.state[r][Board.get_letter_from_index(c)]

        assert eaten_piece is None or eaten_piece.color != piece.color
        assert piece is not None

        move_info = Undo.UndoMove(self, piece, (r, c), lw)
        self.state[piece.row][Board.get_letter_from_index(piece.col)] = None
        self.state[r][Board.get_letter_from_index(c)] = piece

        if not lw:
            if eaten_piece is not None:
                jail_for_color = self.jail[eaten_piece.color]
                count_of_eaten_piece = jail_for_color.get(eaten_piece.get_name(), 0)
                jail_for_color[eaten_piece.get_name()] = count_of_eaten_piece + 1
                self.won = self.has_won()

            # self.history.append(move_info)

            piece.go_to(c, r)

            self.turn = not self.turn

        return move_info

    def get_cell(self, x, y) -> tuple:
        """
        :param x: point x
        :param y: point y
        :return: cell location on board
        """
        c, r = (x - self.bx) // self.cw + 1, self.rows - (y - self.by) // self.ch

        return c, r

    def get_cell_center(self, c, r) -> tuple:
        return (c - 1) * self.cw + self.cw // 2 + self.bx, (self.rows - r) * self.ch + self.ch // 2 + self.by

    def is_valid_cell(self, c, r) -> bool:
        return 0 < c <= self.columns and 0 < r <= self.rows

    def flag_valid_moves(self, x: int, y: int) -> set | None:
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
                get_icon = lambda p: \
                    Pieces.Piece.get_piece_icon('W' if p.color else 'w') if isinstance(p, Pieces.King) and \
                                                                            self.won == p.color else p.get_icon()

                if self.state[real_r][lc] is not None:
                    icon = self.pg.font.SysFont('Segoe UI Symbol', square_size - 10).render(
                        get_icon(self.state[real_r][lc]), True,
                        (255, 255, 255) if self.state[real_r][lc].is_white() else (0, 0, 0))

                    self.screen.blit(icon, (square_size * c + 3, square_size * r - 8))

                self.moves_made.extend(self.valid if self.valid is not None else [])

                if self.valid is not None and len(self.valid) > 0:
                    for p in self.valid:
                        center = self.get_cell_center(*p)
                        self.pg.draw.circle(self.screen, (180, 180, 180), center, self.cw // 3)

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

    def has_won(self) -> bool | None:
        for color, jail in self.jail.items():
            if 'k' in jail or 'K' in jail:
                return not color

        return None

    def get_pieces(self) -> dict[bool, set]:
        re = {True: set(), False: set()}
        x: Pieces.Piece

        for i in self.state.values():
            for x in i.values():
                if x is not None:
                    re[x.color].add(x)

        return re

    def get_king(self, color) -> Pieces.King | None:
        color_pieces = self.get_pieces()[color]

        for p in color_pieces:
            if isinstance(p, Pieces.King):
                return p

        return None

    def filter_moves_if_opponent_can_reach(self, piece: Pieces.Piece, pos: tuple[int, int], valid_moves: set | None):
        assert piece is not None

        vm = set()

        if valid_moves is not None:
            opp_pieces = self.get_pieces()[not piece.color]

            for move in valid_moves:
                # todo: fix flipped C&R somewhere
                undo = self.go_to(*move, piece, lw=True)

                for op in opp_pieces:
                    op_vm = op.get_valid_moves(self, no_turn=True, _filter=False)

                    if op_vm is not None and pos in op_vm:
                        vm.add(move)

                        break

                self.undo_go_to(undo)

            valid_moves.difference_update(vm)

    @staticmethod
    def starting_position():
        return 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
