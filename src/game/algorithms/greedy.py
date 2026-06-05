# ==========================================
# Team Number: 3
# Variant Name: Place highest happiness building first
# Student Names: Ivan Lopez, Maria Ortiz, Jenny Leon
# ==========================================

def greedy_algorithm(buildings, rows=8, columns=8):
    scoring_assets = [b for b in buildings if b['happiness'] > 0]
    listBuildings = sorted(scoring_assets, key=lambda x: x['happiness'], reverse=True)


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