from math import inf as Infity
import sys

sys.setrecursionlimit(20000)


class Minimax:
    def __init__(self, start_node):
        self.start_node = start_node

    def get_the_best_move(self):
        # If no available moves for current move...
        if self.start_node.is_terminal:
            raise GeneratorExit('LOSS')

        move, score = self.maximize(self.start_node)
        if score == 10:
            print('BOT WIN!')
        print('Current state score: ', score)
        return [move, score]

    def maximize(self, node):
        """Returns the maximized value and its state, recursive calls with minimize()"""

        if node.is_terminal:
            return [node.state, node.evaluation]

        max_score = -Infity
        max_state = None
        for descendant in node.descendants:
            state, score = self.minimize(descendant)
            if score > max_score and score != -10:
                max_score = descendant.evaluation
                max_state = descendant.state

        return [max_state, max_score]

    def minimize(self, node):
        """Returns the minimized value and its state, recursive calls with maximize()"""

        if node.is_terminal:
            return [node.state, node.evaluation]

        min_score = Infity
        min_state = None
        for descendant in node.descendants:
            state, score = self.maximize(descendant)
            if score < min_score:
                min_score = descendant.evaluation
                min_state = descendant.state

        return [min_state, min_score]
