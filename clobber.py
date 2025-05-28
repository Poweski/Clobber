import sys
import copy
import time

# --- Constants ---
PLAYER_B = 'B'
PLAYER_W = 'W'
EMPTY = '_'
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
COLS, ROWS = 5, 6
GAME_DEPTH = 3
STARTING_PLAYER_EXTENDED = PLAYER_B
GAME_VERSION_CHOICE = "extended"
AGENT_B_SETTINGS = {
    "algorithm_type": "alphabeta",
    "heuristic_key": "adaptive",
    "depth": GAME_DEPTH
}
AGENT_W_SETTINGS = {
    "algorithm_type": "alphabeta",
    "heuristic_key": "2",
    "depth": GAME_DEPTH
}

# --- Board Utilities ---
def read_board():
    lines = sys.stdin.read().strip().splitlines()
    board = [line.strip().split() for line in lines]
    return board

def print_board_to_stdout(board):
    for row in board:
        print(' '.join(row))

def get_opponent(player):
    return PLAYER_W if player == PLAYER_B else PLAYER_B

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
    new_board[r1][c1] = EMPTY
    return new_board

# --- Heuristics ---
def heuristic_B_1(board, player_perspective):
    opp = get_opponent(player_perspective)
    return sum(row.count(player_perspective) for row in board) - sum(row.count(opp) for row in board)

def heuristic_B_2(board, player_perspective):
    opp = get_opponent(player_perspective)
    return len(generate_moves(board, player_perspective)) - len(generate_moves(board, opp))

def heuristic_B_3(board, player_perspective):
    return len(generate_moves(board, player_perspective))

def heuristic_W_1(board, player_perspective):
    opp = get_opponent(player_perspective)
    safe = 0
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player_perspective:
                is_safe = True
                for dr_opp, dc_opp in DIRECTIONS:
                    nr_opp_attacker, nc_opp_attacker = r + dr_opp, c + dc_opp
                    if 0 <= nr_opp_attacker < ROWS and 0 <= nc_opp_attacker < COLS and \
                       board[nr_opp_attacker][nc_opp_attacker] == opp:
                        is_safe = False
                        break
                if is_safe:
                    safe += 1
    return safe

def heuristic_W_2(board, player_perspective):
    opp = get_opponent(player_perspective)
    return -len(generate_moves(board, opp))

def heuristic_W_3(board, player_perspective):
    center_rows = [ROWS//2 - 1, ROWS//2]
    center_cols = [COLS//2 -1, COLS//2, COLS//2 + 1] if COLS % 2 != 0 else [COLS//2 -1, COLS//2]
    score = 0
    for r_idx in range(ROWS):
        for c_idx in range(COLS):
            if board[r_idx][c_idx] == player_perspective:
                if r_idx in center_rows or c_idx in center_cols:
                    score +=1
                    if r_idx in center_rows and c_idx in center_cols:
                        score +=1
    return score

HEURISTICS = {
    PLAYER_B: {'1': heuristic_B_1, '2': heuristic_B_2, '3': heuristic_B_3},
    PLAYER_W: {'1': heuristic_W_1, '2': heuristic_W_2, '3': heuristic_W_3}
}

def choose_adaptive_heuristic(board, player):
    my_pieces = sum(row.count(player) for row in board)
    opponent_pieces = sum(row.count(get_opponent(player)) for row in board)
    total_pieces_on_board = my_pieces + opponent_pieces

    if total_pieces_on_board > (ROWS * COLS * 2/3):
        chosen_key = '1'
    elif total_pieces_on_board > (ROWS * COLS * 1/3):
        chosen_key = '2'
    else:
        chosen_key = '3'

    if chosen_key not in HEURISTICS[player]:
        chosen_key = '1'
    return HEURISTICS[player][chosen_key]

# --- Search Algorithms ---
def minimax(board, depth, maximizing_turn, root_player, heuristic_for_root_player):
    nodes_visited_total = 1
    actual_mover = root_player if maximizing_turn else get_opponent(root_player)
    moves = generate_moves(board, actual_mover)

    if depth == 0 or not moves:
        return heuristic_for_root_player(board, root_player), None, nodes_visited_total

    best_move = moves[0] if moves else None

    if maximizing_turn:
        max_eval = float('-inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval_val, _, nodes_subtree = minimax(new_board, depth - 1, False, root_player, heuristic_for_root_player)
            nodes_visited_total += nodes_subtree
            if eval_val > max_eval:
                max_eval = eval_val
                best_move = move
        return max_eval, best_move, nodes_visited_total
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval_val, _, nodes_subtree = minimax(new_board, depth - 1, True, root_player, heuristic_for_root_player)
            nodes_visited_total += nodes_subtree
            if eval_val < min_eval:
                min_eval = eval_val
                best_move = move
        return min_eval, best_move, nodes_visited_total

def alphabeta(board, depth, alpha, beta, maximizing_turn, root_player, heuristic_for_root_player):
    nodes_visited_total = 1
    actual_mover = root_player if maximizing_turn else get_opponent(root_player)
    moves = generate_moves(board, actual_mover)

    if depth == 0 or not moves:
        return heuristic_for_root_player(board, root_player), None, nodes_visited_total

    best_move = moves[0] if moves else None

    if maximizing_turn:
        max_eval = float('-inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval_val, _, nodes_subtree = alphabeta(new_board, depth - 1, alpha, beta, False, root_player, heuristic_for_root_player)
            nodes_visited_total += nodes_subtree
            if eval_val > max_eval:
                max_eval = eval_val
                best_move = move
            alpha = max(alpha, eval_val)
            if beta <= alpha:
                break
        return max_eval, best_move, nodes_visited_total
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = apply_move(board, move)
            eval_val, _, nodes_subtree = alphabeta(new_board, depth - 1, alpha, beta, True, root_player, heuristic_for_root_player)
            nodes_visited_total += nodes_subtree
            if eval_val < min_eval:
                min_eval = eval_val
                best_move = move
            beta = min(beta, eval_val)
            if beta <= alpha:
                break
        return min_eval, best_move, nodes_visited_total

# --- Game Playing Functions ---
def play_basic_minimax_vs_minimax(initial_board):
    current_board = copy.deepcopy(initial_board)
    current_player = PLAYER_B
    ply_count = 0
    winner = None
    score = 0
    total_nodes_game = 0
    total_time_game = 0.0

    while True:
        ply_count += 1
        heuristic_fn = choose_adaptive_heuristic(current_board, current_player)
        
        start_time = time.perf_counter()
        score, move, nodes_turn = minimax(current_board, GAME_DEPTH, True, current_player, heuristic_fn)
        end_time = time.perf_counter()
        time_turn = end_time - start_time

        total_nodes_game += nodes_turn
        total_time_game += time_turn
        
        if move is None:
            winner = get_opponent(current_player)
            break
        
        current_board = apply_move(current_board, move)

        opponent_pieces_left = sum(row.count(get_opponent(current_player)) for row in current_board)
        if opponent_pieces_left == 0:
            winner = current_player
            break
            
        current_player = get_opponent(current_player)

    print_board_to_stdout(current_board)
    num_rounds = (ply_count -1) // 2 + 1 if ply_count > 0 else 0
    if winner is None :
        if ply_count > 0: winner = get_opponent(current_player)
        else: winner = "Draw/Undetermined"
    print(f"Rounds: {num_rounds}, Winner: {winner}")

    print(f"Total nodes visited: {total_nodes_game}", file=sys.stderr)
    print(f"Total AI computation time: {total_time_game:.4f}s", file=sys.stderr)


class Agent:
    def __init__(self, player_id, algorithm_type, heuristic_key, depth):
        self.player_id = player_id
        self.algorithm_type = algorithm_type.lower()
        self.heuristic_key = heuristic_key
        self.depth = depth
        self.heuristic_fn_name = "N/A"

    def get_heuristic_fn(self, board):
        if self.heuristic_key == "adaptive":
            selected_fn = choose_adaptive_heuristic(board, self.player_id)
            self.heuristic_fn_name = f"adaptive -> {selected_fn.__name__}"
            return selected_fn
        else:
            try:
                selected_fn = HEURISTICS[self.player_id][self.heuristic_key]
                self.heuristic_fn_name = selected_fn.__name__
                return selected_fn
            except KeyError:
                self.heuristic_key = "adaptive"
                selected_fn = choose_adaptive_heuristic(board, self.player_id)
                self.heuristic_fn_name = f"adaptive_fallback -> {selected_fn.__name__}"
                return selected_fn

    def get_move_and_stats(self, board):
        heuristic_function = self.get_heuristic_fn(board)
        nodes_turn = 0
        move = None
        score = 0

        start_time = time.perf_counter()
        if self.algorithm_type == "minimax":
            score, move, nodes_turn = minimax(board, self.depth, True, self.player_id, heuristic_function)
        elif self.algorithm_type == "alphabeta":
            score, move, nodes_turn = alphabeta(board, self.depth, float('-inf'), float('inf'), True, self.player_id, heuristic_function)
        else:
            score, move, nodes_turn = alphabeta(board, self.depth, float('-inf'), float('inf'), True, self.player_id, heuristic_function)
        end_time = time.perf_counter()
        time_turn = end_time - start_time
        
        return score, move, nodes_turn, time_turn

def play_extended_agents_game(initial_board):
    agent_B = Agent(PLAYER_B, **AGENT_B_SETTINGS)
    agent_W = Agent(PLAYER_W, **AGENT_W_SETTINGS)
    current_board = copy.deepcopy(initial_board)
    winner = None
    score = 0
    total_nodes_game = 0
    total_time_game = 0.0
    
    if STARTING_PLAYER_EXTENDED == PLAYER_B:
        current_agent, next_agent = agent_B, agent_W
    else:
        current_agent, next_agent = agent_W, agent_B

    ply_count = 0
    while True:
        ply_count += 1
        score, move, nodes_turn, time_turn = current_agent.get_move_and_stats(current_board)
        total_nodes_game += nodes_turn
        total_time_game += time_turn

        if move is None:
            winner = next_agent.player_id
            break
        
        current_board = apply_move(current_board, move)

        opponent_pieces_left = sum(row.count(next_agent.player_id) for row in current_board)
        if opponent_pieces_left == 0:
            winner = current_agent.player_id
            break
            
        current_agent, next_agent = next_agent, current_agent

    print_board_to_stdout(current_board)
    num_rounds = (ply_count-1) // 2 + 1 if ply_count > 0 else 0
    if winner is None:
        if ply_count > 0: winner = next_agent.player_id
        else: winner = "Draw/Undetermined"
    print(f"Rounds: {num_rounds}, Winner: {winner}")

    print(f"Total nodes visited: {total_nodes_game}", file=sys.stderr)
    print(f"Total AI computation time: {total_time_game:.4f}s", file=sys.stderr)

# --- Main Execution ---
def main():
    initial_board_state = read_board()

    if GAME_VERSION_CHOICE == "basic":
        play_basic_minimax_vs_minimax(initial_board_state)
    
    elif GAME_VERSION_CHOICE == "extended":
        play_extended_agents_game(initial_board_state)
    else:
        print("Invalid GAME_VERSION_CHOICE set in code. Choose 'basic' or 'extended'.", file=sys.stderr)

if __name__ == "__main__":
    main()
