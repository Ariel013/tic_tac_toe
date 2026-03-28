import random


def get_ai_move(board, ai_player, difficulty):
    if difficulty == "easy":
        return _random_move(board)
    elif difficulty == "medium":
        return _minimax_move(board, ai_player, max_depth=2)
    else:  # hard
        return _minimax_move(board, ai_player, max_depth=9)


def _random_move(board):
    empty = _empty_cells(board)
    return random.choice(empty) if empty else None


def _minimax_move(board, ai_player, max_depth):
    human = "O" if ai_player == "X" else "X"
    best_score = float("-inf")
    best_move = None
    for r, c in _empty_cells(board):
        board[r][c] = ai_player
        score = _minimax(board, 0, False, ai_player, human, max_depth)
        board[r][c] = None
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move


def _minimax(board, depth, is_maximizing, ai_player, human, max_depth):
    winner = _check_winner(board)
    if winner == ai_player:
        return 10 - depth
    if winner == human:
        return depth - 10
    empty = _empty_cells(board)
    if not empty or depth >= max_depth:
        return 0

    if is_maximizing:
        best = float("-inf")
        for r, c in empty:
            board[r][c] = ai_player
            best = max(best, _minimax(board, depth + 1, False, ai_player, human, max_depth))
            board[r][c] = None
        return best
    else:
        best = float("inf")
        for r, c in empty:
            board[r][c] = human
            best = min(best, _minimax(board, depth + 1, True, ai_player, human, max_depth))
            board[r][c] = None
        return best


def _empty_cells(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] is None]


def _check_winner(board):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None
