def backtracking_algorithm(buildings, rows=3, columns=3):
    """
    In this phase of the program, the backtracking algorithm will be used to evaluate the program's
    constraint, which does not allow two buildings of the same type to be placed next to each other.

    Args:
        buildings : This variable contains a list of the building's name and happiness index
        rows :(We are currently using a 3x3 grid.) The path across the board is based on these variables.
        columns :(We are currently using a 3x3 grid.) The path across the board is based on these variables.
    """

    dashboard = [["empty" for _ in range(columns)] for _ in range(rows)]

    def valid_position(row, column, nameBuilding):

        if row > 0 and dashboard[row - 1][columns] == nameBuilding:
            return False
        
        if column > 0 and dashboard[row][column - 1] == nameBuilding:
            return False
        
        return True
    
    def search_solution(row, column):

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