import chess

class TyBotMM:
    def __init__(self, gamestate=chess.STARTING_FEN):
        self.board = chess.Board(gamestate)

    def update_fen(self, fen):
        self.board.set_fen(fen)

    # Should return the move the bot chooses
    def move(self):
        if len(list(self.board.legal_moves)) == 1:
            return next(iter(self.board.legal_moves))
        return self.monte_carlo_tree_search().last_move

    def eval(self, board):
        # Evaluates for white
        # Reverses if black's turn
        white = 0
        total = 0
        values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1}
        for c in self.board.board_fen():
            if c.isalpha():
                if c in values:
                    white += values[c]
                total += values[c.upper()]
            
        score = white / total
        return score if self.board.turn else 1-score

    def order_moves(self, board, moves):
        def eval_move(move):
            board.push(move)
            score = self.eval(board)
            board.pop()
            return score
        return sorted(moves, key=eval_move)

    def negamax(self, board, depth, a, b, color):
        if depth == 0 or board.result() != '*':
            return color * self.eval(board)

        moves = self.orderMoves(board, board.legal_moves)
        value = -1e9
        for move in moves:
            board.push(move)
            value = max(value, -1 * self.negamax(board, depth-1, -b, -a, -color))
            board.pop()
            a = max(a, value)
            if a >= b:
                break
        return value
    
    def choose(self, board):
        pass

# Initial call for Player A's root node
# negamax(rootNode, depth, −∞, +∞, 1)