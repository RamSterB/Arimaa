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