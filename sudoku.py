class Sudoku:
    """
    Represents a Sudoku board as a 9x9 2D Matrix.
    """

    def __init__(self):
        self.cells = [(i, j) for j in range(9) for i in range(9)]
        self.board = [[0] * 9 for _ in range(9)]

    def __str__(self):
        sudoku = "\n"
        for row in self.board:
            sudoku += "["
            sudoku += ", ".join(str(cell) for cell in row)
            sudoku += "]\n"
        sudoku += ""

        return sudoku

    def get_rows(self) -> list:
        """
        Returns the rows
        """
        rows = [row for row in self.board]
        return rows

    def get_columns(self) -> list:
        """
        Returns the columns
        """
        rows = self.get_rows()
        columns = []

        for i in range(9):
            column = []
            for row in rows:
                column.append(row[i])
            columns.append(column)

        return columns

    def get_regions(self):
        """
        Returns a valid 3x3 region
        """

        regions = []
        for row_bound in range(0, 9, 3):
            for col_bound in range(0, 9, 3):
                region = []
                for i in range(row_bound, row_bound + 3):
                    for j in range(col_bound, col_bound + 3):
                        region.append(self.board[i][j])
                regions.append(region)

        return regions

    def valid(self, area: list):
        for sub_area in area:
            seen = set()
            for cell in sub_area:
                if cell == 0:
                    continue
                if cell in seen:
                    return False
                seen.add(cell)
        return True

    def is_valid(self):

        return (
            self.valid(self.get_rows())
            and self.valid(self.get_columns())
            and self.valid(self.get_regions())
        )

    def is_solved(self):
        zero_count = 0
        rows = self.get_rows()
        for row in rows:
            zero_count += row.count(0)

        return zero_count == 0 and self.is_valid()

    def get_neighbors(self, cell: tuple) -> set:
        row, col = cell
        neighbors = set()

        # Same row
        for j in range(9):
            if j != col:
                neighbors.add((row, j))

        # Same column
        for i in range(9):
            if i != row:
                neighbors.add((i, col))

        # 3x3 box
        row_start, col_start = 3 * (row // 3), 3 * (col // 3)
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):

                if i == row and j == col:
                    continue

                neighbors.add((i, j))

        return neighbors

    def generate(self, n):
        """
        Generates a Sudoku board with n empty cells
        """
        pass


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
