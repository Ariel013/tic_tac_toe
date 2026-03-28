class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[None] * 3 for _ in range(3)]
        self.current_player = "X"
        self.winner = None
        self.is_draw = False

    def make_move(self, row, col):
        if self.board[row][col] is not None or self.winner or self.is_draw:
            return False
        self.board[row][col] = self.current_player
        self._check_result()
        if not self.winner and not self.is_draw:
            self.current_player = "O" if self.current_player == "X" else "X"
        return True

    def _check_result(self):
        b = self.board
        for row in range(3):
            if b[row][0] == b[row][1] == b[row][2] and b[row][0] is not None:
                self.winner = b[row][0]
                return
        for col in range(3):
            if b[0][col] == b[1][col] == b[2][col] and b[0][col] is not None:
                self.winner = b[0][col]
                return
        if b[0][0] == b[1][1] == b[2][2] and b[0][0] is not None:
            self.winner = b[0][0]
            return
        if b[0][2] == b[1][1] == b[2][0] and b[0][2] is not None:
            self.winner = b[0][2]
            return
        if all(b[r][c] is not None for r in range(3) for c in range(3)):
            self.is_draw = True

    def get_winning_line(self):
        b = self.board
        for row in range(3):
            if b[row][0] == b[row][1] == b[row][2] and b[row][0] is not None:
                return ("row", row)
        for col in range(3):
            if b[0][col] == b[1][col] == b[2][col] and b[0][col] is not None:
                return ("col", col)
        if b[0][0] == b[1][1] == b[2][2] and b[0][0] is not None:
            return ("diag", 0)
        if b[0][2] == b[1][1] == b[2][0] and b[0][2] is not None:
            return ("diag", 1)
        return None
