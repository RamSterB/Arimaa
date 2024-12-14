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
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))  # Espacio extra para el label
        pygame.display.set_caption("Arimaa Game")
        self.font = pygame.font.SysFont(None, 30)
        self.selected_piece = None
        self.dragging_piece = False
        self.dragging_path = []
        self.running = True
        self.moves_made = 0
        # Añadir botones
        self.pass_turn_button = pygame.Rect(WINDOW_SIZE - 150, WINDOW_SIZE + 10, 140, 40)
        self.push_button = pygame.Rect(10, WINDOW_SIZE + 10, 140, 40)
        self.pull_button = pygame.Rect(160, WINDOW_SIZE + 10, 140, 40)
        self.action_mode = None  # 'push', 'pull', o None para movimientos normales

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

        # Dibuja los botones y el turno actual
        self.draw_buttons()
        self.draw_turn_info()

    def draw_buttons(self):
        """Dibuja los botones de control."""
        pygame.draw.rect(self.screen, (0, 255, 0), self.pass_turn_button)  # Botón de pasar turno
        pygame.draw.rect(self.screen, (0, 200, 200), self.push_button)  # Botón de empujar
        pygame.draw.rect(self.screen, (200, 200, 0), self.pull_button)  # Botón de jalar

        # Añadir texto a los botones
        self.screen.blit(self.font.render("Pasar Turno", True, BLACK), (self.pass_turn_button.x + 10, self.pass_turn_button.y + 10))
        self.screen.blit(self.font.render("Empujar", True, BLACK), (self.push_button.x + 10, self.push_button.y + 10))
        self.screen.blit(self.font.render("Jalar", True, BLACK), (self.pull_button.x + 10, self.pull_button.y + 10))

    def draw_turn_info(self):
        """Dibuja la información del turno actual y movimientos restantes."""
        current_turn = "Oro" if self.game.current_player == "gold" else "Plata"
        moves_left = 4 - self.game.steps_taken
        info_text = f"Turno: {current_turn} | Movimientos restantes: {moves_left}"
        label = self.font.render(info_text, True, WHITE)
        self.screen.blit(label, (10, WINDOW_SIZE + 60))

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
                if self.pass_turn_button.collidepoint(event.pos):
                    self.pass_turn()
                elif self.push_button.collidepoint(event.pos):
                    self.action_mode = 'push'
                    self.dragging_path = []  # Limpiar cualquier selección anterior
                    print("Modo: Empujar activado")
                elif self.pull_button.collidepoint(event.pos):
                    self.action_mode = 'pull'
                    self.dragging_path = []  # Limpiar cualquier selección anterior
                    print("Modo: Jalar activado")
                else:
                    position = self.get_clicked_position(event.pos)
                    self.handle_mouse_down(position)
            elif event.type == pygame.MOUSEBUTTONUP:
                position = self.get_clicked_position(event.pos)
                self.handle_mouse_up(position)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event.pos)

    def pass_turn(self):
        """Maneja la acción de pasar el turno."""
        print("Pasando el turno...")
        self.game.change_turn(TRAP_POSITIONS)
        self.moves_made = 0  # Restablecer los pasos

    def handle_mouse_down(self, position):
        """Maneja el inicio del arrastre."""
        piece = self.game.get_piece_at(position)
        if piece and (self.game.current_player == "gold" and piece.isupper() or 
                      self.game.current_player == "silver" and piece.islower()):
            self.selected_piece = position
            self.dragging_piece = True
            self.dragging_path = [position]

    def handle_mouse_up(self, position):
        """Maneja el fin del arrastre y acciones especiales."""
        if self.dragging_piece:
            # Añadir la posición seleccionada
            if position not in self.dragging_path:
                self.dragging_path.append(position)

            # Verificar la cantidad de posiciones seleccionadas
            try:
                if self.action_mode == 'push' and len(self.dragging_path) == 3:
                    self.handle_push_action()
                elif self.action_mode == 'pull' and len(self.dragging_path) == 3:
                    self.handle_pull_action()
                elif self.action_mode is None:
                    self.handle_normal_move()
                elif len(self.dragging_path) < 2:
                    print(f"Selecciona más posiciones: {len(self.dragging_path)}/3 seleccionadas.")
                else:
                    print(f"{self.action_mode.capitalize()} inválido: seleccione correctamente las posiciones.")
            except ValueError as e:
                print(f"Error: {e}")

            # Resetear después de realizar una acción
            if len(self.dragging_path) >= 3 or self.action_mode is None:
                self.dragging_piece = False
                self.dragging_path = []
                self.action_mode = None

    def handle_push_action(self):
        """Maneja la acción de empujar."""
        if len(self.dragging_path) == 3:
            pusher_pos, pushed_pos, new_pos = self.dragging_path
            try:
                self.game.push_piece(pusher_pos, pushed_pos, new_pos)
                self.moves_made += 2
                print(f"Empuje exitoso: {pusher_pos} empujó {pushed_pos} a {new_pos}")
                # Cambiar de turno si los pasos se agotan
                if self.game.steps_taken >= 4:
                    print("Pasos agotados, cambiando turno.")
                    self.pass_turn()
            except ValueError as e:
                print(f"Error al empujar: {e}")
        else:
            print(f"Empuje inválido: seleccione exactamente 3 posiciones. Actualmente: {len(self.dragging_path)}")

    def handle_pull_action(self):
        """Maneja la acción de jalar."""
        if len(self.dragging_path) == 3:
            puller_pos, pulled_pos, new_pos = self.dragging_path
            try:
                self.game.pull_piece(puller_pos, pulled_pos, new_pos)
                self.moves_made += 2
                print(f"Jalada exitosa: {puller_pos} jaló {pulled_pos} a {new_pos}")
                # Cambiar de turno si los pasos se agotan
                if self.game.steps_taken >= 4:
                    print("Pasos agotados, cambiando turno.")
                    self.pass_turn()
            except ValueError as e:
                print(f"Error al jalar: {e}")
        else:
            print(f"Jalada inválida: seleccione exactamente 3 posiciones. Actualmente: {len(self.dragging_path)}")
        """Maneja la acción de jalar."""
        if len(self.dragging_path) == 3:
            puller_pos, pulled_pos, new_pos = self.dragging_path
            try:
                self.game.pull_piece(puller_pos, pulled_pos, new_pos)
                self.moves_made += 2
                print(f"Jalada exitosa: {puller_pos} jaló {pulled_pos} a {new_pos}")
            except ValueError as e:
                print(f"Error al jalar: {e}")
        else:
            print(f"Jalada inválida: seleccione exactamente 3 posiciones. Actualmente: {len(self.dragging_path)}")

    def handle_mouse_motion(self, pos):
        """Maneja el movimiento mientras se arrastra."""
        if self.dragging_piece:
            current_position = self.get_clicked_position(pos)
            if current_position not in self.dragging_path:  # Evitar duplicados
                self.dragging_path.append(current_position)

    def handle_normal_move(self):
        """Maneja un movimiento normal."""
        for i in range(1, len(self.dragging_path)):
            self.game.move_piece(self.dragging_path[i - 1], self.dragging_path[i])
            self.moves_made += 1
            if self.game.steps_taken >= 4:
                self.moves_made = 0
                self.game.change_turn(TRAP_POSITIONS)

if __name__ == "__main__":
    gui = ArimaaPygame()
    gui.run()
    pygame.quit()
