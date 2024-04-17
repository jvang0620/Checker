import tkinter as tk

# Constants
EMPTY = 0
BLACK = 1
WHITE = 2
BOARD_SIZE = 8
SQUARE_SIZE = 50
PLAYER_COLOR = {BLACK: "black", WHITE: "white"}

class CheckerBoard(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = BLACK
        self.selected_piece = None
        self.setup_board()
        self.draw_board()

    def setup_board(self):
        for row in range(3):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    self.board[row][col] = WHITE
        for row in range(5, BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 1:
                    self.board[row][col] = BLACK

    def draw_board(self):
        self.delete("pieces")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = "brown" if (row + col) % 2 == 0 else "white"
                self.create_rectangle(
                    col * SQUARE_SIZE, row * SQUARE_SIZE,
                    (col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE,
                    fill=color, tags="board"
                )
                if self.board[row][col] != EMPTY:
                    player_color = PLAYER_COLOR[self.board[row][col]]
                    self.create_oval(
                        col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5,
                        (col + 1) * SQUARE_SIZE - 5, (row + 1) * SQUARE_SIZE - 5,
                        fill=player_color, tags=("pieces", "player")
                    )

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
        if self.current_player == WHITE and to_row <= from_row:
            return False
        if abs(from_row - to_row) == 1 and abs(from_col - to_col) == 1:
            return True
        if abs(from_row - to_row) == 2 and abs(from_col - to_col) == 2:
            mid_row, mid_col = (from_row + to_row) // 2, (from_col + to_col) // 2
            if self.board[mid_row][mid_col] != 3 - self.current_player:
                return False
            return True
        return False

    def on_click(self, event):
        row, col = self.get_piece_at_position(event.x, event.y)
        if self.board[row][col] != self.current_player:
            return
        self.selected_piece = (row, col)
        self.draw_board()

    def on_release(self, event):
        if self.selected_piece is None:
            return
        from_row, from_col = self.selected_piece
        to_row, to_col = self.get_piece_at_position(event.x, event.y)
        if (from_row, from_col) == (to_row, to_col):
            self.selected_piece = None
            return
        if self.is_valid_move(from_row, from_col, to_row, to_col):
            if abs(from_row - to_row) == 1:
                self.move_piece(from_row, from_col, to_row, to_col)
                self.selected_piece = None
                self.current_player = 3 - self.current_player
            elif abs(from_row - to_row) == 2:
                self.move_piece(from_row, from_col, to_row, to_col)
                self.capture_piece(from_row, from_col, to_row, to_col)
                self.selected_piece = (to_row, to_col)
                if any(self.is_valid_move(to_row, to_col, to_row + dr, to_col + dc) for dr in (-2, 2) for dc in (-2, 2)):
                    return  # Stay in the same player's turn if multiple jumps are possible
                self.current_player = 3 - self.current_player
        self.draw_board()

class CheckersApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Checkers")
        self.geometry(f"{BOARD_SIZE * SQUARE_SIZE}x{BOARD_SIZE * SQUARE_SIZE}")
        self.checker_board = CheckerBoard(self, width=BOARD_SIZE * SQUARE_SIZE, height=BOARD_SIZE * SQUARE_SIZE)
        self.checker_board.pack(fill=tk.BOTH, expand=True)
        self.checker_board.bind("<Button-1>", self.checker_board.on_click)
        self.checker_board.bind("<ButtonRelease-1>", self.checker_board.on_release)

if __name__ == "__main__":
    app = CheckersApp()
    app.mainloop()
