from enum import Enum

piece_icons: dict[str, str] = {
    "K": "♔",
    "Q": "♕",
    "R": "♖",
    "B": "♗",
    "N": "♘",
    "P": "♙",

    "k": "♚",
    "q": "♛",
    "r": "♜",
    "b": "♝",
    "n": "♞",
    "p": "♟",
}


class CastlingSides(Enum):
    none = 0
    king = 1
    queen = 2


def flatten(*iterable, keep_duplicates: bool = False) -> set | list:
    """
    spreads out all values/tuples into one list/set
    :param keep_duplicates:
    :param iterable: The iterable being flattened
    :return: The flattened iterable
    """

    result = []
    stack = [*iterable]

    while len(stack) > 0:
        p = stack.pop(0)

        if isinstance(p, tuple):
            result.append(p)

        else:
            try:
                stack.extend(p)

            except:
                result.append(p)

    if keep_duplicates:
        return result

    return set(result)


class PieceError(BaseException):
    def __init__(self, name: str):
        self.error: str = name

    def __str__(self):
        return self.error


class Piece:
    standard_name = None

    def __init__(self, name: str, color: bool, col: int, row: int):
        self.piece = name
        self.color: bool = color  # uppercase is w
        self.col: int = col
        self.row: int = row
        self.value: int = 1
        self.has_moved = False
        self.set_name()

    def set_name(self) -> None:
        self.piece = self.piece.upper() if self.color else self.piece.lower()

    def is_white(self) -> bool:
        return self.color

    def get_name(self) -> str:
        """
        Gets the letter of the piece
        :return: Letter of piece
        """
        return self.piece

    @staticmethod
    def get_piece_icon(name):
        global piece_icons

        return piece_icons[name]

    def get_icon(self):
        return Piece.get_piece_icon(self.get_name())

    def get_valid_moves(self, board, no_turn=False, _filter=True) -> set:
        ...

    def go_to(self, c: int, r: int) -> tuple:
        try:
            assert 0 < c < 9 and 0 < r < 9

        except AssertionError:
            return self.col, self.row

        self.has_moved = True
        self.col = c
        self.row = r

        return self.col, self.row

    def _return(self):
        pass

    @staticmethod
    def create_piece(name: str, color: bool, col: int, row: int) -> Piece | None:
        for c in Piece.__subclasses__():
            if c.standard_name == name.lower():
                return c(color, col, row)

        raise PieceError("Piece Not Found")

    @staticmethod
    def get_piece(name: str) -> type[Piece]:
        for c in Piece.__subclasses__():
            if c.standard_name == name.lower():
                return c

        raise PieceError("Invalid Piece Name")

    def line_movement(self, dr: int, dc: int, board, max_range, color) -> set:
        """
        returns the set of tuples that represent the coordinates of the cells of the board in a line starting at
        (self.c+dc,self.r+dr) going in direction dc/dr (e.g. if dc is -1 we go left) up to max_range moves (stops when we reach max_range
        moves or the board size or a piece). we include the move that eat a piece of the opposite color (as last move in the
        line)

        :param color: piece color
        :param dr: delta row
        :param dc: delta col
        :param board: the board
        :param max_range: 0 based
        :return: valid moves
        """
        assert (2 > abs(dc) > -1) and (2 > abs(dr) > -1)
        c = self.col
        r = self.row
        valid_moves = set()

        for n in range(max(board.columns, board.columns)):
            c += dc
            r += dr

            if not board.is_valid_cell(c, r):
                break

            if board.get_piece_at(c, r) is None:
                valid_moves.add((c, r))

            elif board.get_piece_at(c, r).color != color:
                valid_moves.add((c, r))
                break

            else:
                break

            if n >= max_range:
                break

        return valid_moves

    def get_pos(self) -> tuple[int, int]:
        return self.col, self.row

    def __str__(self):
        return f"{self.get_name()} {self.get_pos()}"


# Pieces
# (Listed by value)


class Pawn(Piece):
    standard_name = "p"

    def __init__(self, color: bool, col: int, row: int):
        super().__init__(Pawn.standard_name, color, col, row)
        self.value = 1

    def get_valid_moves(self, board, no_turn=False, _filter=True):
        valid_moves: set = set()

        def move(m):
            nonlocal valid_moves
            skip = False
            # attack / capture
            if board.get_piece_at(self.col + 1, self.row + m) is not None and \
                    board.get_piece_at(self.col + 1, self.row + m).color != self.color:
                valid_moves.add((self.col + 1, self.row + m))

            if board.get_piece_at(self.col - 1, self.row + m) is not None and \
                    board.get_piece_at(self.col - 1, self.row + m).color != self.color:
                valid_moves.add((self.col - 1, self.row + m))

            # normal
            if board.get_piece_at(self.col, self.row + m) is None:
                valid_moves.add((self.col, self.row + m))

            else:
                skip = True

            # double
            if ((m > 0 and self.row == 2) or (m < 0 and self.row == board.rows - 1)
                and board.get_piece_at(self.col, self.row + (m * 2)) is None) and not skip and board.get_piece_at(
                self.col, self.row + (m * 2)) is None:
                valid_moves.add((self.col, self.row + (m * 2)))

        if self.color == board.turn or no_turn:
            move(1 if self.color else -1)

        if _filter:
            # removes this piece valid moves that cause other pieces to be able to reach the king (of the same color)
            board.filter_moves_if_opponent_can_reach(self, board.get_king(self.color).get_pos(), valid_moves)

        return valid_moves


class Knight(Piece):
    standard_name = "n"

    def __init__(self, color: bool, col: int, row: int):
        super().__init__(Knight.standard_name, color, col, row)
        self.value = 3

    def get_valid_moves(self, board, no_turn=False, _filter=True):
        valid_moves: set = set()
        moves = [(self.col + 2, self.row + 1), (self.col + 2, self.row - 1), (self.col + 1, self.row + 2),
                 (self.col - 1, self.row + 2), (self.col + 1, self.row - 2), (self.col - 2, self.row - 1),
                 (self.col - 2, self.row + 1), (self.col - 1, self.row - 2)]

        for move in moves:
            if board.is_valid_cell(*move) and (self.color == board.turn or no_turn):
                if board.get_piece_at(*move) is not None:
                    if board.get_piece_at(*move).color != self.color:
                        valid_moves.add(move)
                else:
                    valid_moves.add(move)

        if _filter:
            board.filter_moves_if_opponent_can_reach(self, board.get_king(self.color).get_pos(), valid_moves)

        return valid_moves


class Bishop(Piece):
    standard_name = "b"

    def __init__(self, color: bool, col: int, row: int):
        super().__init__(Bishop.standard_name, color, col, row)
        self.value = 3

    def get_valid_moves(self, board, no_turn=False, _filter=True):
        if self.color == board.turn or no_turn:
            a = self.line_movement(-1, 1, board, 8, self.color)
            b = self.line_movement(1, -1, board, 8, self.color)
            c = self.line_movement(1, 1, board, 8, self.color)
            d = self.line_movement(-1, -1, board, 8, self.color)

            valid_moves = flatten(a, b, c, d)

            if _filter:
                board.filter_moves_if_opponent_can_reach(self, board.get_king(self.color).get_pos(), valid_moves)

            return valid_moves

        return None


class Rook(Piece):
    standard_name = "r"

    def __init__(self, color: bool, col: int, row: int):
        super().__init__(Rook.standard_name, color, col, row)
        self.value = 5

    def get_valid_moves(self, board, no_turn=False, _filter=True):
        if self.color == board.turn or no_turn:
            a = self.line_movement(1, 0, board, 8, self.color)
            b = self.line_movement(-1, 0, board, 8, self.color)
            c = self.line_movement(0, 1, board, 8, self.color)
            d = self.line_movement(0, -1, board, 8, self.color)

            valid_moves = flatten(a, b, c, d)

            if _filter:
                board.filter_moves_if_opponent_can_reach(self, board.get_king(self.color).get_pos(), valid_moves)

            return valid_moves

        return None


class Queen(Piece):
    standard_name = "q"

    def __init__(self, color: bool, col: int, row: int):
        super().__init__(Queen.standard_name, color, col, row)
        self.value = 9

    def get_valid_moves(self, board, no_turn=False, _filter=True):
        if self.color == board.turn or no_turn:
            # - & |
            a = self.line_movement(1, 0, board, 8, self.color)
            b = self.line_movement(-1, 0, board, 8, self.color)
            c = self.line_movement(0, 1, board, 8, self.color)
            d = self.line_movement(0, -1, board, 8, self.color)

            # \ & /
            e = self.line_movement(-1, 1, board, 8, self.color)
            f = self.line_movement(1, -1, board, 8, self.color)
            g = self.line_movement(1, 1, board, 8, self.color)
            h = self.line_movement(-1, -1, board, 8, self.color)

            valid_moves = flatten(a, b, c, d, e, f, g, h)

            if _filter:
                board.filter_moves_if_opponent_can_reach(self, board.get_king(self.color).get_pos(), valid_moves)

            return valid_moves

        return None


MoveError = PieceError


class King(Piece):
    standard_name = "k"

    def __init__(self, color: bool, col: int, row: int):
        super().__init__(King.standard_name, color, col, row)
        self.value = 12

    def get_valid_moves(self, board, no_turn=False, _filter=True):
        global MoveError

        if self.color == board.turn or no_turn:
            a = self.line_movement(1, 0, board, 0, self.color)
            b = self.line_movement(1, 1, board, 0, self.color)
            c = self.line_movement(0, 1, board, 0, self.color)
            d = self.line_movement(-1, 0, board, 0, self.color)
            e = self.line_movement(-1, 1, board, 0, self.color)
            f = self.line_movement(-1, -1, board, 0, self.color)
            g = self.line_movement(0, -1, board, 0, self.color)
            h = self.line_movement(1, -1, board, 0, self.color)
            i = set()
            rook = board.get_piece_at(8, self.row)

            if _filter:  # approximation, we should add a _filter to the filter_va;lid_moves method
                if rook is not None and not rook.has_moved and not self.has_moved and not self.under_threat(board):
                    cells_in_between = rook.col - self.col - 1
                    if len(board.filter_moves_if_opponent_can_reach(self, None, self.line_movement(0, 1, board,
                                                                                                   cells_in_between,
                                                                                                   self.color))) == (
                            cells_in_between):
                        i.add((self.col + 2, self.row))
            rook = board.get_piece_at(1, self.row)

            if _filter:
                if rook is not None and not rook.has_moved and not self.has_moved and not self.under_threat(board):
                    cells_in_between = self.col - rook.col - 1
                    if len(board.filter_moves_if_opponent_can_reach(self, None, self.line_movement(0, -1, board,
                                                                                                   cells_in_between,
                                                                                                   self.color))) == (
                            cells_in_between):
                        i.add((self.col - 2, self.row))
            o = flatten(a, b, c, d, e, f, g, h, i)

            if _filter:
                # removes the king's valid moves (that are) reachable by opponent pieces
                board.filter_moves_if_opponent_can_reach(self, None, o)

            return o

        return None

    def under_threat(self, board) -> bool:
        for p in board.get_pieces()[not self.color]:
            p_valid_moves = p.get_valid_moves(board, no_turn=True, _filter=False)

            if p_valid_moves is not None:
                if self.get_pos() in p_valid_moves:
                    return True

        return False
