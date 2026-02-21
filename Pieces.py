import Board

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


class PieceError(BaseException):
    def __init__(self, name):
        self.error = name

    def __str__(self):
        return self.error


class Piece:
    def __init__(self, name, col: int, row: int):
        self.piece = name
        self.color = name.isupper()  # uppercase is w
        self.col = col
        self.row = row

    def is_white(self):
        return self.color

    def get_name(self):
        return self.piece

    def get_icon(self):
        global piece_icons

        return piece_icons[self.get_name()]

    def get_valid_moves(self, board: Board):
        valid_moves = []

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


class Pawn(Piece):
    def get_valid_moves(self, board: Board):

        def move(m):
            pos = (self.col + 1, self.row + m)

            if board.is_valid_cell(*pos) and board.get_piece_at(*pos) is not None:
                valid_moves.append(pos)

            pos = (self.col - 1, self.row + m)

            if board.is_valid_cell(*pos) and board.get_piece_at(*pos) is not None:
                valid_moves.append(pos)

            # normal
            pos = (self.col, self.row + m)

            if board.is_valid_cell(*pos) and board.get_piece_at(*pos) is None:
                valid_moves.append(pos)

                if (m > 0 and self.row == 2) or (m < 0 and self.row == (board.rows - 1)):
                    pos = (self.col, self.row + m)

                    if board.is_valid_cell(*pos) and board.get_piece_at(*pos) is None:
                        valid_moves.append((self.col, self.row + 2 * m))

        valid_moves = []
        if self.color == board.turn:
            move(-1 if self.color else 1)
        return valid_moves


class Rook(Piece):
    def get_valid_moves(self, board: Board):
        valid_moves = []

        for r in range(1, board.rows + 1):
            valid_moves.append((self.col, r))

        for c in range(1, board.columns + 1):
            valid_moves.append((c, self.row))

        del valid_moves[valid_moves.index((self.col, self.row))]

        return valid_moves


class Knight(Piece):
    def get_valid_moves(self, board: Board):
        valid_moves = []


class Bishop(Piece):
    def get_valid_moves(self, board: Board):
        valid_moves = []


class Queen(Piece):
    def get_valid_moves(self, board: Board):
        valid_moves = []


class King(Piece):
    def get_valid_moves(self, board: Board):
        valid_moves = [(self.col + 1, self.row), (self.col - 1, self.row), (self.col, self.row + 1),
                       (self.col, self.row - 1), (self.col + 1, self.row + 1), (self.col - 1, self.row - 1),
                       (self.col + 1, self.row - 1), (self.col - 1, self.row + 1)]

        if self.col == 8:
            try:
                valid_moves.remove((self.col + 1, self.row))

            except ValueError:
                pass

            try:
                valid_moves.remove((self.col + 1, self.row + 1))

            except ValueError:
                pass

            try:
                valid_moves.remove((self.col + 1, self.row - 1))

            except ValueError:
                pass

        if self.col == 1:
            try:
                valid_moves.remove((self.col - 1, self.row))

            except ValueError:
                pass

            try:
                valid_moves.remove((self.col - 1, self.row - 1))

            except ValueError:
                pass

            try:
                valid_moves.remove((self.col - 1, self.row + 1))

            except ValueError:
                pass

        if self.row == 8:
            try:
                valid_moves.remove((self.row + 1, self.col))

            except ValueError:
                pass

            try:
                valid_moves.remove((self.row + 1, self.col - 1))

            except ValueError:
                pass

            try:
                valid_moves.remove((self.row + 1, self.col + 1))

            except ValueError:
                pass

        if self.row == 1:
            try:
                valid_moves.remove((self.row - 1, self.col))

            except ValueError:
                pass

            try:
                valid_moves.remove((self.row - 1, self.col - 1))
            except ValueError:
                pass

            try:
                valid_moves.remove((self.row - 1, self.col + 1))
            except ValueError:
                pass

        if valid_moves:

            return valid_moves

        else:
            return 'stalemate' if False else 'checkmate'
