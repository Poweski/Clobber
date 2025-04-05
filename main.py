import sys
import copy

DIRECTIONS = [(-1, -1), (1, 1), (1, -1), (-1, 1)]

def read_board():
    lines = sys.stdin.read().strip().splitlines()
    board = [line.strip().split() for line in lines]
    rows = len(board)
    cols = len(board[0]) if board else 0
    return board, rows, cols

def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

def get_opponent(player):
    return 'W' if player == 'B' else 'B'

def generate_moves(board, player, ROWS, COLS):
    moves = []
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == get_opponent(player):
                        moves.append(((r, c), (nr, nc)))
    return moves

def apply_move(board, move):
    (r1, c1), (r2, c2) = move
    new_board = copy.deepcopy(board)
    new_board[r2][c2] = new_board[r1][c1]
    new_board[r1][c1] = '_'
    return new_board


# różnica pionków
def heuristic_B_1(board, player):  
    opp = get_opponent(player)
    return sum(row.count(player) for row in board) - sum(row.count(opp) for row in board)

# różnica możliwych ruchów
def heuristic_B_2(board, player):
    opp = get_opponent(player)
    return len(generate_moves(board, player)) - len(generate_moves(board, opp))

# liczba możliwych bic
def heuristic_B_3(board, player):  
    return len(generate_moves(board, player))

# liczba bezpiecznych pionków
def heuristic_W_1(board, player):
    opp = get_opponent(player)
    safe = 0
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == player:
                is_safe = True
                for dr, dc in DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < len(board) and 0 <= nc < len(board[0]):
                        if board[nr][nc] == opp:
                            is_safe = False
                if is_safe:
                    safe += 1
    return safe

# minimalizacja ruchów przeciwnika
def heuristic_W_2(board, player):
    opp = get_opponent(player)
    return -len(generate_moves(board, opp))

# kontrola centrum
def heuristic_W_3(board, player):
    center_rows = [len(board)//2 - 1, len(board)//2]
    center_cols = [len(board[0])//2 - 1, len(board[0])//2]
    score = 0
    for r in center_rows:
        for c in range(len(board[0])):
            if board[r][c] == player:
                score += 1
    for r in range(len(board)):
        for c in center_cols:
            if board[r][c] == player:
                score += 1
    return score

HEURISTICS = {
    'B': {
        '1': heuristic_B_1,
        '2': heuristic_B_2,
        '3': heuristic_B_3
    },
    'W': {
        '1': heuristic_W_1,
        '2': heuristic_W_2,
        '3': heuristic_W_3
    }
}


def minimax(board, depth, maximizing_player, player, heuristic, ROWS, COLS):
    moves = generate_moves(board, player, ROWS, COLS)
    if depth == 0 or not moves:
        return heuristic(board, player), None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval, _ = minimax(new_board, depth - 1, False, get_opponent(player), heuristic, ROWS, COLS)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval, _ = minimax(new_board, depth - 1, True, get_opponent(player), heuristic, ROWS, COLS)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move


def alphabeta(board, depth, maximizing_player, alpha, beta, player, heuristic, ROWS, COLS):
    moves = generate_moves(board, player, ROWS, COLS)
    if depth == 0 or not moves:
        return heuristic(board, player), None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval, _ = alphabeta(new_board, depth - 1, False, alpha, beta, get_opponent(player), heuristic, ROWS, COLS)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval, _ = alphabeta(new_board, depth - 1, True, alpha, beta, get_opponent(player), heuristic, ROWS, COLS)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def main():
    board, ROWS, COLS = read_board()
    heuristics = {
        'B': HEURISTICS['B'][1],
        'W': HEURISTICS['W'][1]
    }
    depth = 4
    current_player = 'B'

    while True:
        print(f"Tura gracza {current_player}")
        print_board(board)

        moves = generate_moves(board, current_player, ROWS, COLS)
        if not moves:
            print(f"Brak ruchów dla gracza {current_player}. Koniec gry.")
            break

        _, best_move = minimax(board, depth, True, float('-inf'), float('inf'), current_player, heuristics[current_player], ROWS, COLS)
        if best_move:
            board = apply_move(board, best_move)
            print(f"Gracz {current_player} wykonuje ruch: {best_move}")
        else:
            print("Brak możliwego ruchu!")

        current_player = get_opponent(current_player)

if __name__ == "__main__":
    main()
