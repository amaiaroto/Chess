from base_bot import Bot
import pieces
import random


class Bot1(Bot):
    def make_move(self):
        my_pieces = [p for p in self.board.get_pieces()[self.color] if p.get_valid_moves(self.board)]
        value = self.board.evaluate_positions(self.color)
        moves = []

        for p in my_pieces:
            for m in p.get_valid_moves(self.board):
                undo = self.board.go_to(*m, p, lw=True)

                if value <= self.board.evaluate_positions(self.color):
                    moves.append((self.board.evaluate_positions(self.color), p, m))

                self.board.undo_go_to(undo)

        random.shuffle(moves)
        moves.sort(key=lambda x: x[0])
        move = moves[0]
        print(type(move[1]))
        self.board.go_to(*move[2], move[1])
