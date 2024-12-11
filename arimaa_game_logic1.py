class ArimaaGame:
    def __init__(self):
        # Inicializar el estado del tablero
        self.board = self.initialize_board()
        self.current_player = "gold"  # El jugador dorado comienza
        self.steps_taken = 0

    def initialize_board(self):
        """Crea la disposición inicial del tablero."""
        board = [[None for _ in range(8)] for _ in range(8)]

        # Configuración inicial del jugador dorado
        gold_positions = {
            (0, 0): "R", (0, 1): "R", (0, 2): "R", (0, 3): "R",
            (0, 4): "R", (0, 5): "R", (0, 6): "R", (0, 7): "R",
            (1, 0): "C", (1, 1): "D", (1, 2): "H", (1, 3): "E",
            (1, 4): "E", (1, 5): "H", (1, 6): "D", (1, 7): "C",
        }

        # Configuración inicial del jugador plateado
        silver_positions = {
            (7, 0): "r", (7, 1): "r", (7, 2): "r", (7, 3): "r",
            (7, 4): "r", (7, 5): "r", (7, 6): "r", (7, 7): "r",
            (6, 0): "c", (6, 1): "d", (6, 2): "h", (6, 3): "e",
            (6, 4): "e", (6, 5): "h", (6, 6): "d", (6, 7): "c",
        }

        # Colocar las piezas en el tablero
        for (row, col), piece in gold_positions.items():
            board[row][col] = piece
        for (row, col), piece in silver_positions.items():
            board[row][col] = piece

        return board

    def move_piece(self, start_pos, end_pos):
        """Mueve una pieza de una posición a otra si el movimiento es válido."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        piece = self.board[start_row][start_col]
        
        if not piece:
            raise ValueError("No hay pieza en la posición inicial.")
        if self.board[end_row][end_col] is not None:
            raise ValueError("La posición final ya está ocupada.")

        if self.steps_taken >= 4:
            raise ValueError("No puedes mover más piezas en este turno.")

        # Validar movimientos básicos (adyacencia)
        if abs(start_row - end_row) + abs(start_col - end_col) != 1:
            raise ValueError("Movimiento no válido: solo movimientos adyacentes están permitidos.")

        # Mover la pieza
        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece

        # Incrementar el contador de pasos
        self.steps_taken += 1

        # Cambiar turno
        # self.current_player = "silver" if self.current_player == "gold" else "gold"

    def get_board_state(self):
        """Devuelve el estado actual del tablero."""
        return self.board

    def get_piece_at(self, position):
        """Devuelve la pieza en una posición específica del tablero."""
        row, col = position
        return self.board[row][col]

    def is_valid_move(self, start_pos, end_pos):
        """Valida si un movimiento es permitido sin ejecutarlo."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if not (0 <= start_row < 8 and 0 <= start_col < 8):
            return False
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        piece = self.board[start_row][start_col]
        if not piece:
            return False

        # Validar que la posición final esté vacía
        if self.board[end_row][end_col] is not None:
            return False

        # Validar que sea un movimiento adyacente
        if abs(start_row - end_row) + abs(start_col - end_col) != 1:
            return False

        return True
    
    def end_turn(self):
        """Finaliza el turno del jugador actual y resetea el contador de pasos."""
        self.steps_taken = 0
        self.current_player = "silver" if self.current_player == "gold" else "gold"