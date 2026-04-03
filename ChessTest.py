import unittest
import Board
from Pieces import flatten


class ChessTest(unittest.TestCase):
    def test_valid_moves_filter(self):
        board = Board.Board((8, 8), None, None, fen='k7/7P/3b4/8/4K3/8/8/8')

        piece = board.get_piece_at(8, 7)
        piece2 = board.get_king(True)

        self.assertIsNotNone(piece)
        self.assertIsNotNone(piece2)

        self.assertEqual({(8, 8)}, piece.get_valid_moves(board))
        self.assertEqual({(4, 5), (4, 4), (4, 3), (5, 3), (6, 5), (6, 3)}, piece2.get_valid_moves(board))

    def test_valid_moves_filter_2(self):
        board = Board.Board((8, 8), None, None, fen='3qkbnr/3pp2p/6Q1/8/4B/3/8/8')
        board.printASCII()
        pawn = board.get_piece_at(8, 7)
        self.assertIsNotNone(pawn)

        queen = board.get_piece_at(7, 6)
        pcs = board.get_pieces()[queen.color]
        self.assertEqual(2, len(pcs))

        undo = board.go_to(7, 6, pawn, True)
        pcs = board.get_pieces()[queen.color]
        self.assertEqual(1, len(pcs))

        board.undo_go_to(undo)
        pcs = board.get_pieces()[queen.color]
        self.assertEqual(2, len(pcs))

        self.assertEqual({(7, 6)}, pawn.get_valid_moves(board, no_turn=True))

    def test_fen(self):
        f = 'k7/7P/3b4/8/4K3/8/8/8'
        board = Board.Board(fen=f)
        self.assertEqual(f, board.exportFEN())

    def test_valid_move_fen(self):
        board = Board.Board()

        fen1 = board.exportFEN()
        board.get_piece_at(5, 2).get_valid_moves(board)
        fen2 = board.exportFEN()

        self.assertEqual(fen1, fen2)

    def test_undo_move(self):
        board = Board.Board()
        p = board.get_piece_at(5, 2)

        pcb = board.get_pieces()
        undo = board.go_to(5, 4, p, lw=True)
        pc = flatten(board.get_pieces())

        self.assertEqual(len(flatten(pcb)), len(flatten(pc)))

        board.undo_go_to(undo)


if __name__ == '__main__':
    unittest.main()
