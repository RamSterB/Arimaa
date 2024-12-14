class ArimaaAI:
    def __init__(self, piece_weights):
        self.piece_weights = piece_weights

    def evaluate_board(self, board):
        value = 0
        for row in board:
            for piece in row:
                if piece:
                    value += self.piece_weights[piece] if piece.islower() else -self.piece_weights[piece]
        return value

    def generate_moves(self, board, player):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and ((player == "white" and piece.islower()) or (player == "black" and piece.isupper())):
                    for dr, dc in directions:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] is None:
                            moves.append(((row, col), (new_row, new_col)))
        return moves

    def minimax(self, board, depth, is_maximizing_player, alpha=float('-inf'), beta=float('inf')):
        if depth == 0:
            return self.evaluate_board(board)
        
        moves = self.generate_moves(board, "black" if is_maximizing_player else "white")
        if not moves:
            return self.evaluate_board(board)
        
        if is_maximizing_player:
            max_eval = float('-inf')
            for move in moves:
                new_board = [row[:] for row in board]
                start, end = move
                new_board[end[0]][end[1]] = new_board[start[0]][start[1]]
                new_board[start[0]][start[1]] = None
                eval = self.minimax(new_board, depth - 1, False, alpha, beta)
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
                eval = self.minimax(new_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move(self, board):
        """Encuentra el mejor movimiento usando minimax."""
        best_move = None
        best_value = float('-inf')
        moves = self.generate_moves(board, "black")
        
        if not moves:
            return None
            
        for move in moves:
            new_board = [row[:] for row in board]
            start, end = move
            new_board[end[0]][end[1]] = new_board[start[0]][start[1]]
            new_board[start[0]][start[1]] = None
            move_value = self.minimax(new_board, 2, False)
            if move_value > best_value:
                best_value = move_value
                best_move = move
        return best_move