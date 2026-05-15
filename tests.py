import unittest
import board
import pieces
from bots import bot1
from pieces import flatten


class ChessTest(unittest.TestCase):
    def test_valid_moves_filter(self):
        _board = board.Board((8, 8), None, None, fen='k7/7P/3b4/8/4K3/8/8/8 w')

        piece = _board.get_piece_at(8, 7)
        piece2 = _board.get_king(True)

        self.assertIsNotNone(piece)
        self.assertIsNotNone(piece2)

        self.assertEqual({(8, 8)}, piece.get_valid_moves(_board))
        self.assertEqual({(4, 5), (4, 4), (4, 3), (5, 3), (6, 5), (6, 3)}, piece2.get_valid_moves(_board))

    def test_valid_moves_filter_2(self):
        _board = board.Board((8, 8), None, None, fen='3qkbnr/3pp2p/6Q1/8/4B/8/8/8 w')
        _board.printASCII()
        pawn = _board.get_piece_at(8, 7)
        self.assertIsNotNone(pawn)

        queen = _board.get_piece_at(7, 6)
        pcs = _board.get_pieces()[queen.color]
        self.assertEqual(2, len(pcs))

        undo = _board.go_to(7, 6, pawn, True)
        pcs = _board.get_pieces()[queen.color]
        self.assertEqual(1, len(pcs))

        _board.undo_go_to(undo)
        pcs = _board.get_pieces()[queen.color]
        self.assertEqual(2, len(pcs))

        self.assertEqual({(7, 6)}, pawn.get_valid_moves(_board, no_turn=True))

    def test_valid_moves_filter_3(self):
        _board = board.Board(fen='3pkp2/3p1Q2/8/3B3/8/8/8/8 b')
        king = _board.get_king(False)
        self.assertEqual(set(), king.get_valid_moves(_board))

    def test_fen(self):
        f = 'k7/7P/3b4/8/4K3/8/8/8 w'
        _board = board.Board(fen=f)
        self.assertEqual(f, _board.exportFEN())

    def test_valid_move_fen(self):
        _board = board.Board()

        fen1 = _board.exportFEN()
        _board.get_piece_at(5, 2).get_valid_moves(_board)
        fen2 = _board.exportFEN()

        self.assertEqual(fen1, fen2)

    def test_undo_move(self):
        _board = board.Board()
        p = _board.get_piece_at(5, 2)

        pcb = _board.get_pieces()
        undo = _board.go_to(5, 4, p, lw=True)
        pc = flatten(_board.get_pieces())

        self.assertEqual(len(flatten(pcb)), len(flatten(pc)))

        _board.undo_go_to(undo)

    def test_bot1(self):
        _board = board.Board(fen='rnbqkbnr/ppp1pppp/3p4/1B6/4P/3/8/PPPP1PPP/RNBQK1NR b', bot=bot1.Bot1)

        _board.bot.make_move()
        print(_board.exportFEN())
        self.assertNotEqual(_board.exportFEN(), 'rnb1kbnr/ppppqppp/3p4/1B6/8/8/PPPP1PPP w')

    def test_flatten(self):
        iterable = [
            [(6, 2), (1, 7), (9, 0), (2, 5)],
            [(1, 2), (7, 2), (6, 7)],
            [(9, 5), (6, 3), [(9, 1), (5, 6), (7, 2)]],
            [(2, 3), (6, 3), (1, 3), (8, 6), (8, 6)],
            [(2, 5), (5, 9), (0, 2)],
            [(2, 5), (5, 9), (0, 2)]
        ]

        flattened_iterable = pieces.flatten(iterable)

        self.assertEqual(type(flattened_iterable), set)
        self.assertEqual(len([t for t in flattened_iterable if isinstance(t, tuple)]), 16)
        self.assertEqual(len(flattened_iterable), 16)

        flattened_iterable = pieces.flatten(iterable, keep_duplicates=True)

        self.assertEqual(type(flattened_iterable), list)
        self.assertEqual(len([t for t in flattened_iterable if isinstance(t, tuple)]), 23)
        self.assertEqual(len(flattened_iterable), 23)

if __name__ == '__main__':
    unittest.main()
