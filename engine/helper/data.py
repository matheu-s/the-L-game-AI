from engine.helper.node import Node


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

    def generate_game_tree(self):
        """Start nodes expansion from root"""

        self.__expand(self.root)

    def __expand(self, root: Node):
        """Handles the stack for nodes descendants generation """

        stack = []
        root.expand()

        for desc in root.descendants:
            stack.append(desc)

        while len(stack):
            node = stack.pop()
            node.expand()
            self.nodes_count += 1
            for desc in node.descendants:
                stack.append(desc)
        print('Finished moves generation')



