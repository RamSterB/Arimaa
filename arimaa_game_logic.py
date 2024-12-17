from arimaa_ai import find_best_move
from arimaa_utils import is_frozen, pull_piece, push_piece
import pygame

class ArimaaGame:
    def __init__(self, gui=None):
        self.board = self.initialize_board()
        self.current_player = "white"
        self.steps_taken = 0
        self.gui = gui  # Referencia a la GUI
        self.piece_weights = {
            "E": 5,  # Elefante
            "A": 4,  # Camello
            "H": 3,  # Caballo
            "D": 2,  # Perro
            "C": 1,  # Gato
            "R": 0,  # Conejo
            "e": 5, "a": 4, "h": 3, "d": 2, "c": 1, "r": 0
        }
        self.trap_positions = [(2, 2), (2, 5), (5, 2), (5, 5)]

    def initialize_board(self):
        """Inicializa el tablero con las piezas en sus posiciones iniciales."""
        board = [[None for _ in range(8)] for _ in range(8)]
        # Configuración inicial del Black
        board[1] = ["C", "D", "H", "A", "E", "H", "D", "C"]
        board[0] = ["R"] * 8
        # Configuración inicial de la White
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
        
        # Verificar que la pieza no se mueva a una trampa
        if self.check_trap_positions(self.trap_positions) and self.current_player == "white":
            raise ValueError("La pieza ha caído en una trampa sin apoyo.")

        # Si todas las validaciones pasan, realizamos el movimiento
        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece
        self.steps_taken += 1
        print(f"{piece} movido de {start} a {end}")

    def make_best_move(self):
        """Realiza el mejor movimiento usando el algoritmo minimax."""
        for _ in range(4 - self.steps_taken):
            best_move = find_best_move(self.board, self.current_player)
            if best_move:
                if len(best_move) == 2:
                    # Movimiento simple
                    start, end = best_move
                    if start != end:
                        self.move_piece(start, end)
                        self.check_trap_positions(self.trap_positions)
                        print(f"IA realizó el movimiento de {start} a {end}")
                        # Actualiza el tablero
                        if self.gui:
                            self.gui.draw_board()
                            self.gui.draw_pieces()
                            pygame.display.flip()
                elif len(best_move) == 4:
                    # Movimiento de empuje/jalón
                    move_type, origin, affected, destination = best_move
                    if move_type == "push":
                        self.push_piece(origin, affected, destination)
                        print(f"IA realizó empuje desde {origin} a {destination}")
                        # Actualiza el tablero
                        if self.gui:
                            self.gui.draw_board()
                            self.gui.draw_pieces()
                            pygame.display.flip()
                    elif move_type == "pull":
                        self.pull_piece(origin, affected, destination)
                        print(f"IA realizó jalón desde {origin} a {destination}")
                        # Actualiza el tablero
                        if self.gui:
                            self.gui.draw_board()
                            self.gui.draw_pieces()
                            pygame.display.flip()
                else:
                    print("El mejor movimiento encontrado no es válido.")
            else:
                print("No hay movimientos disponibles para la IA.")
        
    def is_frozen(self, position):
        return is_frozen(self.board, position)

    def check_trap_positions(self, trap_positions):
        """Verifica si alguna pieza debe ser eliminada por estar en una trampa sin apoyo."""
        for row, col in trap_positions:
            piece = self.get_piece_at((row, col))
            if piece and not self.has_support((row, col)):
                self.board[row][col] = None
                return True
        return False

    def has_support(self, position):
        """Verifica si una pieza en una posición tiene apoyo de aliados adyacentes."""
        row, col = position
        piece = self.get_piece_at(position)
        if not piece:
            return False

        allies = set("RCDHEA" if piece.isupper() else "rcdhea")
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
        
        new_board = push_piece(self.board, pusher_pos, pushed_pos, new_pos)
        self.board = new_board
        self.steps_taken += 2

    def pull_piece(self, puller_pos, pulled_pos, new_pos):
        """Jala una pieza enemiga hacia la posición anterior del jalador."""
        if self.steps_taken + 2 > 4:
            raise ValueError("Jalada inválida: no se pueden tomar más de 4 pasos en un turno.")
        
        new_board = pull_piece(self.board, puller_pos, pulled_pos, new_pos)
        self.board = new_board
        self.steps_taken += 2

    def check_victory_conditions(self):
        """Verifica si se han cumplido las condiciones de victoria."""
        black_rabbits = 0
        white_rabbits = 0
        black_has_moves = False
        white_has_moves = False

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if not piece:
                    continue

                # Verificar conejos en el extremo del tablero
                if piece == "R":
                    black_rabbits += 1
                    if row == 7:
                        print("¡Black win!")
                        self.end_game()
                elif piece == "r":
                    white_rabbits += 1
                    if row == 0:
                        print("¡White win!")
                        self.end_game()

                # Verificar si la pieza puede moverse (no está congelada)
                if not self.is_frozen((row, col)):
                    is_black = piece.isupper()
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < 8 and 0 <= new_col < 8 and self.board[new_row][new_col] is None:
                            if is_black:
                                black_has_moves = True
                            else:
                                white_has_moves = True

        # Condición de victoria por eliminación de conejos
        if black_rabbits == 0:
            print("¡White gana! (Black sin conejos)")
            self.end_game()
        if white_rabbits == 0:
            print("¡Black gana! (White sin conejos)")
            self.end_game()

        # Condición de victoria por inmovilidad
        if not black_has_moves:
            print("¡White gana! (Black inmovilizado)")
            self.end_game()
        if not white_has_moves:
            print("¡Black gana! (White inmovilizada)")
            self.end_game()      
    
    def change_turn(self, trap_positions):
        """Cambia el turno y activa la IA para whites."""
        self.current_player = "black" if self.current_player == "white" else "white"
        self.steps_taken = 0
        
        # Validar estado
        self.check_victory_conditions()

        # Activar IA para whites
        if self.current_player == "black":
            try:
                self.make_best_move() # IA
                self.current_player = "white"
                self.steps_taken = 0
            except Exception as e:
                 print(f"Error en movimiento de IA: {e}")
                 if e.args[0] == "Se han tomado demasiados pasos en este turno." or e.args[0] == "Jalada inválida: no se pueden tomar más de 4 pasos en un turno." or e.args[0] == "Empuje inválido: no se pueden tomar más de 4 pasos en un turno.":
                     self.change_turn(trap_positions)
                     print("Se cambió el turno debido a un error en la IA.")

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