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

    def center_knights(self, board):

        return 0

    def eval(self, board):
        result = board.result()
        if result != '*':
            if result == "1/2-1/2":
                return 0
            elif result[0] == "0":
                return -1e4
            elif result[0] == "1":
                return 1e4
        
        score = 0
        values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1,\
                  'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -1}
        for c in board.board_fen():
            if c.isalpha() and c in values:
                score += values[c]

        # To add
        # Knights near the center of the board 0.1
        score += self.center_knights(board)
        # Kings in the back rank in the early game 0.1
        
        return score if self.board.turn else 1-score

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
            return 69, next(iter(board.legal_moves))
        
        color = 1 if board.turn else -1
        return self.negamax(board, self.depth, color)


# Initial call for Player A's root node
# negamax(rootNode, depth, −∞, +∞, 1)