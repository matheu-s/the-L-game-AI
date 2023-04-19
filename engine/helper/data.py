import game.board
from config.constants import ROWS, COLS
from engine.helper.node import Node
from typing import Optional, Dict, List


def nice_print(state):
    s = [[str(e) for e in row] for row in state]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))
    print('----------------------------------')


class Data:
    def __init__(self):
        self.matrix_squares_state = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.root = None  # It's set after state is set too on set_state()
        self.nodes_count = 0

    def set_state(self, data):
        """Update local matrix to make data handling easier"""

        index_offset = 1
        for key in data:
            row, col = key.split(',')
            row = int(row) - index_offset
            col = int(col) - index_offset
            piece = data.get(key)
            if piece:
                self.matrix_squares_state[row][col] = piece
            else:
                self.matrix_squares_state[row][col] = 1
        # Setting the root
        self.root = Node(self.matrix_squares_state, None, 0, 'L2')
        nice_print(self.root.state)

    def generate_game_tree(self):
        self.__expand(self.root)

    def __expand(self, root: Node):
        stack = []
        root.expand()

        for desc in root.descendants:
            stack.append(desc)

        # Removed recursion due to stack overflow errors...
        while len(stack):
            node = stack.pop()
            node.expand()
            self.nodes_count += 1
            for desc in node.descendants:
                # stack.insert(0, desc)
                stack.append(desc)
            # if self.nodes_count > 100:
            #     child1 = self.root.descendant[0]
            #     test family tree
            #     print()
        print('Finished moves generation')

    def find_the_best_move(self, start_node=None):
        if not start_node:
            start_node = self.root

        print('first generation: ')
        print('gen: ', start_node.descendants[3].generation)
        print('eval: ', start_node.descendants[3].evaluation)
        chosen_move = start_node.descendants[3].state
        nice_print(chosen_move)

        print('second gen: ')
        print('gen: ', start_node.descendants[3].descendants[0].generation)
        print('eval2: ', start_node.descendants[3].descendants[0].evaluation)
        chosen_move2 = start_node.descendants[3].descendants[0].state
        nice_print(chosen_move2)

        # print('third gen: ')
        # print('gen: ',  start_node.descendants[3].descendants[0].generation)
        # print('eval3: ', start_node.descendants[3].descendants[0].descendants[0].evaluation)
        # chosen_move3 = start_node.descendants[3].descendants[0].descendants[0].state
        # nice_print(chosen_move3)

        return chosen_move
        #logic here or in Lphant? handling the minimax... maybe later
        # for desc in start_node.descendants:



