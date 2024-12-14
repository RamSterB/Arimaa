def evaluate_board(board):
    piece_values = {
        "E": 5, "C": 4, "H": 3, "D": 2, "A": 1, "R": 0,
        "e": 5, "c": 4, "h": 3, "d": 2, "a": 1, "r": 0
    }
    value = 0
    for row in board:
        for piece in row:
            if piece:
                value += piece_values[piece] if piece.islower() else -piece_values[piece]
    return value

def generate_moves(board, player):
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and ((player == "silver" and piece.islower()) or (player == "gold" and piece.isupper())):
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] is None:
                        moves.append(((row, col), (new_row, new_col)))
    return moves

def minimax(board, depth, is_maximizing_player, alpha=float('-inf'), beta=float('inf')):
    if depth == 0:
        return evaluate_board(board)
    
    moves = generate_moves(board, "silver" if is_maximizing_player else "gold")
    if not moves:
        return evaluate_board(board)
    
    if is_maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_board = [row[:] for row in board]
            start, end = move
            new_board[end[0]][end[1]] = new_board[start[0]][start[1]]
            new_board[start[0]][start[1]] = None
            eval = minimax(new_board, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = [row[:] for row in board]
            start, end = move
            new_board[end[0]][end[1]] = new_board[start[0]][start[1]]
            new_board[start[0]][start[1]] = None
            eval = minimax(new_board, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board):
    best_move = None
    best_value = float('-inf')
    moves = generate_moves(board, "silver")
    for move in moves:
        new_board = [row[:] for row in board]
        start, end = move
        new_board[end[0]][end[1]] = new_board[start[0]][start[1]]
        new_board[start[0]][start[1]] = None
        move_value = minimax(new_board, 3, False)
        if move_value > best_value:
            best_value = move_value
            best_move = move
    return best_move