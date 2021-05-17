import chess

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

    def eval(self, board):
        result = board.result()
        if result == "1/2-1/2":
            return 0
        elif result[0] == "0":
            return -1e8
        elif result[0] == "1":
            return 1e8
        
        score = 0
        values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1,\
                  'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -1}
        for c in board.board_fen():
            if c.isalpha() and c in values:
                score += values[c]
        
        # if board.is_check():
        #     score += 0.1 if board.turn else -0.1

        # To add
        # Knights near the center of the board 0.1
        # Kings in the back rank in the early game 0.1
        # Attacking the queen? 0.2
        
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
            return color * self.eval(board), None

        # moves = self.order_moves(board, board.legal_moves)
        moves = board.legal_moves
        best = next(iter(moves))
        value = -1e8
        for move in moves:
            board.push(move)
            score = -int(self.negamax(board, depth-1, -b, -a, -color)[0])
            score += depth/100
            board.pop()
            if depth == self.depth:
                print("{}{}: {}".format("|"*(4-depth), move, score))
            if score > value:
                value = score
                best = move
            a = max(a, value)
            if a >= b:
                break
        return value, best
    
    def move(self, board):
        best_move = next(iter(board.legal_moves))
        if len(list(board.legal_moves)) == 1:
            return best_move
        
        color = 1 if board.turn else -1
        return self.negamax(board, self.depth, -1e9, 1e9, color)[1]


# Initial call for Player A's root node
# negamax(rootNode, depth, −∞, +∞, 1)