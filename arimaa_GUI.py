import tkinter as tk
from arimaa_game_logic import ArimaaGame

class ArimaaGUI:
    def __init__(self):
        self.game = ArimaaGame()
        self.selected_piece = None
        self.root = tk.Tk()
        self.root.title("Arimaa Game")

        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()
        self.update_pieces()

        # Añadir botón para finalizar el turno
        self.end_turn_button = tk.Button(self.root, text="End Turn", command=self.end_turn)
        self.end_turn_button.pack()

        self.root.mainloop()

    def draw_board(self):
        """Dibuja el tablero de 8x8 con las trampas."""
        trap_positions = [(2, 2), (2, 5), (5, 2), (5, 5)]
        for row in range(8):
            for col in range(8):
                if (row, col) in trap_positions:
                    color = "red"
                else:
                    color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(
                    col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill=color
                )

    def update_pieces(self):
        """Dibuja todas las piezas en el tablero."""
        self.canvas.delete("piece")
        board = self.game.get_board_state()
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    x = col * 50 + 25
                    y = row * 50 + 25
                    self.canvas.create_text(x, y, text=piece, font=("Arial", 24), tags="piece")

    def on_click(self, event):
        """Maneja los clics del usuario para seleccionar y mover piezas."""
        col = event.x // 50
        row = event.y // 50
        position = (row, col)

        if self.selected_piece:
            # Intentar mover la pieza seleccionada
            try:
                self.game.move_piece(self.selected_piece, position)
                self.selected_piece = None
                self.update_pieces()

                # Verificar si se alcanzaron los 4 pasos
                if self.game.steps_taken >= 4:
                    print("Se han completado los 4 pasos. Finaliza el turno.")
            except ValueError as e:
                print(e)
                self.selected_piece = None
        else:
            # Seleccionar la pieza
            piece = self.game.get_piece_at(position)
            if piece and (self.game.current_player == "gold" and piece.isupper() or 
                          self.game.current_player == "silver" and piece.islower()):
                self.selected_piece = position

    def end_turn(self):
        """Finaliza el turno del jugador actual."""
        if self.game.steps_taken < 4:
            print(f"Aún quedan {4 - self.game.steps_taken} pasos disponibles.")
        self.game.end_turn()
        self.update_pieces()

if __name__ == "__main__":
    ArimaaGUI()
