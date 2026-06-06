/* ==========================================
   Team Number: 3
   Variant Name: main.cpp (Improved JSON Parser)
   Student Names: Ivan Lopez, Maria Ortiz, Jenny Leon
   ========================================== */

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

#include "linked_list.cpp"
#include "tree.cpp"

int main(int argc, char* argv[])
{
    string inputPath = "src/data/input.json";
    string outputPath = "src/data/state.json";

    if (argc >= 3) {
        inputPath = argv[1];
        outputPath = argv[2];
    }

    ifstream input(inputPath);
    if (!input.is_open())
    {
        cout << "Error opening input file at: " << inputPath << endl;
        return 1;
    }

    string jsonText, line;
    while (getline(input, line)) jsonText += line;
    input.close();

    string gridNames[64];
    string gridTypes[64];
    for(int i=0; i<64; i++) {
        gridNames[i] = "empty";
        gridTypes[i] = "empty";
    }

    auto extractArray = [&](string key, string* target) {
        size_t keyPos = jsonText.find("\"" + key + "\"");
        if (keyPos == string::npos) return;
        
        size_t startBracket = jsonText.find("[", keyPos);
        if (startBracket == string::npos) return;
        
        size_t endBracket = jsonText.find("]", startBracket);
        if (endBracket == string::npos) return;
        
        string arrayContent = jsonText.substr(startBracket + 1, endBracket - startBracket - 1);
        int idx = 0;
        size_t pos = 0;
        while (idx < 64) {
            size_t openQ = arrayContent.find("\"", pos);
            if (openQ == string::npos) break;
            size_t closeQ = arrayContent.find("\"", openQ + 1);
            if (closeQ == string::npos) break;
            
            target[idx++] = arrayContent.substr(openQ + 1, closeQ - openQ - 1);
            pos = closeQ + 1;
        }
    };

    extractArray("grid_layout", gridNames);
    extractArray("grid_types", gridTypes);

    AdjacencyList adjacencyGraph;
    BST happinessTree;
    int buildingsDiscovered = 0;

    for (int r = 0; r < 8; r++)
    {
        for (int c = 0; c < 8; c++)
        {
            int currentCell = r * 8 + c;
            if (gridNames[currentCell] != "empty")
            {
                buildingsDiscovered++;
                if (c < 7 && gridNames[currentCell + 1] != "empty")
                    adjacencyGraph.addEdge(currentCell, currentCell + 1);
                if (r < 7 && gridNames[(r + 1) * 8 + c] != "empty")
                    adjacencyGraph.addEdge(currentCell, (r + 1) * 8 + c);
            }
        }
    }

    for (int i = 0; i < 64; i++)
    {
        if (gridNames[i] == "empty") continue;

        Building b;
        b.name = gridNames[i];
        
        if (b.name == "House") b.happiness = 50;
        else if (b.name == "School") b.happiness = 75;
        else if (b.name == "Park") b.happiness = 90;
        else if (b.name == "Hospital") b.happiness = 85;
        else if (b.name == "Factory") b.happiness = -40;
        else if (b.name == "Landfill") b.happiness = -60;
        else b.happiness = 0;

        if (gridTypes[i] == "Residential")
        {
            for (int neighbor = 0; neighbor < 64; neighbor++)
            {
                if (adjacencyGraph.isAdjacent(i, neighbor) && gridTypes[neighbor] == "Industrial")
                {
                    b.happiness -= 50; 
                }
            }
        }
        happinessTree.insert(b);
    }

    Building happiest;
    if (buildingsDiscovered > 0) happiest = happinessTree.getMax();
    else { happiest.name = "None"; happiest.happiness = 0; }

    ofstream state(outputPath);
    state << "{\n";
    state << "  \"totalBuildings\": " << buildingsDiscovered << ",\n";
    state << "  \"happiestBuilding\": {\n";
    state << "    \"name\": \"" << happiest.name << "\",\n";
    state << "    \"happiness\": " << happiest.happiness << "\n";
    state << "  }\n";
    state << "}\n";
    state.close();

    return 0;
}