# ==========================================
# Team Number: 3
# Variant Name: Valid layout, satisfying zoning rules
# Student Names: Ivan Lopez, Maria Ortiz, Jenny Leon
# ==========================================



def backtracking_algorithm(buildings, rows=8, columns=8):


    """
    In this phase of the program, the backtracking algorithm will be used to evaluate the program's
    constraint, which does not allow two buildings of the same type to be placed next to each other.

    Args:
        buildings : This variable contains a list of the building's name and happiness index
        rows : The path across the board is based on these variables.
        columns :The path across the board is based on these variables.
    Returns:
        An arrangement of the buildings on the grid that satisfies the constraints, or None if no solution is found.
    """
    
    
    dashboard = [["empty" for _ in range(columns)] for _ in range(rows)]

    def valid_position(row, column, asset):
        nameBuilding = asset['name']
        size = asset.get('size', 1)

        if column + size > columns:
            return False

        for step in range(size):
            c_target = column + step
            if dashboard[row][c_target] != "empty":
                return False

            if row > 0 and dashboard[row - 1][c_target] == nameBuilding:
                return False
            if row < rows - 1 and dashboard[row + 1][c_target] == nameBuilding:
                return False
            if c_target > 0 and dashboard[row][c_target - 1] == nameBuilding:
                return False
            if c_target < columns - 1 and dashboard[row][c_target + 1] == nameBuilding:
                return False

        return True

    def search_solution(row, column):
        if row == rows:
            return True
        if column >= columns:
            return search_solution(row + 1, 0)
        if dashboard[row][column] != "empty":
            return search_solution(row, column + 1)

        for asset in buildings:
            if valid_position(row, column, asset):
                size = asset.get('size', 1)
                name = asset['name']

                for step in range(size):
                    dashboard[row][column + step] = name

                if search_solution(row, column + size):
                    return True
                
                for step in range(size):
                    dashboard[row][column + step] = "empty"

        return False

    if search_solution(0, 0):
        return dashboard
    return None