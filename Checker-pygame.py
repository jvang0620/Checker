import pygame
import sys

# Constants
EMPTY = 0
BLACK = 1
Red = 2
BOARD_SIZE = 8
SQUARE_SIZE = 50
PLAYER_COLOR = {BLACK: (0, 0, 0), Red: (200, 0, 0)}

class CheckerBoard:
    def __init__(self):
        self.board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = BLACK
        self.selected_piece = None
        self.setup_board()

    def setup_board(self):
        for row in range(3):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Red
        for row in range(5, BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    self.board[row][col] = BLACK

    def draw_board(self, screen):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = (139, 69, 19) if (row + col) % 2 == 0 else (245, 222, 179)
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if self.board[row][col] != EMPTY:
                    player_color = PLAYER_COLOR[self.board[row][col]]
                    pygame.draw.circle(screen, player_color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

    def get_piece_at_position(self, x, y):
        col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
        return row, col

    def move_piece(self, from_row, from_col, to_row, to_col):
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = EMPTY

    def capture_piece(self, from_row, from_col, to_row, to_col):
        mid_row, mid_col = (from_row + to_row) // 2, (from_col + to_col) // 2
        self.board[mid_row][mid_col] = EMPTY

    def is_valid_move(self, from_row, from_col, to_row, to_col):
        if to_row < 0 or to_row >= BOARD_SIZE or to_col < 0 or to_col >= BOARD_SIZE:
            return False
        if self.board[to_row][to_col] != EMPTY:
            return False
        if self.current_player == BLACK and to_row >= from_row:
            return False
        if self.current_player == Red and to_row <= from_row:
            return False
        if abs(from_row - to_row) == 1 and abs(from_col - to_col) == 1:
            return True
        if abs(from_row - to_row) == 2 and abs(from_col - to_col) == 2:
            mid_row, mid_col = (from_row + to_row) // 2, (from_col + to_col) // 2
            if self.board[mid_row][mid_col] != 3 - self.current_player:
                return False
            return True
        return False

    def switch_player(self):
        self.current_player = 3 - self.current_player

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            row, col = self.get_piece_at_position(*event.pos)
            if self.board[row][col] == self.current_player:
                self.selected_piece = (row, col)
        elif event.type == pygame.MOUSEBUTTONUP and self.selected_piece:
            from_row, from_col = self.selected_piece
            to_row, to_col = self.get_piece_at_position(*event.pos)
            if (from_row, from_col) == (to_row, to_col):
                self.selected_piece = None
                return
            if self.is_valid_move(from_row, from_col, to_row, to_col):
                if abs(from_row - to_row) == 1:
                    self.move_piece(from_row, from_col, to_row, to_col)
                    self.selected_piece = None
                    self.switch_player()
                elif abs(from_row - to_row) == 2:
                    self.move_piece(from_row, from_col, to_row, to_col)
                    self.capture_piece(from_row, from_col, to_row, to_col)
                    self.selected_piece = (to_row, to_col)
                    if any(self.is_valid_move(to_row, to_col, to_row + dr, to_col + dc) for dr in (-2, 2) for dc in (-2, 2)):
                        return
                    self.switch_player()
            self.selected_piece = None

def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE))
    pygame.display.set_caption("Checkers")
    clock = pygame.time.Clock()
    checker_board = CheckerBoard()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            checker_board.handle_event(event)

        screen.fill((0, 0, 0))
        checker_board.draw_board(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
