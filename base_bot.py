class Bot:
    """
    A standard chess bot.
    """

    def __init__(self, board, color: bool):
        """
        What am I supposed to say here?
        :param board: The current board
        """
        self.board = board
        self.color = color

    def make_move(self):
        ...
