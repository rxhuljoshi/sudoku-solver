import streamlit as st
import copy

# Local imports
from sudoku_solver import solve_sudoku as backtracking_solve_sudoku
from optimized_solver import solve_optimized

# Wrapper for naming consistency
def optimized_solve_sudoku(board):
    return solve_optimized(board)

# Predefined example puzzles
EXAMPLES = {
    "Easy": [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"]
    ],
    "Medium": [
        [".", ".", "9", "7", "4", "8", ".", ".", "."],
        ["7", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", "2", ".", "1", ".", "9", ".", ".", "."],
        [".", ".", "7", ".", ".", ".", "2", "4", "."],
        [".", "6", "4", ".", "1", ".", "5", "9", "."],
        [".", "9", "8", ".", ".", ".", "3", ".", "."],
        [".", ".", ".", "8", ".", "3", ".", "2", "."],
        [".", ".", ".", ".", ".", ".", ".", ".", "6"],
        [".", ".", ".", "2", "7", "5", "9", ".", "."]
    ],
    "Hard": [
        [".", ".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", "3", ".", "8", "5"],
        [".", ".", "1", ".", "2", ".", ".", ".", "."],
        [".", ".", ".", "5", ".", "7", ".", ".", "."],
        [".", ".", "4", ".", ".", ".", "1", ".", "."],
        [".", "9", ".", ".", ".", ".", ".", ".", "."],
        ["5", ".", ".", ".", ".", ".", ".", "7", "3"],
        [".", ".", "2", ".", "1", ".", ".", ".", "."],
        [".", ".", ".", ".", "4", ".", ".", ".", "9"]
    ]
}

def main():
    st.title("🧩 Sudoku Solver")
    st.write("Welcome! Choose an input method and a solving strategy to crack your puzzle.")

    # Select input mode
    input_mode = st.radio("Input Mode", ("Custom Input", "Use Example Puzzle"))

    # Solver selection
    solver_option = st.radio("Solver", ("Backtracking Solver", "Optimized Solver"), index=0)

    grid = []

    if input_mode == "Use Example Puzzle":
        difficulty = st.selectbox("Select difficulty:", list(EXAMPLES.keys()))
        example = EXAMPLES[difficulty]
        grid = [[int(cell) if cell != "." else 0 for cell in row] for row in example]
        st.write("Loaded Puzzle:")
        display_solution(grid, disabled=True)

    else:
        # Manual grid input
        st.write("Enter Sudoku Grid:")
        for i in range(9):
            row = []
            if i > 0 and i % 3 == 0:
                st.write("")

            cols = st.columns(12, gap="small")
            col_index = 0
            for j in range(9):
                if j > 0 and j % 3 == 0:
                    col_index += 1

                val = cols[col_index].text_input(
                    "",
                    value="",
                    max_chars=1,
                    key=f"cell_{i}_{j}",
                    label_visibility="collapsed"
                )
                row.append(int(val) if val.isdigit() else 0)
                col_index += 1
            grid.append(row)

    if st.button("Solve Sudoku"):
        if is_valid_grid(grid):
            solution = solve_puzzle(grid, solver_option)
            if solution:
                st.success("✅ Sudoku Solved!")
                display_solution(solution)
            else:
                st.error("❌ No solution exists for the given Sudoku.")
        else:
            st.error("⚠️ Invalid grid. Must be 9x9 with numbers 0–9.")

def solve_puzzle(grid, solver_option):
    board = copy.deepcopy(grid)
    if solver_option == "Backtracking Solver":
        return board if backtracking_solve_sudoku(board) else None
    elif solver_option == "Optimized Solver":
        return board if optimized_solve_sudoku(board) else None

def is_valid_grid(grid):
    return len(grid) == 9 and all(len(row) == 9 for row in grid)

def display_solution(solution, disabled=True):
    for i in range(9):
        if i > 0 and i % 3 == 0:
            st.write("")
        cols = st.columns(12, gap="small")
        col_index = 0
        for j in range(9):
            if j > 0 and j % 3 == 0:
                col_index += 1
            cols[col_index].text_input(
                "",
                value=str(solution[i][j]) if solution[i][j] != 0 else "",
                max_chars=1,
                key=f"sol_cell_{i}_{j}_{st.session_state.get('unique_key', 0)}",  # Add a unique identifier
                label_visibility="collapsed",
                disabled=disabled
            )
            col_index += 1

if __name__ == "__main__":
    main()