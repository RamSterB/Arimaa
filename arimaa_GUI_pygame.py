import pygame
from arimaa_game_logic import ArimaaGame

# Dimensiones de la ventana
WINDOW_SIZE = 800
CELL_SIZE = WINDOW_SIZE // 8

# Colores
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

# Posiciones de las trampas
TRAP_POSITIONS = [(2, 2), (2, 5), (5, 2), (5, 5)]

class ArimaaPygame:
    def __init__(self):
        pygame.init()
        self.game = ArimaaGame()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Arimaa Game")
        self.selected_piece = None
        self.dragging_piece = False
        self.dragging_path = []
        self.running = True
        self.moves_made = 0

    def draw_board(self):
        """Dibuja el tablero de juego."""
        for row in range(8):
            for col in range(8):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if (row, col) in TRAP_POSITIONS:
                    color = RED
                else:
                    color = WHITE if (row + col) % 2 == 0 else GRAY
                pygame.draw.rect(self.screen, color, rect)

    def draw_pieces(self):
        """Dibuja las piezas en el tablero."""
        board = self.game.get_board_state()
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    center_x = col * CELL_SIZE + CELL_SIZE // 2
                    center_y = row * CELL_SIZE + CELL_SIZE // 2
                    color = GOLD if piece.isupper() else SILVER
                    pygame.draw.circle(self.screen, color, (center_x, center_y), CELL_SIZE // 3)
                    text = pygame.font.SysFont(None, 40).render(piece, True, BLACK)
                    text_rect = text.get_rect(center=(center_x, center_y))
                    self.screen.blit(text, text_rect)

    def get_clicked_position(self, pos):
        """Devuelve la posición de la celda clicada."""
        x, y = pos
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        return row, col

    def run(self):
        """Bucle principal del juego."""
        while self.running:
            self.handle_events()
            self.screen.fill(BLACK)
            self.draw_board()
            self.draw_pieces()
            pygame.display.flip()

    def handle_events(self):
        """Maneja los eventos de entrada del usuario."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = self.get_clicked_position(event.pos)
                self.handle_mouse_down(position)
            elif event.type == pygame.MOUSEBUTTONUP:
                position = self.get_clicked_position(event.pos)
                self.handle_mouse_up(position)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event.pos)

    def handle_mouse_down(self, position):
        """Maneja el inicio del arrastre."""
        piece = self.game.get_piece_at(position)
        if piece and (self.game.current_player == "gold" and piece.isupper() or 
                      self.game.current_player == "silver" and piece.islower()):
            self.selected_piece = position
            self.dragging_piece = True
            self.dragging_path = [position]

    def handle_mouse_up(self, position):
        """Maneja el fin del arrastre."""
        if self.dragging_piece:
            self.dragging_path.append(position)
            try:
                for i in range(1, 5):
                    self.game.move_piece(self.dragging_path[i - 1], self.dragging_path[i])
                    self.moves_made += 1
                    if self.game.steps_taken >= 4:
                        self.moves_made = 0
                        self.game.change_turn(TRAP_POSITIONS)
                self.selected_piece = None
                
                
                
            except ValueError as e:
                print(e)
            self.dragging_piece = False
            self.dragging_path = []
        


    def handle_mouse_motion(self, pos):
        """Maneja el movimiento mientras se arrastra."""
        if self.dragging_piece:
            current_position = self.get_clicked_position(pos)
            if current_position != self.dragging_path[-1]:
                self.dragging_path.append(current_position)

if __name__ == "__main__":
    gui = ArimaaPygame()
    gui.run()
    pygame.quit()
