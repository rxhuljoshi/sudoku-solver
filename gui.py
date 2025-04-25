import streamlit as st

def main():
    st.title("Sudoku Solver")
    st.write("Welcome to the Sudoku Solver! Enter your puzzle below and let the solver do the rest.")

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
            solution = solve_sudoku(grid)
            if solution:
                st.success("Sudoku Solved!")
                display_solution(solution)
            else:
                st.error("No solution exists for the given Sudoku.")
        else:
            st.error("Invalid Sudoku grid. Please check your input.")

def is_valid_grid(grid):
    # Validate the grid (e.g., check dimensions, valid numbers)
    return len(grid) == 9 and all(len(row) == 9 for row in grid)

def solve_sudoku(grid):
    # Placeholder for the Sudoku solving logic
    # Replace this with your actual solving algorithm
    return grid  # Return the solved grid (for now, returning the input)

def display_solution(solution):
    st.write("Solved Sudoku:")
    for row in solution:
        st.write(" ".join(str(num) if num != 0 else "." for num in row))

if __name__ == "__main__":
    main()