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


def list_sum(l):
    r = set()

    for i in l:
        for x in i:
            r.add(x)

    return r


class PieceError(BaseException):
    def __init__(self, name: str):
        self.error: str = name

    def __str__(self):
        return self.error


class Piece:
    def __init__(self, name: str, col: int, row: int, board, win=False):
        self.piece: str = name
        self.color: bool = name.isupper()  # uppercase is w
        self.col: int = col
        self.row: int = row
        self.win = win
        self.moves: set = set()
        # self.king = board.get_king(self.color)

    def is_white(self):
        return self.color

    def get_name(self):
        return self.piece if not self.win else 'W' if self.color else 'w'

    @staticmethod
    def get_piece_icon(name):
        global piece_icons

        return piece_icons[name]

    def get_icon(self):
        return Piece.get_piece_icon(self.get_name())

    def get_valid_moves(self, board, ignore_turn=False, filter=True):
        # if self.moves is not None:
        #     return self.moves
        # else:
        if self.color == board.turn or ignore_turn:
            self.__compute_valid_moves(board, ignore_turn, filter)
            return self.moves
        return None

    def __compute_valid_moves(self, board, ignore_turn=False, filter=True):
        ...

    def go_to(self, c, r):
        self.col = c
        self.row = r

        return self.col, self.row

    @staticmethod
    def create_piece(name: str, col, row, board):
        match name.lower():
            case 'p':
                return Pawn(name, col, row, board)

            case 'r':
                return Rook(name, col, row, board)

            case 'n':
                return Knight(name, col, row, board)

            case 'b':
                return Bishop(name, col, row, board)

            case 'q':
                return Queen(name, col, row, board)

            case 'k':
                return King(name, col, row, board)

            case 'w':
                return King(name, col, row, board, True)

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

    def line_movement(self, dr: int, dc: int, board, max_range, color, no_turn=False):
        """
        :param no_turn:
        :param color: piece color
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

            elif board.get_piece_at(c, r).color != color or (board.get_piece_at(c, r) and no_turn):
                valid_moves.append((c, r))
                break

            else:
                break

            if n >= max_range:
                break

        return valid_moves


skip = False


class Pawn(Piece):
    def __compute_valid_moves(self, board, ignore_turn=False, filter=True):
        def move(m):
            # attack / capture
            global skip
            if board.get_piece_at(self.col + 1, self.row + m) is not None and \
                    board.get_piece_at(self.col + 1, self.row + m).color != self.color or ignore_turn:
                valid_moves.add((self.col + 1, self.row + m))

            if board.get_piece_at(self.col - 1, self.row + m) is not None and \
                    board.get_piece_at(self.col - 1, self.row + m).color != self.color or ignore_turn:
                valid_moves.add((self.col - 1, self.row + m))

            # normal
            print(self.col, self.row + m)
            if board.get_piece_at(self.col, self.row + m) is None:
                valid_moves.add((self.col, self.row + m))

            else:
                skip = True

            # double
            if ((m > 0 and self.row == 2) or (m < 0 and self.row == board.rows - 1)
                and board.get_piece_at(self.col, self.row + m + m) is None) and board.get_piece_at(
                self.col, self.row + m + m) is None and not skip:
                valid_moves.add((self.col, self.row + m + m))

        valid_moves: set = set()

        if self.color == board.turn or ignore_turn:
            move(1 if self.color else -1)

        self.moves = valid_moves


class Rook(Piece):
    def __compute_valid_moves(self, board, ignore_turn=False, filter=True):
        if self.color == board.turn or ignore_turn:
            a = self.line_movement(1, 0, board, 8, self.color, ignore_turn)
            b = self.line_movement(-1, 0, board, 8, self.color, ignore_turn)
            c = self.line_movement(0, 1, board, 8, self.color, ignore_turn)
            d = self.line_movement(0, -1, board, 8, self.color, ignore_turn)

            o = {a, b, c, d}

            self.moves = list_sum(o)



class Knight(Piece):
    def __compute_valid_moves(self, board, ignore_turn=False, filter=True):
        valid_moves: set = set()
        if self.color == board.turn or ignore_turn:

            moves = {0: (self.col + 2, self.row + 1), 1: (self.col + 2, self.row - 1), 2: (self.col + 1, self.row + 2),
                     3: (self.col - 1, self.row + 2), 4: (self.col + 1, self.row - 2), 5: (self.col - 2, self.row - 1),
                     6: (self.col - 2, self.row + 1), 7: (self.col - 1, self.row - 2)}

            for p in range(len(moves)):
                if board.is_valid_cell(*moves[p]) and self.color == board.turn:
                    if board.get_piece_at(*moves[p]) is not None:
                        if board.get_piece_at(*moves[p]).color != self.color:
                            valid_moves.add(moves[p])
                    else:
                        valid_moves.add(moves[p])

        self.moves = valid_moves


class Bishop(Piece):
    def __compute_valid_moves(self, board, ignore_turn=False, filter=True):
        self.moves = set()
        if self.color == board.turn or ignore_turn:
            a = self.line_movement(-1, 1, board, 8, self.color, ignore_turn)
            b = self.line_movement(1, -1, board, 8, self.color, ignore_turn)
            c = self.line_movement(1, 1, board, 8, self.color, ignore_turn)
            d = self.line_movement(-1, -1, board, 8, self.color, ignore_turn)

            o = {a, b, c, d}

            self.moves = list_sum(o)


class Queen(Piece):
    def __compute_valid_moves(self, board, ignore_turn=False, filter=True):
        self.moves = set()
        if self.color == board.turn or ignore_turn:
            # - & |
            a = self.line_movement(1, 0, board, 8, self.color, ignore_turn)
            b = self.line_movement(-1, 0, board, 8, self.color, ignore_turn)
            c = self.line_movement(0, 1, board, 8, self.color, ignore_turn)
            d = self.line_movement(0, -1, board, 8, self.color, ignore_turn)

            # \ & /
            e = self.line_movement(-1, 1, board, 8, self.color, ignore_turn)
            f = self.line_movement(1, -1, board, 8, self.color, ignore_turn)
            g = self.line_movement(1, 1, board, 8, self.color, ignore_turn)
            h = self.line_movement(-1, -1, board, 8, self.color, ignore_turn)

            o = {a, b, c, d, e, f, g, h}

            # filter piece if piece can be eaten by an opp piece excluding K P & N
            # if so then 4 each valid move of piece: move there and if the threatening piece(s loop) can capture king
            # remove current valid move

            self.moves = list_sum(o)


class King(Piece):
    def __compute_valid_moves(self, board, ignore_turn=False, filter=True):
        self.moves = set()
        if self.color == board.turn or ignore_turn:
            a = self.line_movement(1, 0, board, 0, self.color, ignore_turn)
            b = self.line_movement(1, 1, board, 0, self.color, ignore_turn)
            c = self.line_movement(0, 1, board, 0, self.color, ignore_turn)
            d = self.line_movement(-1, 0, board, 0, self.color, ignore_turn)
            e = self.line_movement(-1, 1, board, 0, self.color, ignore_turn)
            f = self.line_movement(-1, -1, board, 0, self.color, ignore_turn)
            g = self.line_movement(0, -1, board, 0, self.color, ignore_turn)
            h = self.line_movement(1, -1, board, 0, self.color, ignore_turn)
            _ = [(self.col, self.row)]

            o = list_sum([a, b, c, d, e, f, g, h, _])
            if filter:
                opp_pieces = board.pieces[not self.color]
                p: Piece

                for p in opp_pieces:
                    p.get_valid_moves(board, ignore_turn=True, filter=False)
                    o.difference_update(p.moves)

            self.moves = o
