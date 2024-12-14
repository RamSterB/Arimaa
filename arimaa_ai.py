from arimaa_utils import is_frozen

def evaluate_board(board):
    piece_values = {
        "E": 5, "C": 4, "H": 3, "D": 2, "A": 1, "R": 0,  # Oro (mayúsculas)
        "e": -5, "c": -4, "h": -3, "d": -2, "a": -1, "r": 0  # Plata (minúsculas)
    }
    
    # Factores adicionales para evaluación
    trap_positions = [(2, 2), (2, 5), (5, 2), (5, 5)]
    gold_goal_row = 7  # Los conejos de oro quieren llegar a la fila 7
    silver_goal_row = 0  # Los conejos de plata quieren llegar a la fila 0

    value = 0
    for row_idx, row in enumerate(board):
        for col_idx, piece in enumerate(row):
            if piece in piece_values:
                # Valor base de la pieza
                piece_value = piece_values[piece]
                
                # Agregar incentivos según la posición
                if piece.lower() == "r":  # Evaluación especial para conejos
                    distance_to_goal = (
                        gold_goal_row - row_idx if piece.isupper() else row_idx - silver_goal_row
                    )
                    piece_value += 7 - distance_to_goal  # Más puntos por estar cerca del objetivo
                
                # Penalizar/bonificar posiciones cerca de trampas
                if (row_idx, col_idx) in trap_positions:
                    piece_value -= 2  # Riesgo de trampa
                
                # Agregar al valor total
                value += piece_value
    
    # Opcional: agrega un factor por movilidad (número de movimientos posibles)
    mobility_gold = len(generate_moves(board, "black"))
    mobility_silver = len(generate_moves(board, "white"))
    value += (mobility_gold - mobility_silver) * 0.1  # Movilidad importa, pero no demasiado
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
    
    return moves

def minimax(board, depth, is_maximizing_player, alpha=float('-inf'), beta=float('inf')):
    if depth == 0:
        return evaluate_board(board)
    
    moves = generate_moves(board, "black" if is_maximizing_player else "white")
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
    """Encuentra el mejor movimiento usando minimax."""
    best_move = None
    best_value = float('-inf')
    moves = generate_moves(board, "black")
    
    if not moves:
        return None
        
    for move in moves:
        new_board = [row[:] for row in board]
        start, end = move
        new_board[end[0]][end[1]] = new_board[start[0]][start[1]]
        new_board[start[0]][start[1]] = None
        move_value = minimax(new_board, 2, False)
        if move_value > best_value:
            best_value = move_value
            best_move = move
    return best_move