def greedy_algorithm(buildings, rows=8, columns=8):
    """
    In this phase of the code, we use the greedy algorithm to sort the buildings from highest to 
    lowest happiness, filling the “grid” with the options that provide the most happiness 

    Args:
        buildings : This variable contains a list of the building's name and happiness index
        rows : The path across the board is based on these variables.
        columns : The path across the board is based on these variables.
    Returns:
        An arrangement of the buildings on the grid that satisfies the constraints, or None if no solution is found.
    """
    listBuildings = sorted(buildings, key=lambda x: x.happiness, reverse=True)

    dashboard = [["empty" for _ in range(columns)] for _ in range(rows)]

    numBuilding = 0

    for i in range(rows):
        for j in range(columns):

            if numBuilding < len(listBuildings):
                dashboard[i][j] = listBuildings[numBuilding]['name']
                numBuilding += 1

            else:
                dashboard[i][j] = listBuildings[0]['name']
    
    return dashboard
