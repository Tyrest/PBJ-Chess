import chess
import chess.svg
import time

from agent1 import TyBot
from agent2 import TyBotNM

def render(board):
    boardsvg = chess.svg.board(board)
    f = open("board.SVG", "w")
    f.write(boardsvg)
    f.close()

def MCTSmirror():
    print("MCTS Bot Mirror Match\n=====================")
    board = chess.Board()
    bot = TyBot()

    while board.result() == "*":
        render(board)
        # print(str(board) + "\n")

        move = bot.move()
        board.push(move)
        bot.update_fen(board.fen())
        print(move)
    
    render(board)
    print(board.result())

def NMmirror():
    print("Negamax Bot Mirror Match\n========================")
    board = chess.Board()
    bot = TyBotNM()

    while board.result() == "*":
        render(board)
        move = bot.move(board)
        board.push(move)
        print(move)
    
    render(board)
    print(board.result())

def botvbot():
    print("Negamax vs MCTS\n===============")
    board = chess.Board()
    MCTSbot = TyBot()
    NMbot = TyBotNM()

    turn = 1

    if input("MCTS color? (W or B): ") == "B":
        turn = 0

    while board.result() == "*":
        render(board)
        if not turn:
            move = NMbot.move(board)
            board.push(move)
            print(move)
            MCTSbot.update_fen(board.fen())
        else:
            move = MCTSbot.move()
            board.push(move)
            print(move)
        turn = 1 - turn
    render(board)
    print(board.result())

def botvplayer():
    board = chess.Board()
    bot = TyBot()

    turn = 0

    if input("color? (W or B): ") == "B":
        turn = 1

    while board.result() == "*":
        render(board)
        if not turn:
            valid_moves = [str(x) for x in list(board.legal_moves)]

            print("Legal moves are: {}".format(valid_moves))
            move = input("Input your move: ")
            while move not in valid_moves:
                print("Legal moves are: {}".format(valid_moves))
                move = input("Please input a legal move: ")
            board.push_uci(move)
            bot.update_fen(board.fen())
        else:
            move = bot.move()
            board.push(move)
            print(move)
        turn = 1 - turn
    render(board)
    print(board.result())

def nextmove(fen):
    board = chess.Board(fen)
    render(board)
    bot = TyBotNM()
    move = bot.move(board)
    board.push(move)
    print(move)
    render(board)
    return move

def test1move():
    nextmove("4k3/R7/1R6/8/8/8/8/4K3 w - - 0 1")
    time.sleep(2)
    nextmove("4k3/8/4K3/6Q1/8/8/8/8 w - - 0 1")
    time.sleep(2)
    nextmove("4k3/P7/4K3/8/8/8/8/8 w - - 0 1")
    time.sleep(2)
    nextmove("4k3/8/8/8/8/1r6/r7/4K3 b - - 0 1")

def test2move():
    nextmove("4k3/R7/4K3/8/5b2/8/8/8 w - - 0 1") #a7a8
    time.sleep(2)
    nextmove("r6k/pp1b2p1/3Np2p/8/3p1PRQ/2nB4/q1P4P/2K5 w - - 0 1") # h4h6
    time.sleep(2)
    nextmove("R1Q5/1p3p2/1k1qpb2/8/P2p4/P2P2P1/4rPK1/8 w - - 0 1") # a4a5
    time.sleep(2)
    nextmove("r6k/6pp/6n1/1p2pR2/3q4/1B5Q/P1P3P1/1K6 w - - 0 1") # h3h7
    time.sleep(2)
    nextmove("rnbq2kr/ppp3pp/4P2n/3p2NQ/4p3/B1P5/P1P2PPP/R3KB1R w K - 0 1") # h5f7
    time.sleep(2)
    nextmove("4k3/8/3K1R2/8/5P2/8/8/8 w - - 0 1")

def main():
    # botvbot()
    # botvbotNM()
    # botvplayer()
    test1move()
    # test2move()

if __name__ == "__main__":
    main()