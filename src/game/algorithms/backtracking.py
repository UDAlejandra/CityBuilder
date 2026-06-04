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

    def valid_position(row, column, nameBuilding):

        """
        
        This function checks if the position is valid for placing a building. It checks if the building is not
        placed next to another building of the same type.
        
        Args:
            row: The row index of the position to check.
            column: The column index of the position to check.
            nameBuilding: The name of the building to place.
        Returns:
            True if the position is valid, False otherwise.   
        """

        if row > 0 and dashboard[row - 1][column] == nameBuilding:
            return False
        
        if column > 0 and dashboard[row][column - 1] == nameBuilding:
            return False
        
        return True
    
    def search_solution(row, column):

        """
        This function implements the backtracking algorithm to find a valid arrangement of buildings on the grid.
        It recursively tries to place each building in the current position and checks if it leads to a valid solution. 
        If a valid solution is found, it returns True; otherwise, it backtracks and tries the
        
        Args:
            row: The current row index to place a building.
            column: The current column index to place a building.  
        Returns:
            True if a valid solution is found, False otherwise.
        """

        if row == rows:

            return True
        
        nextRow = row + (column + 1) // columns
        nextColumn = (column + 1) % columns

        for i in buildings:

            name = i['name']

            if valid_position(row, column, name):
                dashboard[row][column] = name

                if search_solution(nextRow, nextColumn):
                    return True
                
                dashboard[row][column] = "empty"

        return False
    
    if search_solution(0, 0):

        return dashboard
    
    return None