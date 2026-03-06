# from Chess import board

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

    def get_valid_moves(self, board, c=None, r=None):
        if not c:
            c = self.col
        if not r:
            r = self.row
            
        ...

    def go_to(self, c, r):
        self.col = c
        self.row = r

        return self.col, self.row

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

    def line_movement(self, dr: int, dc: int, board, max_range, color):
        """
        :param dr: delta row
        :param dc: delta col
        :param board: the board
        :param max_range: 0 based
        :return: valid moves
        """
        c = self.col
        r = self.row
        valid_moves = []

        for n in range(max(board.columns, board.columns)):
            c += dc
            r += dr

            if not board.is_valid_cell(c, r):
                break

            if board.get_piece_at(c, r) is None:
                valid_moves.append((c, r))

            else:
                valid_moves.append((c, r))
                break
            if n >= max_range:
                break

        return valid_moves


class Pawn(Piece):
    def get_valid_moves(self, board, c=None, r=None):
        def move(m):
            # attack / capture; \ /
            if board.get_piece_at(self.col + 1, self.row + 1) is not None and \
                    board.get_piece_at(self.col + 1, self.row + 1).color != self.color:
                valid_moves.append((self.col + 1, self.row + 1))

            if board.get_piece_at(self.col - 1, self.row + 1) is not None and \
                    board.get_piece_at(self.col - 1, self.row + 1).color != self.color:
                valid_moves.append((self.col - 1, self.row + 1))

            if (m > 0 and self.row == 2) or (m < 0 and self.row == board.rows - 1):
                # double; |\n         !
                valid_moves.extend(self.line_movement(m, 0, board, 1, self.color))
            else:
                # normal !
                valid_moves.extend(self.line_movement(m, 0, board, 0, self.color))

        valid_moves: list[tuple] = []

        if self.color == board.turn:
            move(1 if self.color else -1)

        return valid_moves


class Rook(Piece):
    def get_valid_moves(self, board, c=None, r=None):
        a = self.line_movement(1, 0, board, 8, self.color)
        b = self.line_movement(-1, 0, board, 8, self.color)
        c = self.line_movement(0, 1, board, 8, self.color)
        d = self.line_movement(0, -1, board, 8, self.color)

        o = [a, b, c, d]

        return list_sum(o)


class Knight(Piece):
    def get_valid_moves(self, board, c=None, r=None):
        valid_moves: list[tuple] = []
        moves = {0: (self.col + 2, self.row + 1), 1: (self.col + 2, self.row - 1), 2: (self.col + 1, self.row + 2),
                 3: (self.col - 1, self.row + 2), 4: (self.col + 1, self.row - 2), 5: (self.col - 2, self.row - 1),
                 6: (self.col - 2, self.row + 1), 7: (self.col - 1, self.row - 2)}

        for p in range(len(moves)):
            if board.is_valid_cell(*moves[p]):
                if board.get_piece_at(*moves[p]) is not None:
                    if board.get_piece_at(*moves[p]).color != self.color:
                        valid_moves.append(moves[p])
                else:
                    valid_moves.append(moves[p])

        return valid_moves


class Bishop(Piece):
    def get_valid_moves(self, board, c=None, r=None):
        a = self.line_movement(-1, 1, board, 8, self.color)
        b = self.line_movement(1, -1, board, 8, self.color)
        c = self.line_movement(1, 1, board, 8, self.color)
        d = self.line_movement(-1, -1, board, 8, self.color)

        o = [a, b, c, d]

        return list_sum(o)


class Queen(Piece):
    def get_valid_moves(self, board, c=None, r=None):
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

        o = [a, b, c, d, e, f, g, h]

        return list_sum(o)


class King(Piece):
    def get_valid_moves(self, board, c=None, r=None):
        a = self.line_movement(1, 0, board, 0, self.color)
        b = self.line_movement(1, 1, board, 0, self.color)
        c = self.line_movement(0, 1, board, 0, self.color)
        d = self.line_movement(-1, 0, board, 0, self.color)
        e = self.line_movement(-1, 1, board, 0, self.color)
        f = self.line_movement(-1, -1, board, 0, self.color)
        g = self.line_movement(0, -1, board, 0, self.color)
        h = self.line_movement(1, -1, board, 0, self.color)

        o = [a, b, c, d, e, f, g, h]

        return list_sum(o)
