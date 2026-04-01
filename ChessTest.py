import unittest
import Board


class TestMoves(unittest.TestCase):
    def test_valid_moves_filter(self):
        board = Board.Board((8, 8), None, None, fen='k7/7P/3b4/8/4K3/8/8/8')

        piece = board.get_piece_at(8, 7)
        piece2 = board.get_king(True)

        self.assertIsNotNone(piece)
        self.assertIsNotNone(piece2)

        self.assertEqual({(8, 8)}, piece.get_valid_moves(board))
        # self.assertEqual(6,len(piece2.get_valid_moves(board)))
        self.assertEqual({(4, 5), (4, 4), (4, 3), (5, 3), (6, 5), (6, 3)}, piece2.get_valid_moves(board))

    def test_fen(self):
        f = 'k7/7P/3b4/8/4K3/8/8/8'
        board = Board.Board((8, 8), None, None, fen=f)
        self.assertEqual(f, board.exportFEN())


if __name__ == '__main__':
    unittest.main()
