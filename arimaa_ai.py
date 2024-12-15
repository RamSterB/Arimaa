# arimaa_ai.py - Refactorizado
from arimaa_utils import is_frozen, is_enemy, get_piece_strength, push_piece, pull_piece

def evaluate_board(board):
    piece_values = {
        "E": 5, "C": 4, "H": 3, "D": 2, "A": 1, "R": 0,  # Oro (mayúsculas)
        "e": -5, "c": -4, "h": -3, "d": -2, "a": -1, "r": 0  # Plata (minúsculas)
    }
    
    trap_positions = [(2, 2), (2, 5), (5, 2), (5, 5)]
    gold_goal_row = 7
    silver_goal_row = 0

    value = 0
    for row_idx, row in enumerate(board):
        for col_idx, piece in enumerate(row):
            if piece in piece_values:
                piece_value = piece_values[piece]
                if piece.lower() == "r":
                    distance_to_goal = (
                        gold_goal_row - row_idx if piece.isupper() else row_idx - silver_goal_row
                    )
                    piece_value += 7 - distance_to_goal
                if (row_idx, col_idx) in trap_positions:
                    piece_value -= 2
                value += piece_value

    mobility_gold = len(generate_moves(board, "black"))
    mobility_silver = len(generate_moves(board, "white"))
    value += (mobility_gold - mobility_silver) * 0.1
    return value

def generate_moves(board, player):
    moves = []

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and ((player == "white" and piece.islower()) or 
                          (player == "black" and piece.isupper())):
                if not is_frozen(board, (row, col)):
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_row, new_col = row + dr, col + dc
                        if (0 <= new_row < 8 and 0 <= new_col < 8 and 
                            board[new_row][new_col] is None):
                            moves.append(((row, col), (new_row, new_col)))
                    moves.extend(generate_push_pull_moves(board, (row, col), piece))
    return moves

def generate_push_pull_moves(board, position, piece):
    push_pull_moves = []
    strength = get_piece_strength(piece)
    row, col = position
    adjacent_positions = [(row + dr, col + dc) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

    for adj_row, adj_col in adjacent_positions:
        if 0 <= adj_row < 8 and 0 <= adj_col < 8:
            adjacent_piece = board[adj_row][adj_col]
            if adjacent_piece and is_enemy(piece, adjacent_piece):
                if get_piece_strength(adjacent_piece) < strength:
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_row, new_col = adj_row + dr, adj_col + dc
                        if (0 <= new_row < 8 and 0 <= new_col < 8 and 
                            board[new_row][new_col] is None):
                            score = evaluar_push_pull(board, (row, col), (new_row, new_col))
                            if score > 0:
                                push_pull_moves.append(("push", (row, col), (adj_row, adj_col), (new_row, new_col)))
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        pull_row, pull_col = row + dr, col + dc
                        if (0 <= pull_row < 8 and 0 <= pull_col < 8 and 
                            board[pull_row][pull_col] is None):
                            score = evaluar_push_pull(board, (row, col), (pull_row, pull_col))
                            if score > 0:
                                push_pull_moves.append(("pull", (row, col), (adj_row, adj_col), (pull_row, pull_col)))
    return push_pull_moves

def evaluar_push_pull(board, origin, destination):
    score = 0
    traps = [(2,2), (2,5), (5,2), (5,5)]
    for trap in traps:
        if manhattan_distance(destination, trap) < manhattan_distance(origin, trap):
            score += 3
    if 2 <= destination[0] <= 5 and 2 <= destination[1] <= 5:
        score += 2
    return score

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def apply_move(board, move):
    new_board = [row[:] for row in board]
    if len(move) == 2:
        start, end = move
        new_board[end[0]][end[1]] = new_board[start[0]][start[1]]
        new_board[start[0]][start[1]] = None
    elif len(move) == 4:
        move_type, origin, affected, destination = move
        if move_type == "push":
            push_piece(new_board, origin, affected, destination)
        elif move_type == "pull":
            pull_piece(new_board, origin, affected, destination)
    return new_board

def minimax(board, depth, is_maximizing_player, alpha=float('-inf'), beta=float('inf')):
    if depth == 0:
        return evaluate_board(board)

    moves = generate_moves(board, "black" if is_maximizing_player else "white")
    moves = sorted(moves, key=lambda m: evaluar_movimiento(board, m), reverse=is_maximizing_player)

    if is_maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval = minimax(new_board, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval = minimax(new_board, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def evaluar_movimiento(board, move):
    if len(move) == 2:
        return evaluate_board(apply_move(board, move))
    elif len(move) == 4:
        _, origin, _, destination = move
        return evaluar_push_pull(board, origin, destination)

def find_best_move(board, player):
    best_move = None
    best_value = float('-inf') if player == "black" else float('inf')
    moves = generate_moves(board, player)
    moves = sorted(moves, key=lambda m: evaluar_movimiento(board, m), reverse=(player == "black"))

    for move in moves:
        new_board = apply_move(board, move)
        move_value = minimax(new_board, 2, player == "white")
        if (player == "black" and move_value > best_value) or (player == "white" and move_value < best_value):
            best_value = move_value
            best_move = move
    return best_move
