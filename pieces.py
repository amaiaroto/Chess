piece_icons: dict[str, str] = {
    'K': '♔',
    'Q': '♕',
    'R': '♖',
    'B': '♗',
    'N': '♘',
    'P': '♙',
    'W': '🜲',

    'k': '♚',
    'q': '♛',
    'r': '♜',
    'b': '♝',
    'n': '♞',
    'p': '♟',
    'w': '🜲'
}


def flatten(*iterable, keep_duplicates: bool = False) -> set | list:
    """
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
    def __init__(self, name: str, col: int, row: int, win=False):
        self.piece: str = name
        self.color: bool = name.isupper()  # uppercase is w
        self.col: int = col
        self.row: int = row
        self.win = win
        self.value: int = 1

    def is_white(self):
        return self.color

    def get_name(self):
        """
        Gets the letter of the piece
        :return: Letter of piece
        """
        return self.piece if not self.win else 'W' if self.color else 'w'

    @staticmethod
    def get_piece_icon(name):
        global piece_icons

        return piece_icons[name]

    def get_icon(self):
        return Piece.get_piece_icon(self.get_name())

    def get_valid_moves(self, board, no_turn=False, _filter=True) -> set:
        ...

    def go_to(self, c: int, r: int):
        try:
            assert 0 < c < 9 and 0 < r < 9

        except AssertionError:
            return self.col, self.row

        self.col = c
        self.row = r

        return self.col, self.row

    def _return(self):
        pass

    @staticmethod
    def create_piece(name: str, col, row):
        match name.lower():
            case 'p':
                return Pawn(name, col, row)

            case 'r':
                return Rook(name, col, row)

            case 'n':
                return Knight(name, col, row)

            case 'b':
                return Bishop(name, col, row)

            case 'q':
                return Queen(name, col, row)

            case 'k':
                return King(name, col, row)

            case 'w':
                return King(name, col, row)

        print(name)

        raise PieceError('Not valid piece type')

    @staticmethod
    def get_piece(name='please input name'):
        match name.lower():
            case 'pawn' | 'p':
                return Pawn

            case 'rook' | 'r':
                return Rook

            case 'knight' | 'n':
                return Knight

            case 'bishop' | 'b':
                return Bishop

            case 'queen' | 'q':
                return Queen

            case 'king' | 'k':
                return King

            case 'winner' | 'w':
                return King

        raise PieceError('Not valid name')

    def line_movement(self, dr: int, dc: int, board, max_range, color):
        """
        :param color: piece color
        :param dr: delta row
        :param dc: delta col
        :param board: the board
        :param max_range: 0 based
        :return: valid moves
        """
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


class Pawn(Piece):
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


class Rook(Piece):
    def __init__(self, name: str, col: int, row: int):
        super().__init__(name, col, row)
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


class Knight(Piece):
    def __init__(self, name: str, col: int, row: int):
        super().__init__(name, col, row)
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
    def __init__(self, name: str, col: int, row: int):
        super().__init__(name, col, row)
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


class Queen(Piece):
    def __init__(self, name: str, col: int, row: int):
        super().__init__(name, col, row)
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
    def __init__(self, name: str, col: int, row: int):
        super().__init__(name, col, row)
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

            o = flatten(a, b, c, d, e, f, g, h)

            if _filter:
                # removes the king's valid moves that/are reachable by opponent pieces
                board.filter_moves_if_opponent_can_reach(self, None, o)

            return o

        return None
