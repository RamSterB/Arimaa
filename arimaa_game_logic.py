class ArimaaGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = "gold"
        self.steps_taken = 0

    def initialize_board(self):
        """Inicializa el tablero con las piezas en sus posiciones iniciales."""
        board = [[None for _ in range(8)] for _ in range(8)]
        # Configuración inicial del oro
        board[1] = ["C", "D", "H", "A", "E", "H", "D", "C"]
        board[0] = ["R"] * 8
        # Configuración inicial de la plata
        board[7] = ["r"] * 8
        board[6] = ["c", "d", "h", "a", "e", "h", "d", "c"]
        return board

    def get_board_state(self):
        """Devuelve el estado actual del tablero."""
        return self.board

    def get_piece_at(self, position):
        """Devuelve la pieza en una posición específica."""
        row, col = position
        return self.board[row][col]

    def move_piece(self, start, end):
        """Mueve una pieza desde una posición inicial a una posición final."""
        start_row, start_col = start
        end_row, end_col = end
        piece = self.get_piece_at(start)

        if not piece:
            raise ValueError("No hay pieza en la posición inicial.")

        if self.board[end_row][end_col]:
            raise ValueError("La posición final ya está ocupada.")

        if abs(start_row - end_row) + abs(start_col - end_col) != 1:
            raise ValueError("Movimiento inválido: las piezas solo pueden moverse una casilla a la vez.")

        if self.steps_taken >= 4:
            raise ValueError("Se han tomado demasiados pasos en este turno.")

        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece
        self.steps_taken += 1
        

    def change_turn(self, trap_positions):
        """Cambia el turno al siguiente jugador."""
        self.current_player = "silver" if self.current_player == "gold" else "gold"
        self.steps_taken = 0

        # Validar estado del juego si es necesario
        self.check_trap_positions(trap_positions)
        self.check_victory_conditions()

    def check_trap_positions(self, trap_positions):
        """Verifica si alguna pieza debe ser eliminada por estar en una trampa sin apoyo."""
        for row, col in trap_positions:
            piece = self.get_piece_at((row, col))
            if piece and not self.has_support((row, col)):
                self.board[row][col] = None

    def has_support(self, position):
        """Verifica si una pieza en una posición tiene apoyo de aliados adyacentes."""
        row, col = position
        piece = self.get_piece_at(position)
        if not piece:
            return False

        allies = set("RCDHEP" if piece.isupper() else "rcdhep")
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj_row, adj_col = row + dr, col + dc
            if 0 <= adj_row < 8 and 0 <= adj_col < 8:
                adj_piece = self.get_piece_at((adj_row, adj_col))
                if adj_piece in allies:
                    return True
        return False

    def check_victory_conditions(self):
        """Verifica si se han cumplido las condiciones de victoria."""
        for col in range(8):
            if self.board[0][col] == "r":
                print("¡Plata gana!")
                self.end_game()
            if self.board[7][col] == "R":
                print("¡Oro gana!")
                self.end_game()

    def end_game(self):
        """Finaliza el juego."""
        print("Juego terminado.")
        raise SystemExit

# Ejemplo de uso:
if __name__ == "__main__":
    game = ArimaaGame()
    print("Estado inicial del tablero:")
    for row in game.get_board_state():
        print(row)
