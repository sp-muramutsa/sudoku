# AI Sudoku Solver - Constraint Satisfaction Problem (CSP) Approach

## Overview

This project implements a Sudoku puzzle solver using Constraint Satisfaction Problem (CSP) techniques, combining **AC-3 arc consistency algorithm** with **backtracking search** enhanced by heuristics such as Minimum Remaining Values (MRV) and Least Constraining Value (LCV). The solver efficiently handles standard 9x9 Sudoku boards and guarantees correctness by enforcing the core Sudoku constraints: row, column, and 3x3 box validity.

The core classes are:

* `Sudoku`: Represents the Sudoku board as a 9x9 matrix with methods to validate the puzzle state and identify neighbor relationships.
* `SudokuSolver`: Models Sudoku as a CSP and provides algorithms to solve the puzzle using AC-3 and backtracking search.

---

## Features

* **CSP Modeling:**
  Each cell is treated as a variable with a domain of possible values (1-9). Pre-filled cells have fixed domains of one value.

* **Constraints:**
  Enforces classic Sudoku constraints where no digit can repeat in the same row, column, or 3x3 sub-grid.

* **Arc Consistency (AC-3):**
  Prunes domains by iteratively enforcing consistency across arcs (variable pairs), reducing the search space.

* **Backtracking Search:**
  Recursive search that tries assigning values to unassigned cells, combined with inference to maintain arc consistency.

* **Heuristics:**

  * **MRV (Minimum Remaining Values):** Selects the next variable with the fewest legal values to reduce branching factor.
  * **LCV (Least Constraining Value):** Orders values to assign those that constrain neighbors the least, improving search efficiency.

* **Validity Checks:**
  Functions to verify partial or complete validity of the board at any stage.

---

## Installation and Setup

1. **Python Version:**
   The code is compatible with Python 3.8+.

2. **Dependencies:**
   Only Python standard libraries. No external dependencies are required.

3. **Project Structure:**

```
/sudoku_solver
  ├── sudoku.py        # Contains Sudoku board representation and validation
  ├── solver.py        # Contains SudokuSolver CSP and solving logic
  └── README.md        # This documentation
```

---

## Usage
See ```runner.py```

---

## Reference
> Russell, S., & Norvig, P. (2009). *Artificial Intelligence: A Modern Approach* (3rd ed.). Pearson.
>
> * **Chapter 6**: Constraint Satisfaction Problems
---

Would you like me to help you embed this reference inside your code docstrings or in the README?

---

## Contributing
Contributions for performance improvements, GUI integration, or support for variant puzzles (e.g., Sudoku-X with diagonal constraints) are welcome. Please fork the repository, create a feature branch, and submit a pull request.

---


## Contact
For questions or collaboration inquiries, please contact:

**Author:** Sandrin Muramutsa


