from arimaa_utils import is_frozen, is_enemy, get_piece_strength, push_piece, pull_piece

STEPS_TAKEN = 0  # Contador de pasos para empujar y arrastrar

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
                    # Movimientos básicos (desplazamientos)
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_row, new_col = row + dr, col + dc
                        if (0 <= new_row < 8 and 0 <= new_col < 8 and 
                            board[new_row][new_col] is None):
                            moves.append(((row, col), (new_row, new_col)))
                    
                    # Empujar o arrastrar
                    moves.extend(generate_push_pull_moves(board, (row, col), piece))
    
    return moves

def generate_push_pull_moves(board, position, piece):
    """Genera movimientos de empujar y arrastrar según las reglas de Arimaa."""
    push_pull_moves = []
    strength = get_piece_strength(piece)
    
    row, col = position
    adjacent_positions = [(row + dr, col + dc) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
    
    for adj_row, adj_col in adjacent_positions:
        if 0 <= adj_row < 8 and 0 <= adj_col < 8:
            adjacent_piece = board[adj_row][adj_col]
            
            # Empujar: pieza enemiga más débil
            if adjacent_piece and is_enemy(piece, adjacent_piece):
                if get_piece_strength(adjacent_piece) < strength:
                    for push_dr, push_dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        push_row, push_col = adj_row + push_dr, adj_col + push_dc
                        if (0 <= push_row < 8 and 0 <= push_col < 8 and 
                            board[push_row][push_col] is None):
                            try:
                                # El empuje cuesta 2 pasos
                                if STEPS_TAKEN  + 2 > 4:  # Verificar si hay suficientes pasos disponibles
                                    continue
                                # Corregir orden: (tablero, posición_empujador, posición_empujado, nueva_posición)
                                push_piece(board, (row, col), (adj_row, adj_col), (push_row, push_col))
                                push_pull_moves.append(('push', (row, col), (adj_row, adj_col), (push_row, push_col)))
                                STEPS_TAKEN += 2  # Incrementar el contador de pasos
                            except ValueError:
                                continue
            
            # Arrastrar
            if adjacent_piece and is_enemy(piece, adjacent_piece):
                if get_piece_strength(adjacent_piece) < strength:
                    for pull_dr, pull_dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        pull_row, pull_col = row + pull_dr, col + pull_dc
                        if (0 <= pull_row < 8 and 0 <= pull_col < 8 and 
                            board[pull_row][pull_col] is None):
                            try:
                                # El arrastre cuesta 2 pasos
                                if STEPS_TAKEN  + 2 > 4:  # Verificar si hay suficientes pasos disponibles
                                    continue
                                pull_piece(board, (row, col), (adj_row, adj_col), (pull_row, pull_col))
                                push_pull_moves.append(('pull', (row, col), (adj_row, adj_col), (pull_row, pull_col)))
                                STEPS_TAKEN  += 2  # Incrementar el contador de pasos
                            except ValueError:
                                continue
                                
    return push_pull_moves

def apply_move(board, move):
    """Aplica un movimiento (básico, empujar o arrastrar) y devuelve un nuevo tablero."""
    new_board = [row[:] for row in board]  # Crear una copia del tablero actual

    if len(move) == 2:  # Movimiento estándar
        start, end = move
        new_board[end[0]][end[1]] = new_board[start[0]][start[1]]
        new_board[start[0]][start[0]] = None
    elif len(move) == 3:  # Movimiento de empujar o arrastrar
        start, end, affected = move
        # Mover la pieza activa
        new_board[end[0]][end[1]] = new_board[start[0]][start[1]]
        new_board[start[0]][start[1]] = None
        # Mover la pieza afectada
        new_board[affected[0]][affected[1]] = new_board[end[0]][end[1]]
    return new_board

def minimax(board, depth, is_maximizing_player, alpha=float('-inf'), beta=float('inf')):
    """Algoritmo Minimax con poda alfa-beta y soporte para movimientos complejos."""
    if depth == 0:
        return evaluate_board(board)

    moves = generate_moves(board, "black" if is_maximizing_player else "white")
    if not moves:  # Si no hay movimientos posibles, evalúa el estado del tablero
        return evaluate_board(board)

    if is_maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_board = apply_move(board, move)  # Aplicar el movimiento
            eval = minimax(new_board, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:  # Poda
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = apply_move(board, move)  # Aplicar el movimiento
            eval = minimax(new_board, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:  # Poda
                break
        return min_eval

def find_best_move(board, player):
    """Encuentra el mejor movimiento usando minimax."""
    best_move = None
    best_value = float('-inf') if player == "black" else float('inf')
    moves = generate_moves(board, player)
    
    if not moves:
        return None
        
    for move in moves:
        new_board = apply_move(board, move)
        move_value = minimax(new_board, 2, player == "white")
        if (player == "black" and move_value > best_value) or (player == "white" and move_value < best_value):
            best_value = move_value
            best_move = move
    return best_move