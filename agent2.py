import chess
import random

class TyBotNM:
    def __init__(self, gamestate=chess.STARTING_FEN, depth=4):
        self.board = chess.Board(gamestate)
        self.depth = depth

    def update_fen(self, fen):
        self.board.set_fen(fen)

    # Should return the move the bot chooses
    def move(self):
        if len(list(self.board.legal_moves)) == 1:
            return next(iter(self.board.legal_moves))
        return self.monte_carlo_tree_search().last_move

    def center_knights(self, positions):
        score = 0
        if 'N' in positions:
            for pos in positions['N']:
                score += 7 - (abs(4.5 - pos[0]) + abs(4.5 - pos[1]))
        if 'n' in positions:
            for pos in positions['n']:
                score -= 7 - (abs(4.5 - pos[0]) + abs(4.5 - pos[1]))
        return score / 2 # convert to centipawns

    def king_safety(self, positions):
        score = 0
        score += -abs(2 - abs(3.5 - positions['K'][0][1]))
        score -= -abs(2 - abs(3.5 - positions['k'][0][1]))
        return score
    
    def pawn_aggression(self, positions):
        score = 0
        if 'P' in positions:
            for pos in positions['P']:
                score += 6 - pos[0]
        if 'p' in positions:
            for pos in positions['p']:
                score -= pos[0] - 1
        return score # convert to centipawns
    
    def center_control(self, legal_moves, turn):
        legal_moves = map(lambda x : str(x), legal_moves)
        score = 0
        center = ["d4", "d5", "e4", "e5"]
        for move in legal_moves:
            if move[2:3] in center:
                score += 1
        score *= 4
        return -score if turn else score

    # board should be a fen of a board
    def eval(self, board):
        result = board.result()
        if result != '*':
            if result == "1/2-1/2":
                return 0
            elif result[0] == "0":
                return -1e4
            elif result[0] == "1":
                return 1e4
        
        board_fen = board.board_fen()
        score = 0
        col = 0
        row = 0
        positions = {}
        values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1,\
                  'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -1}
        for c in board_fen:
            if c.isalpha() and c in values:
                score += values[c]
                if c in positions:
                    positions[c].append((row, col))
                else:
                    positions.update({c: [(row, col)]})
                col += 1
            elif c.isdigit():
                col += int(c)
            elif c == '/':
                row += 1
                col = 0
        score *= 100
        # To add
        # Knights near the center of the board 0.1
        score += self.center_knights(positions)
        score += self.king_safety(positions)
        score += self.pawn_aggression(positions)
        score += self.center_control(board.legal_moves, board.turn)
        # Kings in the back rank in the early game 0.1
        
        return score

    def order_moves(self, board, moves):
        def eval_move(move):
            board.push(move)
            score = self.eval(board)
            board.pop()
            return score
        return sorted(moves, key=eval_move)

    def negamax(self, board, depth, color):
        if depth == 0 or board.result() != '*':
            return color * self.eval(board) - depth * 100, None

        # moves = self.order_moves(board, board.legal_moves)
        moves = board.legal_moves
        best_moves = []
        value = -1e5
        for move in moves:
            board.push(move)
            score = -int(self.negamax(board, depth-1, -color)[0])
            board.pop()
            # if depth == self.depth:
            #     print("{}{}: {}".format("|"*(self.depth-depth), move, score))
            if score == value:
                best_moves.append(move)
            if score > value:
                value = score
                best_moves = [move]
            # a = max(a, value)
            # if a >= b:
            #     break
        return value, random.choice(best_moves)
    
    def move(self, board):
        if len(list(board.legal_moves)) == 1:
            return 69420, next(iter(board.legal_moves))
        
        color = 1 if board.turn else -1
        return self.negamax(board, self.depth, color)


# Initial call for Player A's root node
# negamax(rootNode, depth, −∞, +∞, 1)