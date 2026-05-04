from base_bot import Bot

import random


class Bot0(Bot):
    """
    A random moves bot
    """

    def make_move(self):
        piece = random.choice(list([p for p in self.board.get_pieces()[self.color] if p.get_valid_moves(self.board)]))
        move = random.choice(list(piece.get_valid_moves(self.board)))
        self.board.go_to(*move, piece)
