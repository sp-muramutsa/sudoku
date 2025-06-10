class Sudoku:
    """
    Represents a 9x9 Sudoku board as a 2D Matrix.
    """

    def __init__(self) -> None:
        """
        Initializes the Sudoku board with all cells empty (0).
        Also initializes the list of cell coordinates.
        """
        self.cells = [(i, j) for j in range(9) for i in range(9)]
        self.board = [[0] * 9 for _ in range(9)]

    def __str__(self) -> str:
        """
        Returns a string representation of the Sudoku board.
        """
        sudoku = "\n"
        for row in self.board:
            sudoku += "["
            sudoku += ", ".join(str(cell) for cell in row)
            sudoku += "]\n"
        sudoku += ""
        return sudoku

    def get_rows(self) -> list:
        """
        Returns the rows of the Sudoku board as a list of lists.
        """
        rows = [row for row in self.board]
        return rows

    def get_columns(self) -> list:
        """
        Returns the columns of the Sudoku board as a list of lists.
        """
        rows = self.get_rows()
        columns = []

        for i in range(9):
            column = []
            for row in rows:
                column.append(row[i])
            columns.append(column)

        return columns

    def get_regions(self) -> list:
        """
        Returns the 3x3 regions (sub-grids) of the Sudoku board as a list of lists.
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

    def valid(self, area: list) -> bool:
        """
        Checks if the provided list of lists (area) contains no duplicates except 0.
        Returns True if valid, False otherwise.
        """
        for sub_area in area:
            seen = set()
            for cell in sub_area:
                if cell == 0:
                    continue
                if cell in seen:
                    return False
                seen.add(cell)
        return True

    def is_valid(self) -> bool:
        """
        Checks whether the entire Sudoku board is valid by validating
        rows, columns, and 3x3 regions.
        """
        return (
            self.valid(self.get_rows())
            and self.valid(self.get_columns())
            and self.valid(self.get_regions())
        )

    def is_solved(self) -> bool:
        """
        Returns True if the Sudoku board is completely filled with no zeros
        and is valid; False otherwise.
        """
        zero_count = 0
        rows = self.get_rows()
        for row in rows:
            zero_count += row.count(0)

        return zero_count == 0 and self.is_valid()

    def get_neighbors(self, cell: tuple[int, int]) -> set[tuple[int, int]]:
        """
        Returns the set of neighboring cells (row, column, and 3x3 box neighbors)
        for a given cell coordinate (row, col).
        """
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
