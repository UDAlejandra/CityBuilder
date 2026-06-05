/* ==========================================
   Team Number: 3
   Variant Name: main.cpp (Robust Paths)
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
    // Fallback default paths if no arguments are passed
    string inputPath = "../data/input.json";
    string outputPath = "../data/state.json";

    // If Python sends us explicit target paths, use them instead!
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

    size_t nameArrayPos = jsonText.find("\"grid_layout\"");
    if (nameArrayPos != string::npos)
    {
        int idx = 0;
        size_t searchPos = nameArrayPos;
        while (idx < 64)
        {
            size_t openQ = jsonText.find("\"", searchPos + 1);
            if (openQ == string::npos) break;
            size_t closeQ = jsonText.find("\"", openQ + 1);
            string val = jsonText.substr(openQ + 1, closeQ - openQ - 1);
            
            if (val != "grid_layout" && val != "buildings" && val != "grid_types") {
                gridNames[idx] = val;
                idx++;
            }
            searchPos = closeQ;
        }
    }

    size_t typeArrayPos = jsonText.find("\"grid_types\"");
    if (typeArrayPos != string::npos)
    {
        int idx = 0;
        size_t searchPos = typeArrayPos;
        while (idx < 64)
        {
            size_t openQ = jsonText.find("\"", searchPos + 1);
            if (openQ == string::npos) break;
            size_t closeQ = jsonText.find("\"", openQ + 1);
            string val = jsonText.substr(openQ + 1, closeQ - openQ - 1);
            
            if (val != "grid_types" && val != "empty" && val != "Residential" && val != "Commercial" && val != "Industrial") {
                searchPos = closeQ;
                continue;
            }
            gridTypes[idx] = val;
            idx++;
            searchPos = closeQ;
        }
    }

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