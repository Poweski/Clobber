import sys
import copy

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
COLS, ROWS = 5, 6

def read_board():
    lines = sys.stdin.read().strip().splitlines()
    board = [line.strip().split() for line in lines]
    return board

def print_board(board):
    for row in board:
        print(' '.join(row))

def get_opponent(player):
    return 'W' if player == 'B' else 'B'

def generate_moves(board, player):
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

# pawn difference
def heuristic_B_1(board, player):  
    opp = get_opponent(player)
    return sum(row.count(player) for row in board) - sum(row.count(opp) for row in board)

# difference of possible moves
def heuristic_B_2(board, player):
    opp = get_opponent(player)
    return len(generate_moves(board, player)) - len(generate_moves(board, opp))

# number of possible bics
def heuristic_B_3(board, player):  
    return len(generate_moves(board, player))

# number of safe pawns
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

#minimizing opponent's movements
def heuristic_W_2(board, player):
    opp = get_opponent(player)
    return -len(generate_moves(board, opp))

# center control
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

def choose_adaptive_heuristic(board, player):
    total_pieces = sum(row.count('B') + row.count('W') for row in board)

    # Early game
    if total_pieces > 20:
        chosen = '1'
    # Mid game
    elif total_pieces > 10:
        chosen = '2'
    # Late game
    else:
        chosen = '3'

    return HEURISTICS[player][chosen]

def minimax(board, depth, maximizing_player, player, heuristic):
    moves = generate_moves(board, player)
    if depth == 0 or not moves:
        return heuristic(board, player), None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval, _ = minimax(new_board, depth - 1, False, get_opponent(player), heuristic)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval, _ = minimax(new_board, depth - 1, True, get_opponent(player), heuristic)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move

def alphabeta(board, depth, maximizing_player, alpha, beta, player, heuristic):
    moves = generate_moves(board, player)
    if depth == 0 or not moves:
        return heuristic(board, player), None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval, _ = alphabeta(new_board, depth - 1, False, alpha, beta, get_opponent(player), heuristic)
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
            eval, _ = alphabeta(new_board, depth - 1, True, alpha, beta, get_opponent(player), heuristic)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def play_ai_vs_ai(board, depth, isMinimaxAlgorithm):
    current_player = 'B'
    print_board(board)
    while True:
        heuristic_fn = choose_adaptive_heuristic(board, current_player)

        if isMinimaxAlgorithm:
            _, move = minimax(board, depth, True, current_player, heuristic_fn)
        else:
            _, move = alphabeta(board, depth, True, float('-inf'), float('inf'), current_player, heuristic_fn)

        if move is None:
            print(f"No moves for player {current_player}. Game over.")
            break

        board = apply_move(board, move)

        print(f"\nPlayer {current_player} makes a move: {move}")
        print_board(board)

        current_player = get_opponent(current_player)

def main():
    board = read_board()
    depth = 4
    isMinimaxAlgorithm = False

    play_ai_vs_ai(board, depth, isMinimaxAlgorithm)

# Get-Content board.txt | python clobber.py
if __name__ == "__main__":
    main()
