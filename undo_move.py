import pieces
from pieces import CastlingSides


class UndoMove:
    def __init__(self, board, source_piece,
                 target_pos, lw, pp=False, castling=CastlingSides.none):
        assert source_piece is not None
        assert target_pos is not None and len(target_pos) == 2

        delta = source_piece.col - target_pos[0]
        castling = CastlingSides.none
        if abs(delta) > 1 and isinstance(source_piece, pieces.King):
            castling = CastlingSides.king if delta > 0 else CastlingSides.queen
        self.source_piece_has_moved = source_piece.has_moved
        self.sp = source_piece
        self.sp_pos = source_piece.get_pos()
        self.piece_at_target = board.get_piece_at(*target_pos)
        self.pos_of_piece_at_target = target_pos
        self.lw = lw
        self.pp = pp
        self.castling = castling
