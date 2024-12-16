piece_weights = {
    "E": 5, "A": 4, "H": 3, "D": 2, "C": 1, "R": 0,
    "e": 5, "a": 4, "h": 3, "d": 2, "c": 1, "r": 0
}

def is_frozen(board, position):
    row, col = position
    piece = board[row][col]
    if not piece:
        return False

    allies = set("RCDHEP" if piece.isupper() else "rcdhep")
    enemies = set("rcdhep" if piece.isupper() else "RCDHEP")

    has_ally = False
    is_overpowered = False
    
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        adj_row, adj_col = row + dr, col + dc
        if 0 <= adj_row < 8 and 0 <= adj_col < 8:
            adj_piece = board[adj_row][adj_col]
            if adj_piece:
                if adj_piece in allies:
                    has_ally = True
                elif adj_piece in enemies and piece_weights[adj_piece] > piece_weights[piece]:
                    is_overpowered = True

    return is_overpowered and not has_ally

def is_enemy(piece, other):
    return (piece.isupper() and other.islower()) or (piece.islower() and other.isupper())

def get_piece_strength(piece):
    """Devuelve la fuerza de una pieza según las reglas de Arimaa."""
    strength_order = {"E": 5, "C": 1, "H": 3, "D": 2, "A": 4, "R": 0,
                      "e": 5, "c": 1, "h": 3, "d": 2, "a": 4, "r": 0}
    return strength_order.get(piece.upper(), 0)

def push_piece(board, pusher_pos, pushed_pos, new_pos):
    """Empuja una pieza enemiga a una nueva posición."""
    # Obtener las piezas
    pusher = board[pusher_pos[0]][pusher_pos[1]]
    pushed = board[pushed_pos[0]][pushed_pos[1]]

    # Validar que ambas piezas existen
    if not pusher or not pushed:
        raise ValueError("Empuje inválido: falta una pieza.")

    # El empujador debe ser más fuerte que la pieza empujada
    if piece_weights[pusher] <= piece_weights[pushed]:
        raise ValueError("Empuje inválido: el empujador debe ser más fuerte que la pieza empujada.")

    # La nueva posición debe estar vacía
    if board[new_pos[0]][new_pos[1]] is not None:
        raise ValueError("Empuje inválido: la nueva posición debe estar vacía.")

    # Validar que las posiciones son adyacentes
    if abs(pusher_pos[0] - pushed_pos[0]) + abs(pusher_pos[1] - pushed_pos[1]) != 1:
        raise ValueError("Empuje inválido: el empujador no está adyacente a la pieza empujada.")
    if abs(pushed_pos[0] - new_pos[0]) + abs(pushed_pos[1] - new_pos[1]) != 1:
        raise ValueError("Empuje inválido: la nueva posición no está adyacente a la pieza empujada.")

    # Realizar el empuje
    board[pusher_pos[0]][pusher_pos[1]] = None  # El empujador deja su posición
    board[new_pos[0]][new_pos[1]] = pushed     # La pieza empujada se mueve
    board[pushed_pos[0]][pushed_pos[1]] = pusher  # El empujador toma el lugar de la pieza empujada

    return board

def pull_piece(board, puller_pos, pulled_pos, new_pos):
    """Jala una pieza enemiga hacia la posición anterior del jalador."""
    # Obtener las piezas
    puller = board[puller_pos[0]][puller_pos[1]]
    pulled = board[pulled_pos[0]][pulled_pos[1]]

    # Validar que ambas piezas existen
    if not puller or not pulled:
        raise ValueError("Jalada inválida: falta una pieza.")

    # El jalador debe ser más fuerte que la pieza jalada
    if piece_weights[puller] <= piece_weights[pulled]:
        raise ValueError("Jalada inválida: el jalador debe ser más fuerte que la pieza jalada.")

    # La nueva posición debe estar vacía
    if board[new_pos[0]][new_pos[1]] is not None:
        raise ValueError("Jalada inválida: la nueva posición debe estar vacía.")

    # Validar que las posiciones son adyacentes
    if abs(puller_pos[0] - pulled_pos[0]) + abs(puller_pos[1] - pulled_pos[1]) != 1:
        raise ValueError("Jalada inválida: el jalador no está adyacente a la pieza jalada.")
    if abs(puller_pos[0] - new_pos[0]) + abs(puller_pos[1] - new_pos[1]) != 1:
        raise ValueError("Jalada inválida: la nueva posición no está adyacente al jalador.")

    # Realizar la jalada
    board[puller_pos[0]][puller_pos[1]] = None  # El jalador deja su posición
    board[pulled_pos[0]][pulled_pos[1]] = None  # La pieza jalada deja su posición original
    board[new_pos[0]][new_pos[1]] = puller     # El jalador se mueve a la nueva posición
    board[puller_pos[0]][puller_pos[1]] = pulled  # La pieza jalada toma el lugar del jalador

    return board