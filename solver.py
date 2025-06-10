from sudoku import Sudoku
from collections import deque


class SudokuSolver:
    def __init__(self, sudoku: Sudoku):
        """
        Represents a Sudoku as a CSP
        - VARIABLES, X: each one of the 81 cells.
        - Domains: 1-9 for an empty cell, i for a filled cell with i
        - CONSTRAINTS: row, column, and diagonal Validity
        """

        self.sudoku = sudoku
        self.VARIABLES = sudoku.cells
        self.domain = {}
        self.constraints = sudoku.is_valid()
        self.arcs = []
        self.solution = None

        # Assign each variable its domain
        for variable in self.VARIABLES:
            row, col = variable
            # Empty cell
            if self.sudoku.board[row][col] == 0:
                self.domain[variable] = set(i for i in range(1, 10))
            # Filled cell
            else:
                self.domain[variable] = {self.sudoku.board[row][col]}

        # Represent arcs i.e. mapping each variable to its neighbors
        for variable in self.VARIABLES:
            neighbors = sudoku.get_neighbors(variable)
            for neighbor in neighbors:
                self.arcs.append((variable, neighbor))

    def get_domain(self, cell: tuple) -> set:
        return self.domain[cell]

    def REVISE(self, x, y) -> bool:
        domain_X, domain_Y = self.get_domain(x), self.get_domain(y)
        revised = False
        for value in domain_X.copy():
            # Remove any value that violates the constraints
            if not any(y != value for y in domain_Y):
                domain_X.remove(value)
                revised = True

        return revised

    def AC3(self) -> bool:
        queue = deque(self.arcs)

        while queue:
            x, y = queue.popleft()  # Remove first

            if self.REVISE(x, y):
                if len(self.domain[x]) == 0:
                    return False

                neighbors = self.sudoku.get_neighbors(x) - {y}
                for neighbor in neighbors:
                    queue.append((neighbor, x))

        return True

    def BACKTRACKING_SEARCH(self):
        return self.BACKTRACK(dict())

    def is_complete_assignment(self, assignment: dict):
        """
        Checks if an assignment is complete i.e. each cell is mapped to one value and the board is solved.
        """

        temp_sudoku = Sudoku()
        if not assignment:
            return False

        for variable, value in assignment.items():
            row, col = variable

            if len(value) != 1:
                return False

            temp_sudoku.board[row][col] = list(value)[0]

        return temp_sudoku.is_solved()

    def is_value_consistent(self, variable: tuple, value: int, assignment: dict):
        """
        value is not assigned to any of the neighbors
        """
        neighbors = self.sudoku.get_neighbors(variable)

        for neighbor in neighbors:
            if neighbor in assignment:
                if len(assignment[neighbor]) == 1 and value in assignment[neighbor]:
                    return False

        return True

    def BACKTRACK(self, assignment: dict):
        """
        Classical backtrack algorithm
        """

        if self.is_complete_assignment(assignment):
            return assignment

        variable = self.SELECT_UNASSIGNED_VARIABLE(assignment)
        values = self.ORDERED_DOMAIN_VALUES(variable, assignment)

        for value in values:
            if self.is_value_consistent(variable, value, assignment):

                saved_domains = {var: self.get_domain(var) for var in self.VARIABLES}
                self.domain[variable] = {value}
                assignment[variable] = {value}

                if self.INFERENCE():
                    result = self.BACKTRACK(assignment)
                    if result:
                        return result

                # remove {var = value} from assingment
                assignment.pop(variable)

                # Remove assignments
                self.domain = saved_domains

        return False

    def INFERENCE(self):
        """
        calls arc consistency
        """
        return self.AC3()

    def SELECT_UNASSIGNED_VARIABLE(self, assignment):
        mrv_variable = self.MRV(assignment)
        return mrv_variable

    def MRV(self, assignment: dict):
        mrv_count, mrv_variable = float("inf"), None

        for variable in self.VARIABLES:

            if variable in assignment:
                continue

            domain_size = len(self.get_domain(variable))
            if domain_size < mrv_count:
                mrv_count, mrv_variable = domain_size, variable

        return mrv_variable

    def LSV(self, variable, assignment: dict):
        counter = {value: 0 for value in self.get_domain(variable)}

        for var, values in assignment.items():
            for value in values:
                if value in counter:
                    counter[value] += 1

        lcv_sorted = dict(sorted(counter.items(), key=lambda x: x[1]))

        return list(lcv_sorted.keys())

    def DEGREE(self):
        """
        Not applicable in this case as all nodes have the same level of degree = 20
        """
        pass

    def ORDERED_DOMAIN_VALUES(self, variable, assignment: dict):
        values = self.LSV(variable, assignment)
        return values

    def solve(self):
        if not self.sudoku.is_valid():
            print("This algorithm doesn't support invalid Sudoku puzzles.")
            return

        print("Initial Sudoku: \n", self.sudoku, end="\n\n\n")
        if self.AC3() and self.sudoku.is_solved():
            print("Sudoku solved by AC3: \n", self.sudoku, end="")
        else:
            self.BACKTRACKING_SEARCH()
            print("Sudoku solved by BACKTRACKING_SEARCH: ", end="")

        for variable, value in self.domain.items():
            row, col = variable
            self.sudoku.board[row][col] = value.pop()

        print(self.sudoku, end="\n")
