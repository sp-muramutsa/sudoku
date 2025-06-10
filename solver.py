from sudoku import Sudoku
from collections import deque


class SudokuSolver:
    def __init__(self, sudoku: Sudoku):
        """
        Represents a Sudoku puzzle as a Constraint Satisfaction Problem (CSP):
        - VARIABLES (X): Each of the 81 cells on the board.
        - DOMAINS: For empty cells, possible values are 1-9; for filled cells, the domain is the assigned value.
        - CONSTRAINTS: Each assigned value must satisfy Sudoku rules:
          * Row constraint: No duplicate numbers in the same row.
          * Column constraint: No duplicate numbers in the same column.
          * Diagonal constraint: No duplicate numbers in any of the nine 3x3 regiond.
        """

        self.sudoku = sudoku
        self.VARIABLES = sudoku.cells
        self.domain = {}
        self.constraints = sudoku.is_valid()
        self.arcs = []
        self.solution = None

        self.create_graph()
        self.enforce_node_consistency()

    def create_graph(self):
        # Represent arcs i.e. mapping each variable to its neighbors
        for variable in self.VARIABLES:
            neighbors = self.sudoku.get_neighbors(variable)
            for neighbor in neighbors:
                self.arcs.append((variable, neighbor))

    def enforce_node_consistency(self):
        # Assign each variable its domain
        for variable in self.VARIABLES:
            row, col = variable
            # Empty cell
            if self.sudoku.board[row][col] == 0:
                self.domain[variable] = set(i for i in range(1, 10))
            # Filled cell
            else:
                self.domain[variable] = {self.sudoku.board[row][col]}

    def get_domain(self, cell: tuple) -> set:
        """Returns the current domain of the given cell (variable)."""
        return self.domain[cell]

    def is_complete_assignment(self, assignment: dict) -> bool:
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

    def is_value_consistent(
        self, variable: tuple, value: int, assignment: dict
    ) -> bool:
        """
        Checks if the value is not assigned to any of the variable's neighbors in the assignment.
        """
        neighbors = self.sudoku.get_neighbors(variable)

        for neighbor in neighbors:
            if neighbor in assignment:
                if len(assignment[neighbor]) == 1 and value in assignment[neighbor]:
                    return False

        return True

    def REVISE(self, x: tuple, y: tuple) -> bool:
        """
        Revise the domain of variable x with respect to variable y.
        Removes values from domain[x] that have no compatible values in domain[y].
        Returns True if domain[x] was revised, False otherwise.
        """
        domain_X, domain_Y = self.get_domain(x), self.get_domain(y)
        revised = False
        for value in domain_X.copy():
            # Remove any value that violates the constraints
            if not any(y != value for y in domain_Y):
                domain_X.remove(value)
                revised = True

        return revised

    def AC3(self) -> bool:
        """
        AC3 algorithm enforcing arc consistency on all arcs.
        Returns True if arc consistency is achieved without empty domains; False otherwise.
        """
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

    def INFERENCE(self) -> bool:
        """
        Performs inference by calling the AC3 algorithm.
        """
        return self.AC3()

    def SELECT_UNASSIGNED_VARIABLE(self, assignment: dict) -> tuple:
        """
        Selects an unassigned variable using MRV heuristic.
        """
        mrv_variable = self.MRV(assignment)
        return mrv_variable

    def MRV(self, assignment: dict) -> tuple:
        """
        Minimum Remaining Values heuristic: selects the variable with the smallest domain.
        """
        mrv_count, mrv_variable = float("inf"), None

        for variable in self.VARIABLES:

            if variable in assignment:
                continue

            domain_size = len(self.get_domain(variable))
            if domain_size < mrv_count:
                mrv_count, mrv_variable = domain_size, variable

        return mrv_variable

    def LSV(self, variable: tuple, assignment: dict) -> list:
        """
        Least Constraining Value heuristic: orders values by how few constraints they impose on neighbors.
        """
        counter = {value: 0 for value in self.get_domain(variable)}

        for var, values in assignment.items():
            for value in values:
                if value in counter:
                    counter[value] += 1

        lcv_sorted = dict(sorted(counter.items(), key=lambda x: x[1]))

        return list(lcv_sorted.keys())

    def DEGREE(self):
        """
        Degree heuristic placeholder.
        Not applicable in this case as all nodes have the same level of degree = 20
        """
        pass

    def ORDERED_DOMAIN_VALUES(self, variable: tuple, assignment: dict) -> list:
        """
        Returns domain values ordered by the LSV heuristic.
        """
        values = self.LSV(variable, assignment)
        return values

    def BACKTRACK(self, assignment: dict):
        """
        Classical backtracking search algorithm.
        Returns a complete assignment if successful, otherwise False.
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

                # remove {var = value} from assignment
                assignment.pop(variable)

                # Restore domains
                self.domain = saved_domains

        return False

    def BACKTRACKING_SEARCH(self):
        """
        Initiates backtracking search with an empty assignment.
        """
        return self.BACKTRACK(dict())

    def solve(self):
        """
        Attempts to solve the Sudoku puzzle using AC3 and backtracking search.
        Prints the solution if found.
        """
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

        self.solution = self.sudoku.board
        print(self.sudoku, end="\n")
