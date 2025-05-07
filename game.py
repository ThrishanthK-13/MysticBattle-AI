import random

ELEMENTS = ["Fire", "Water", "Earth", "Air"]
INTERACTIONS = {
    ("Fire", "Water"): -1, ("Water", "Fire"): 1,
    ("Water", "Earth"): -1, ("Earth", "Water"): 1,
    ("Earth", "Air"): -1, ("Air", "Earth"): 1,
    ("Air", "Fire"): -1, ("Fire", "Air"): 1
}

class MysticBattle:
    def __init__(self, size=3):  # ✅ fixed constructor
        self.board = [[None] * size for _ in range(size)]

    def display_board(self):
        print("\n".join([" ".join(elem or "-" for elem in row) for row in self.board]) + "\n")

    def make_move(self, row, col, element):
        if 0 <= row < len(self.board) and 0 <= col < len(self.board) and self.board[row][col] is None:
            self.board[row][col] = element
            return True
        return False

    def evaluate_board(self):
        score = 0
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                if self.board[r][c]:
                    for dr, dc in [(0, 1), (1, 0)]:  # ✅ avoid double-counting
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < len(self.board) and 0 <= nc < len(self.board) and self.board[nr][nc]:
                            score += INTERACTIONS.get((self.board[r][c], self.board[nr][nc]), 0)
        return score

    def minimax(self, depth, is_max):
        if depth == 0:
            return self.evaluate_board(), None

        moves = [(r, c, e) for r in range(len(self.board)) for c in range(len(self.board)) 
                 if self.board[r][c] is None for e in ELEMENTS]

        if not moves:
            return self.evaluate_board(), None

        best_score = float('-inf') if is_max else float('inf')
        best_move = None

        for r, c, e in moves:
            self.board[r][c] = e
            score, _ = self.minimax(depth - 1, not is_max)
            self.board[r][c] = None  # Undo move

            if is_max and score > best_score:
                best_score, best_move = score, (r, c, e)
            elif not is_max and score < best_score:
                best_score, best_move = score, (r, c, e)

        return best_score, best_move

    def get_ai_move(self):
        _, move = self.minimax(2, True)
        return move

# Start the game
game = MysticBattle()

while True:
    game.display_board()
    try:
        user_row, user_col = map(int, input("Enter move (row col): ").split())
        user_element = input(f"Choose element {ELEMENTS}: ")

        if user_element not in ELEMENTS or not game.make_move(user_row, user_col, user_element):
            print("Invalid move! Try again.")
            continue

        game.display_board()
        print("AI thinking...")
        ai_move = game.get_ai_move()
        if ai_move:
            game.make_move(*ai_move)
            print(f"AI plays {ai_move[2]} at ({ai_move[0]}, {ai_move[1]})")

        if all(all(cell is not None for cell in row) for row in game.board):
            print("Game over! Final score:", game.evaluate_board())
            break

    except ValueError:
        print("Invalid input! Please enter valid numbers.")
