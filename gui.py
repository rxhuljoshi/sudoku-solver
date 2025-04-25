import streamlit as st
# Import from local Python files
from sudoku_solver import solve_sudoku as backtracking_solve_sudoku
from optimized_solver import optimized_solve_sudoku
import time

def main():
    st.title("Sudoku Solver")
    st.write("Welcome to the Sudoku Solver! Enter your puzzle below and let the solver do the rest.")

    # Add a feature to select the solver
    solver_option = st.radio(
        "Select the solver to use:",
        ("Backtracking Solver", "Optimized Solver"),
        index=0
    )

    # Create a 9x9 grid for Sudoku input with 3x3 subgrid formatting
    grid = []
    for i in range(9):
        row = []
        # Add vertical spacing between 3x3 subgrids
        if i > 0 and i % 3 == 0:
            st.write("")  # Add a blank line for spacing

        cols = st.columns(12, gap="small")  # Adjust to accommodate extra spacing columns
        col_index = 0
        for j in range(9):
            # Add horizontal spacing between 3x3 subgrids
            if j > 0 and j % 3 == 0:
                col_index += 1  # Skip a column for spacing

            # Create a text input for each cell
            cell = cols[col_index].text_input(
                "",
                value="",
                max_chars=1,
                key=f"cell_{i}_{j}",
                label_visibility="collapsed",
                help=None
            )
            row.append(int(cell) if cell.isdigit() else 0)
            col_index += 1
        grid.append(row)

    if st.button("Solve Sudoku"):
        if is_valid_grid(grid):
            solution = solve_puzzle(grid, solver_option)
            if solution:
                st.success("Sudoku Solved!")
                display_solution(solution)
            else:
                st.error("No solution exists for the given Sudoku.")
        else:
            st.error("Invalid Sudoku grid. Please check your input.")

def solve_puzzle(grid, solver_option):
    if solver_option == "Backtracking Solver":
        return backtracking_solve_sudoku(grid)
    elif solver_option == "Optimized Solver":
        return optimized_solve_sudoku(grid)

def is_valid_grid(grid):
    # Validate the grid (e.g., check dimensions, valid numbers)
    return len(grid) == 9 and all(len(row) == 9 for row in grid)

def display_solution(solution):
    for i in range(9):
        if i > 0 and i % 3 == 0:
            st.write("")  # Blank line for spacing between subgrids
        cols = st.columns(12, gap="small")
        col_index = 0
        for j in range(9):
            if j > 0 and j % 3 == 0:
                col_index += 1  # Skip a column for spacing
            # Ensure unique key using row and column indices, and a timestamp
            key = f"sol_cell_{i}_{j}_{int(time.time() * 1000)}"
            cols[col_index].text_input(
                "",
                value=str(solution[i][j]) if solution[i][j] != 0 else "",
                max_chars=1,
                key=key,  # Ensures unique key for each input
                label_visibility="collapsed",
                disabled=True
            )
            col_index += 1

if __name__ == "__main__":
    main()