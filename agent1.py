"""
A minimal implementation of Monte Carlo tree search (MCTS) in Python 3
Luke Harold Miles, July 2019, Public Domain Dedication
See also https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
"""
from abc import ABC, abstractmethod
from collections import defaultdict
import math
import chess
import random
import time

class MCTS:
    "Monte Carlo tree searcher. First rollout the tree then choose a move."

    def __init__(self, exploration_weight=1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight

    def choose(self, node):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward
        
        # for child in self.children[node]:
        #     print("{}: {}".format(child.last_move, score(child)))

        return max(self.children[node], key=score)

    def do_rollout(self, node):
        "Make the tree one layer better. (Train for one iteration.)"
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

    def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node):
        "Update the `children` dict with the children of `node`"
        if node not in self.children:
            self.children[node] = node.find_children()

    # This is where the code spends most of its time
    # Try to optimize this???
    def _simulate(self, node):
        # wins = 0
        # for i in range(69):
        "Returns the reward for a random simulation (to completion) of `node`"
        return node.simulate()

    def _backpropagate(self, path, reward):
        "Send the reward back up to the ancestors of the leaf"
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa

    def _uct_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)


class Node(ABC):
    @abstractmethod
    def find_children(self):
        "All possible successors of this board state"
        return set()

    @abstractmethod
    def simulate(self):
        "Simulates the board till the end or till a set depth is passed"
        return None

    @abstractmethod
    def is_terminal(self):
        "Returns True if the node has no children"
        return True

    @abstractmethod
    def reward(self):
        "Assumes `self` is terminal node. 1=win, 0=loss, .5=tie, etc"
        return 0

    @abstractmethod
    def __hash__(self):
        "Nodes must be hashable"
        return 123456789

    @abstractmethod
    def __eq__(node1, node2):
        "Nodes must be comparable"
        return True

class ChessNode(Node):
    def __init__(self, gamestate=chess.STARTING_FEN, last_move=""):
        self.board = chess.Board(gamestate)
        self.last_move = last_move
        self.children = set()

    def find_children(self):
        for move in self.board.legal_moves:
            self.board.push(move)
            self.children.add(ChessNode(self.board.fen(), move))
            self.board.pop()
        return self.children

    def simulate(self):
        invert_reward = True
        initial_fen = self.board.fen()
        count = 0
        while not self.is_terminal():
            self.board.push(random.choice(list(self.board.legal_moves)))
            invert_reward = not invert_reward
            if count >= 7:
                score = self.eval()
                self.board.set_fen(initial_fen)
                return score
            count += 1
        self.board.set_fen(initial_fen)
        reward = self.reward()
        return 1-reward if invert_reward else reward

    def is_terminal(self):
        return self.board.result() != "*"

    def eval(self):
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
        return 1-score if self.board.turn else score

    def reward(self):
        # print(str(self.board) + "\n")
        if self.is_terminal():
            outcome = self.board.result()
            if outcome == "1/2-1/2":
                return 0.5
            else:
                return 0
        else:
            return self.eval()

    def __hash__(self):
        return hash(self.board.fen())

    def __eq__(self, node1):
        return self.board.fen() == node1.board.fen()

class TyBot:
    def __init__(self, gamestate=chess.STARTING_FEN):
        self.board = chess.Board(gamestate)

    def update_fen(self, fen):
        self.board.set_fen(fen)
    
    # Should return the move the bot chooses
    def move(self):
        if len(list(self.board.legal_moves)) == 1:
            return next(iter(self.board.legal_moves))
        return self.monte_carlo_tree_search().last_move
    
    def monte_carlo_tree_search(self):
        tree = MCTS()
        root = ChessNode(self.board.fen())
        start_time = time.time()
        count = 0
        while time.time() - start_time < 20:
            tree.do_rollout(root)
            count += 1
        # print("rollouts: {}".format(count))
        return tree.choose(root)