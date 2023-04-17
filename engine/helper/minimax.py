class Minimax:
    def __init__(self, start_node):
        self.start_node = start_node

    def get_the_best_move(self):
        # If no available moves for current move...
        if self.start_node.is_terminal:
            raise GeneratorExit('LOSS')

        state = self.maximize(self.start_node)



    def maximize(self, node):
        for descendants in node:
            if descendants.is_teminal:
                print('terminal')





    def minimize(self, node):
        print('minimizing')

