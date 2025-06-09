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
        self.assignment = dict()

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
            x, y = queue.popleft() # Remove first

            if self.REVISE(x, y):
                if len(self.domain[x]) == 0:
                    return False
                
                neighhors = self.sudoku.get_neighbors(x) - {y}
                for neighbor in neighhors:
                    queue.append((neighbor, x))
        
        return True
    
    def BACKTRACKING_SEARCH(self):
        return self.BACKTRACK() # Initially an empty dict

    def complete_assignment(assignment: dict):
        for variable, value in assignment:
                row, col = variable
                self.sudoku.board[row][col] = value.pop()

    # def BACKTRACK(self, assignment: dict):
    #     if self.complete_assignment()

    # def SELECT_UNASSIGNED_VARIABLE(self):
    #     pass

    # def ORDER_DOMAIN_VALUES(self):
    #     pass

    # def INFERENCE(self):
    #     pass

    # def DEGREE(self):
    #     pass NOT APPLICABLE HERE BECAUSE ALL ARCS HAVE THE SAME NUMBER OF DEGREE = 20

    # def MRV(self):
    #     pass

    # def LSV(self):
    #     pass


    
    def solve(self):
        print("Initial Sudoku: \n", self.sudoku, end="\n\n\n")
        if self.AC3():
            for variable, value in self.domain.items():
                row, col = variable
                self.sudoku.board[row][col] = value.pop()
            
            print("Solved Sudoku: \n", self.sudoku, end="\n")
         
        



s = Sudoku()
s.board = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 3, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0],
]

x = SudokuSolver(s)
x.solve()
