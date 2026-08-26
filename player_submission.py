import random
from copy import deepcopy
from collections import deque
from game import Board

def get_active_player_position(game):
    row, col, _ = game.__last_queen_move__[game.get_active_players_queen()]
    return (row, col)

def get_inactive_player_position(game):
    row, col, _ = game.__last_queen_move__[game.get_inactive_players_queen()]
    return (row, col)

def get_blocked_squares(game):
    board_state = game.get_state()
    blocked = set()
    for r in range(game.height):  
        for c in range(game.width):
            if board_state[r][c] == Board.BLOCKED:
                blocked.add((r, c))
    return blocked

class OpenMoveEvalFn:
    def score(self, game, maximizing_player_turn=True):
        player_moves = len(game.get_legal_moves())
        opponent_moves = len(game.get_opponent_moves())
        return player_moves - opponent_moves

class CustomEvalFn:
    def score(self, game, maximizing_player_turn=True):
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return float("-inf")  

        active_pos = get_active_player_position(game)
        inactive_pos = get_inactive_player_position(game)

        player_moves = len(legal_moves)
        opponent_moves = len(game.get_opponent_moves())

        
        center_positions = [(3,3), (3,4), (4,3), (4,4)]
        center_bonus = 10 if active_pos in center_positions else 0

        
        push_bonus = 15 if any(move[2] for move in legal_moves) else 0

        
        mobility = player_moves - opponent_moves

        return mobility + center_bonus + push_bonus

def detect_trap(game, pos):
    blocked = get_blocked_squares(game)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]
    trap_count = 0

    for dr, dc in directions:
        new_r, new_c = pos[0] + dr, pos[1] + dc
        if not game.move_is_in_board(new_r, new_c) or (new_r, new_c) in blocked:
            trap_count += 1

    return trap_count >= 6 

def is_near_margin(pos, board_width, board_height):
    r, c = pos
    return r <= 1 or r >= board_height - 2 or c <= 1 or c >= board_width - 2

def is_opponent_in_margin_and_push(game, legal_moves):
    margin_positions = [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
        (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), 
        (1, 6), (2, 6), (3, 6), (4, 6), (5, 6),
        (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)
    ]

    opponent_pos = game.__last_queen_move__[game.get_inactive_players_queen()]
    opp_row, opp_col, _ = opponent_pos

    if (opp_row, opp_col) in margin_positions:
        for move in legal_moves:
            r, c, is_push = move
            if is_push and (r, c) == (opp_row, opp_col):
                return move  

    return None

def in_margin_and_push(game, legal_moves):
    margin_positions = [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
        (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), 
        (1, 6), (2, 6), (3, 6), (4, 6), (5, 6),
        (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)
    ]
    safe_moves = []
    opponent_moves = game.get_opponent_moves()

    for move in legal_moves:
        row, col, is_push = move
        if (row, col) in margin_positions and (row, col, False) in opponent_moves:
            continue
        else:
            safe_moves.append(move)

    return safe_moves if safe_moves else legal_moves

class CustomPlayer:

    def __init__(self, search_depth=6, eval_fn=CustomEvalFn()):
        self.eval_fn = eval_fn
        self.search_depth = search_depth

    def move(self, game, legal_moves, time_left):
        
        if not legal_moves:
            return None
        first_random_move = [ (5, 1, False) , (1, 5, False), (1, 1, False) , (5, 5, False)] 
        
        if  game.move_count == 1:
            return random.choice(first_random_move) 
        
        filtered_moves = in_margin_and_push(game, legal_moves)
        
        best_move = None
        self.search_depth = dynamic_depth_adjustment(game, self.search_depth)
        
        depth = 1

        while time_left() > 100 and depth <= self.search_depth:
            move, _ = self.alphabeta(game, depth, float("-inf"), float("inf"), True, filtered_moves)
            if move:
                best_move = move
            depth += 1

        if not best_move and filtered_moves:
            best_move = random.choice(filtered_moves)

        if not best_move and legal_moves:
            best_move = random.choice(legal_moves)

        return best_move

    def utility(self, game, maximizing_player):
        return self.eval_fn.score(game, maximizing_player_turn=maximizing_player)

    def alphabeta(self, game, depth, alpha, beta, maximizing_player=True, filtered_moves=None):
        if filtered_moves is not None:
            legal_moves = filtered_moves
        else:
            legal_moves = game.get_legal_moves()

        if depth == 0 or not legal_moves:
            return None, self.utility(game, maximizing_player)

        legal_moves.sort(key=lambda m: move_flexibility_score(game, m), reverse=maximizing_player)

        best_move = None
        if maximizing_player:
            best_value = float("-inf")
            for move in legal_moves:
                next_state, is_over, winner = game.forecast_move(move)
                if is_over:
                    val = float("inf") if winner == game.get_active_players_queen() else float("-inf")
                else:
                    _, val = self.alphabeta(next_state, depth - 1, alpha, beta, False)
    
                if val > best_value:
                    best_value = val
                    best_move = move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
        else:
            best_value = float("inf")
            for move in legal_moves:
                next_state, is_over, winner = game.forecast_move(move)
                if is_over:
                    val = float("-inf") if winner == game.get_inactive_players_queen() else float("inf")
                else:
                    _, val = self.alphabeta(next_state, depth - 1, alpha, beta, True)
    
                if val < best_value:
                    best_value = val
                    best_move = move
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        return best_move, best_value

def move_flexibility_score(game, move):
    next_state, _, _ = game.forecast_move(move)
    return len(next_state.get_legal_moves())

def dynamic_depth_adjustment(game, max_depth):
    if game.move_count < 10:
        return 2
    elif 10 <= game.move_count < 20:
        return 4
    elif 20 <= game.move_count < 30:
        if max_depth > 4:
            return max_depth
        else: 
            max_depth = 6
            return max_depth
    else: 
        return max_depth + 2
