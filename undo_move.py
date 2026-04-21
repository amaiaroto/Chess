from pieces import Piece


class UndoMove:
    def __init__(self, board, source_piece: Piece,
                 target_pos, lw):
        assert source_piece is not None
        assert target_pos is not None and len(target_pos) == 2

        self.sp = source_piece
        self.sp_pos = source_piece.get_pos()
        self.piece_at_target = board.get_piece_at(*target_pos)
        self.pos_of_piece_at_target = target_pos
        self.lw = lw
