from Pieces import Piece


class UndoMove:
    def __init__(self, board, source_piece: Piece,
                 target_pos):
        assert source_piece is not None
        target_pos = target_pos.get_pos()
        print(target_pos)
        assert target_pos is not None and len(target_pos) == 2
        self.sp = source_piece
        self.sp_pos = source_piece.get_pos()
        self.piece_at_target = board.get_piece_at(*target_pos)
        self.pos_of_piece_at_target = target_pos

    def undo(self, board):
        self.sp.go_to(*self.sp_pos)
        board.modify_pos(*self.pos_of_piece_at_target, self.piece_at_target)
