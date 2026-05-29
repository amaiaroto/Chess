from base_bot import Bot
import random


class Bot1(Bot):
    def make_move(self):
        my_pieces = [p for p in self.board.get_pieces()[self.color] if p.get_valid_moves(self.board)]
        value = self.board.evaluate_positions(self.color)
        moves = []
        optimal = {}

        # TODO: debug the 3 available moves for the bishop at 3,8.
        #  find out why the move that goes to 2,7 is preferred to the one that goes to 1,6 (eating one)

        # The bot prefers 2,7 instead of 1,6 because: ""
        best_moves_value = value
        for p in my_pieces:
            for m in p.get_valid_moves(self.board):
                undo = self.board.go_to(*m, p, lw=True)

                tmp = self.board.evaluate_positions(self.color)
                if tmp >= best_moves_value:
                    moves.append((tmp, p, m))
                    optimal[p] = m, self.board.get_piece_at(*m)
                    best_moves_value = tmp

                self.board.undo_go_to(undo)

        random.shuffle(moves)
        moves.sort(key=lambda x: x[0], reverse=True)

        if len(moves) > 0:
            move = moves[0]
            self.board.go_to(*move[2], move[1])
