from arimaa_ai import find_best_move

class ArimaaGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = "gold"
        self.steps_taken = 0
        self.piece_weights = {
            "E": 5,  # Elefante
            "C": 4,  # Camello
            "H": 3,  # Caballo
            "D": 2,  # Perro
            "A": 1,  # Gato
            "R": 0,  # Conejo
            "e": 5, "c": 4, "h": 3, "d": 2, "a": 1, "r": 0
        }

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
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def move_piece(self, start, end):
        """Mueve una pieza desde una posición inicial a una posición final."""
        start_row, start_col = start
        end_row, end_col = end
        piece = self.get_piece_at(start)

        # Comprobamos que la pieza existe en la posición de inicio
        if not piece:
            raise ValueError("No hay pieza en la posición inicial.")

        # Verificar si la pieza está congelada
        if self.is_frozen(start):
            raise ValueError("La pieza está congelada y no puede moverse.")

        # Verificamos si la posición final está ocupada
        if self.board[end_row][end_col]:
            raise ValueError("La posición final ya está ocupada.")

        # Verificamos que la pieza se mueva solo a una casilla adyacente
        if abs(start_row - end_row) + abs(start_col - end_col) != 1:
            raise ValueError("Movimiento inválido: las piezas solo pueden moverse una casilla a la vez.")

        # Prohibir que los conejos se muevan hacia atrás
        if piece.lower() == "r" and (
            (piece.isupper() and end_row < start_row) or (piece.islower() and end_row > start_row)
        ):
            raise ValueError("Los conejos no pueden moverse hacia atrás.")

        # Asegurarse de que no se realicen más de 4 movimientos en un turno
        if self.steps_taken >= 4:
            raise ValueError("Se han tomado demasiados pasos en este turno.")

        # Si todas las validaciones pasan, realizamos el movimiento
        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece
        self.steps_taken += 1
        print(f"{piece} movido de {start} a {end}")

    def make_best_move(self):
        """Realiza el mejor movimiento usando el algoritmo minimax."""
        for _ in range(4 - self.steps_taken):
            best_move = find_best_move(self.board)
            if best_move:
                start, end = best_move
                if start != end:  # Validar que el movimiento no deje la pieza en la misma posición
                    self.move_piece(start, end)
                    print(f"IA realizó el movimiento de {start} a {end}")
                else:
                    print("El mejor movimiento encontrado deja la pieza en la misma posición, buscando otro movimiento.")
            else:
                print("No hay movimientos disponibles para la IA.")
    
    def is_frozen(self, position):
        """Determina si una pieza en una posición está congelada."""
        row, col = position
        piece = self.get_piece_at(position)
        if not piece:
            return False  # Una posición vacía no puede estar congelada

        # Determinar equipo de la pieza
        allies = set("RCDHEP" if piece.isupper() else "rcdhep")
        enemies = set("rcdhep" if piece.isupper() else "RCDHEP")

        # Verificar piezas adyacentes
        has_ally = False
        is_overpowered = False
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj_row, adj_col = row + dr, col + dc
            if 0 <= adj_row < 8 and 0 <= adj_col < 8:
                adj_piece = self.get_piece_at((adj_row, adj_col))
                if adj_piece in allies:
                    has_ally = True
                elif adj_piece in enemies:
                    if self.piece_weights[adj_piece] > self.piece_weights[piece]:
                        is_overpowered = True

        # Una pieza está congelada si está sobrepasada por el enemigo y no tiene aliados
        return is_overpowered and not has_ally

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
    
    def push_piece(self, pusher_pos, pushed_pos, new_pos):
        """Empuja una pieza enemiga a una nueva posición."""
        if self.steps_taken + 2 > 4:
            raise ValueError("Empuje inválido: no se pueden tomar más de 4 pasos en un turno.")
        
        pusher = self.get_piece_at(pusher_pos)
        pushed = self.get_piece_at(pushed_pos)

        # Validar que ambas piezas existen
        if not pusher or not pushed:
            raise ValueError("Empuje inválido: falta una pieza.")

        # El empujador debe ser más fuerte que la pieza empujada
        if self.piece_weights[pusher] <= self.piece_weights[pushed]:
            raise ValueError("Empuje inválido: el empujador debe ser más fuerte que la pieza empujada.")

        # La nueva posición debe estar vacía
        if self.board[new_pos[0]][new_pos[1]] is not None:
            raise ValueError("Empuje inválido: la nueva posición debe estar vacía.")

        # Validar que las posiciones son adyacentes
        if abs(pusher_pos[0] - pushed_pos[0]) + abs(pusher_pos[1] - pushed_pos[1]) != 1:
            raise ValueError("Empuje inválido: el empujador no está adyacente a la pieza empujada.")
        if abs(pushed_pos[0] - new_pos[0]) + abs(pushed_pos[1] - new_pos[1]) != 1:
            raise ValueError("Empuje inválido: la nueva posición no está adyacente a la pieza empujada.")
            
        
        # Realizar el empuje
        self.board[pusher_pos[0]][pusher_pos[1]] = None  # El empujador deja su posición
        self.board[new_pos[0]][new_pos[1]] = pushed     # La pieza empujada se mueve
        self.board[pushed_pos[0]][pushed_pos[1]] = pusher  # El empujador toma el lugar de la pieza empujada
        self.steps_taken += 2


    def pull_piece(self, puller_pos, pulled_pos, new_pos):
        """Jala una pieza enemiga hacia la posición anterior del jalador."""
        
        if self.steps_taken + 2 > 4:
            raise ValueError("Empuje inválido: no se pueden tomar más de 4 pasos en un turno.")
        
        puller = self.get_piece_at(puller_pos)
        pulled = self.get_piece_at(pulled_pos)

        # Validar que ambas piezas existen
        if not puller or not pulled:
            raise ValueError("Jalada inválida: falta una pieza.")

        # El jalador debe ser más fuerte que la pieza jalada
        if self.piece_weights[puller] <= self.piece_weights[pulled]:
            raise ValueError("Jalada inválida: el jalador debe ser más fuerte que la pieza jalada.")

        # La nueva posición debe estar vacía
        if self.board[new_pos[0]][new_pos[1]] is not None:
            raise ValueError("Jalada inválida: la nueva posición debe estar vacía.")

        # Validar que las posiciones son adyacentes
        if abs(puller_pos[0] - pulled_pos[0]) + abs(puller_pos[1] - pulled_pos[1]) != 1:
            raise ValueError("Jalada inválida: el jalador no está adyacente a la pieza jalada.")
        if abs(puller_pos[0] - new_pos[0]) + abs(puller_pos[1] - new_pos[1]) != 1:
            raise ValueError("Jalada inválida: la nueva posición no está adyacente al jalador.")

        # Realizar la jalada
        self.board[puller_pos[0]][puller_pos[1]] = None  # El jalador deja su posición
        self.board[pulled_pos[0]][pulled_pos[1]] = None  # La pieza jalada deja su posición original
        self.board[new_pos[0]][new_pos[1]] = puller     # El jalador se mueve a la nueva posición
        self.board[puller_pos[0]][puller_pos[1]] = pulled  # La pieza jalada toma el lugar del jalador
        self.steps_taken += 2



    def check_victory_conditions(self):
        """Verifica si se han cumplido las condiciones de victoria."""
        gold_rabbits = 0
        silver_rabbits = 0
        gold_has_moves = False
        silver_has_moves = False

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if not piece:
                    continue

                # Verificar conejos en el extremo del tablero
                if piece == "R":
                    gold_rabbits += 1
                    if row == 7:
                        print("¡Oro gana!")
                        self.end_game()
                elif piece == "r":
                    silver_rabbits += 1
                    if row == 0:
                        print("¡Plata gana!")
                        self.end_game()

                # Verificar si la pieza puede moverse (no está congelada)
                if not self.is_frozen((row, col)):
                    is_gold = piece.isupper()
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < 8 and 0 <= new_col < 8 and self.board[new_row][new_col] is None:
                            if is_gold:
                                gold_has_moves = True
                            else:
                                silver_has_moves = True

        # Condición de victoria por eliminación de conejos
        if gold_rabbits == 0:
            print("¡Plata gana! (Oro sin conejos)")
            self.end_game()
        if silver_rabbits == 0:
            print("¡Oro gana! (Plata sin conejos)")
            self.end_game()

        # Condición de victoria por inmovilidad
        if not gold_has_moves:
            print("¡Plata gana! (Oro inmovilizado)")
            self.end_game()
        if not silver_has_moves:
            print("¡Oro gana! (Plata inmovilizada)")
            self.end_game()      
    
    def change_turn(self, trap_positions):
        """Cambia el turno y activa la IA para silver."""
        self.current_player = "silver" if self.current_player == "gold" else "gold"
        self.steps_taken = 0
        
        # Validar estado
        self.check_trap_positions(trap_positions)
        self.check_victory_conditions()

        # Activar IA para silver
        if self.current_player == "silver":
            try:
                self.make_best_move()
                self.current_player = "gold"
                self.steps_taken = 0
            except Exception as e:
                print(f"Error en movimiento de IA: {e}")

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
    game.make_best_move() # Este método no existe en la clase ArimaaGame