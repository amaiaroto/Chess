import logging
import unittest
import board
import pieces
from bots import bot1
from pieces import flatten


class ChessTest(unittest.TestCase):
    @staticmethod
    def test_startup():
        board.Board()

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
        pcw = flatten(_board.get_pieces())

        self.assertEqual(len(flatten(pcb)), len(flatten(pcw)))

        _board.undo_go_to(undo)
        _board.check_consistency()

    def test_bot1(self):
        _board = board.Board(fen='rnbqkbnr/ppp1pppp/3p4/1B6/4P3/8/PPPP1PPP/RNBQK1NR b', bot=bot1.Bot1)

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

    def test_bot1_2(self):
        _board = board.Board(fen='r1bqkbnr/1ppppppp/3N4/p1n5/8/8/PPPPPPPP/RNBQKB1R b', bot=bot1.Bot1)

        bk = _board.get_king(False)
        tps = _board.get_pieces_under_threat(False)

        self.assertIn(bk, tps, "King not under threat when supposed to be")

        _board.bot.make_move()

        tps = _board.get_pieces_under_threat(False)

        self.assertNotIn(bk, tps, "King under threat when not supposed to be")

    def test_bot1_eating(self):
        """
        r . b q k b n r
        p . . p . p p .
        B p . . . . . p
        . . p . p . . .
        . . . P P P . .
        . . . . . . . .
        P P P . . . P P
        R N B Q K 1 N R

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        r1bqkbnr/p2p1pp1/Bp5p/2p1p3/3PPP2/8/PPP3PP/RNBQK1NR b
        """

        # TODO: Finish "test_bot1_eating"

        _board = board.Board(fen='r1bqkbnr/p2p1pp1/Bp5p/2p1p3/3PPP2/8/PPP3PP/RNBQK1NR b', bot=bot1.Bot1)
        _board.bot.make_move()

        self.assertEqual(_board.exportFEN(), 'r2qkbnr/p2p1pp1/bp5p/2p1p3/3PPP2/8/PPP3PP/RNBQK1NR w')

    def test_checkmate(self):
        """
             r . . . k b n r
             p . P . . p p .
             . p B . . . . .
             . . p . . . . p
             . . . . . P . .
             . . . . . . P .
             P P P . . . . P
             R N B Q K . N R

             ~~~~

             r3kbnr/p4pp1/1pB2p2/2p4p/5P2/6P1/PPP4P/RNBQK1NR b
        """

        _board = board.Board(fen='r3kbnr/p1P2pp1/1pB2p2/2p4p/5P2/6P1/PPP4P/RNBQK1NR b', bot=lambda x, y: None)
        self.assertFalse(_board.checkmate())

    def test_checkmate_2(self):
        """
             . . . r . . . .
             r . . k . . b .
             . p q . . p . p
             p K p b p n p .
             . n . p . . . .
             . . . . . . . .
             P P P P . P P P
             R N B Q . B N R

            ~~~~

            3r4/r2k2b1/1pq2p1p/pKpbpnp1/1n1p4/8/PPPP1PPP/RNBQ1BNR w
        """

        _board = board.Board(fen='3r4/r2k2b1/1pq2p1p/pKpbpnp1/1n1p4/8/PPPP1PPP/RNBQ1BNR w')
        self.assertTrue(_board.checkmate())

    def test_pawn_last_row(self):
        ...


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    unittest.main()
