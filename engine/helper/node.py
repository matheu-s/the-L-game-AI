from config.constants import ROWS, COLS, DEPTH
from engine.helper.evaluator import Evaluator
from copy import deepcopy


def nice_print(state):
    s = [[str(e) for e in row] for row in state]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))
    print('----------------------------------')


def clean_piece(state, piece):
    """Removes own piece from board to place it again"""

    cleaned_state = deepcopy(state)
    for i in range(ROWS):
        for j in range(COLS):
            if cleaned_state[i][j] == piece:
                cleaned_state[i][j] = 1
    return cleaned_state


class Node:
    def __init__(self, state, ancestor=None, evaluation=0, player=None):
        self.state = state
        self.descendants = []
        self.ancestor = ancestor
        self.evaluation = evaluation
        self.is_terminal = False
        if ancestor:
            self.generation = ancestor.generation + 1
            self.player = 'L2' if self.ancestor.player == 'L1' else 'L1'
        else:
            self.generation = 0
            self.player = player

    def expand(self):
        if self.is_terminal:
            return

        # Remove its own piece from board
        piece = self.player
        state = clean_piece(self.state, piece)

        # Generates possible L moves
        L_moves = self.get_L_moves(state, piece)
        if len(L_moves) == 0 and self.player == 'L2':
            self.is_terminal = True
            self.evaluation = -10
            return
        if len(L_moves) == 0 and self.player == 'L1':
            self.is_terminal = True
            self.evaluation = 10
            return

        # Depth reached
        if self.generation == DEPTH:
            self.is_terminal = True
            return

        # Get all moves (include coin moves now)
        possible_moves = self.get_coin_moves(L_moves)
        evaluator_obj = Evaluator()
        for move in possible_moves:
            # print('Child: ')
            # nice_print(i)
            evaluation = evaluator_obj.get_score(move)
            self.descendants.append(Node(move, self, evaluation))

    def get_L_moves(self, state, l_piece):
        """Get all L moves"""

        # print('trying to find smt on this state: ')
        # nice_print(state)
        possible_L = []
        three_zeros_row = []
        three_zeros_col = []
        # Check rows with three 0's
        row_counter = 0
        for row in state:
            for i in range(4 - 2):
                if row[i] == row[i + 1] == row[i + 2] == 1:
                    three_zeros_row.append([row_counter, i, i + 1, i + 2])
            row_counter = row_counter + 1

        # Check columns with three 0's
        column_counter = 0
        for j in range(ROWS):
            column = [state[i][j] for i in range(COLS)]
            for i in range(4 - 2):
                if column[i] == column[i + 1] == column[i + 2] == 1:
                    three_zeros_col.append([column_counter, i, i + 1, i + 2])
            column_counter += 1

        # Checking adjacent 0 on found rows
        for arr in three_zeros_row:
            row_counter, i1, i2, i3 = arr
            # row below
            if row_counter != 3:
                for j in range(ROWS):
                    # if there is a 0 and is adjacent to head/tail
                    if state[row_counter + 1][j] == 1 and (j == i1 or j == i3):
                        found = deepcopy(state)
                        found[row_counter][i1] = l_piece
                        found[row_counter][i2] = l_piece
                        found[row_counter][i3] = l_piece
                        found[row_counter + 1][int(j)] = l_piece
                        # Adding new L move if it's diff from original
                        if self.check_state_diff(found):
                            possible_L.append(found)
            # row above
            if row_counter != 0:
                for j in range(ROWS):
                    # if there is a 0 and is adjacent to head/tail
                    if state[row_counter - 1][j] == 1 and (j == i1 or j == i3):
                        found = deepcopy(state)
                        found[row_counter][i1] = l_piece
                        found[row_counter][i2] = l_piece
                        found[row_counter][i3] = l_piece
                        found[row_counter - 1][int(j)] = l_piece
                        if self.check_state_diff(found):
                            possible_L.append(found)

        # Checking adjacent 0 on found cols
        for arr in three_zeros_col:
            col_counter, i1, i2, i3 = arr
            # col right
            if col_counter != 3:
                for j in range(COLS):
                    # if there is a 0 and is adjacent to head/tail
                    if state[j][col_counter + 1] == 1 and (j == i1 or j == i3):
                        found = deepcopy(state)
                        found[i1][col_counter] = l_piece
                        found[i2][col_counter] = l_piece
                        found[i3][col_counter] = l_piece
                        found[int(j)][col_counter + 1] = l_piece
                        if self.check_state_diff(found):
                            possible_L.append(found)

            # col left
            if col_counter != 0:
                for j in range(COLS):
                    # if there is a 0 and is adjacent to head/tail
                    if state[j][col_counter - 1] == 1 and (j == i1 or j == i3):
                        found = deepcopy(state)
                        found[i1][col_counter] = l_piece
                        found[i2][col_counter] = l_piece
                        found[i3][col_counter] = l_piece
                        found[int(j)][col_counter - 1] = l_piece
                        if self.check_state_diff(found):
                            possible_L.append(found)

        return possible_L

    def get_coin_moves(self, moves):
        """Get all coin moves for each L move"""

        possible_moves = []
        # Getting coin 1 moves
        for move in moves:
            new_c1_cleaned = clean_piece(move, 'C1')
            new_c2_cleaned = clean_piece(move, 'C2')
            for i in range(ROWS):
                for j in range(COLS):
                    if new_c1_cleaned[i][j] == 1:
                        found = deepcopy(new_c1_cleaned)
                        found[i][j] = 'C1'
                        possible_moves.append(found)
                    if new_c2_cleaned[i][j] == 1:
                        found = deepcopy(new_c2_cleaned)
                        found[i][j] = 'C2'
                        possible_moves.append(found)

        return possible_moves

    def check_state_diff(self, state1):
        """Compares state with ancestor state"""

        state2 = deepcopy(self.state)
        flag = False
        for i in range(ROWS):
            for j in range(ROWS):
                if state1[i][j] != state2[i][j]:
                    return True
        return flag
