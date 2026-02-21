piece_icons: dict[str, str] = {
    'K': '♔',
    'Q': '♕',
    'R': '♖',
    'B': '♗',
    'N': '♘',
    'P': '♙',

    'k': '♚',
    'q': '♛',
    'r': '♜',
    'b': '♝',
    'n': '♞',
    'p': '♟',
}


def list_sum(l):
    r = []

    for i in l:
        r.extend(i)

    return r


class PieceError(BaseException):
    def __init__(self, name: str):
        self.error: str = name

    def __str__(self):
        return self.error


class Piece:
    def __init__(self, name: str, col: int, row: int):
        self.piece: str = name
        self.color: bool = name.isupper()  # uppercase is w
        self.col: int = col
        self.row: int = row

    def is_white(self):
        return self.color

    def get_name(self):
        return self.piece

    def get_icon(self):
        global piece_icons

        return piece_icons[self.get_name()]

    def get_valid_moves(self, board):
        ...

    def move(self, col, row):
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

        raise PieceError('Not valid name')

    def line_movement(self, dr: int, dc: int, board, max_range):
        c = self.col
        r = self.row
        valid_moves = []

        for n in range(max(board.columns, board.columns)):
            c += dc
            r += dr

            if n >= max_range:
                break

            if not board.is_valid_cell(c, r):
                break

            if board.get_piece_at(c, r) is None:
                valid_moves.append((c, r))

            else:
                break

        return valid_moves


class Pawn(Piece):
    def get_valid_moves(self, board):
        def move(m):
            # attack / capture; \ /
            if board.get_piece_at(self.col + 1, self.row + 1) is not None and \
                    board.get_piece_at(self.col + 1, self.row + 1).color != self.color:
                valid_moves.append((self.col + 1, self.row + 1))

            if board.get_piece_at(self.col - 1, self.row + 1) is not None and \
                    board.get_piece_at(self.col - 1, self.row + 1).color != self.color:
                valid_moves.append((self.col - 1, self.row + 1))

            # normal !
            valid_moves.extend(self.line_movement(m, 0, board, 1))

            if (m > 0 and self.row == board.rows // 4) or (m < 0 and self.row == board.rows - 1):
                # double; |\n         !
                valid_moves.extend(self.line_movement(m, 0, board, 1))

        valid_moves: list[tuple] = []

        if self.color == board.turn:
            move(1 if self.color else -1)

        return valid_moves


class Rook(Piece):
    def get_valid_moves(self, board):
        a = self.line_movement(1, 0, board, 9)
        b = self.line_movement(-1, 0, board, 9)
        c = self.line_movement(0, 1, board, 9)
        d = self.line_movement(0, -1, board, 9)

        o = [a, b, c, d]

        return list_sum(o)


class Knight(Piece):
    def get_valid_moves(self, board):
        valid_moves: list[tuple] = []

        return valid_moves


class Bishop(Piece):
    def get_valid_moves(self, board):
        a = self.line_movement(-1, 1, board, 9)
        b = self.line_movement(1, -1, board, 9)
        c = self.line_movement(1, 1, board, 9)
        d = self.line_movement(-1, -1, board, 9)

        o = [a, b, c, d]

        return list_sum(o)


class Queen(Piece):
    def get_valid_moves(self, board):
        # - & |
        a = self.line_movement(1, 0, board, 9)
        b = self.line_movement(-1, 0, board, 9)
        c = self.line_movement(0, 1, board, 9)
        d = self.line_movement(0, -1, board, 9)

        # \ & /
        e = self.line_movement(-1, 1, board, 9)
        f = self.line_movement(1, -1, board, 9)
        g = self.line_movement(1, 1, board, 9)
        h = self.line_movement(-1, -1, board, 9)

        o = [a, b, c, d, e, f, g, h]

        return list_sum(o)


class King(Piece):
    def get_valid_moves(self, board):
        a = self.line_movement(1, 0, board, 1)
        b = self.line_movement(1, 1, board, 1)
        c = self.line_movement(0, 1, board, 1)
        d = self.line_movement(-1, 0, board, 1)
        e = self.line_movement(-1, 1, board, 1)
        f = self.line_movement(-1, -1, board, 1)
        g = self.line_movement(0, -1, board, 1)
        h = self.line_movement(1, -1, board, 1)

        o = [a, b, c, d, e, f, g, h]

        return list_sum(o)
