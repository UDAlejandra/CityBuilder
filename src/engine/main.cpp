/*
Variant: City Builder
Students:Angel Ivan Lopez
Maria Alejandra Ortiz
Jenny Vanesa Leon
*/

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

#include "linked_list.cpp"
#include "tree.cpp"

int main()
{
    ifstream input("../data/input.json");

    if(!input.is_open())
    {
        cout << "Error abriendo input.json" << endl;
        return 1;
    }

    string jsonText;
    string line;

    while(getline(input, line))
    {
        jsonText += line;
    }

    input.close();

    LinkedList adjacencyList;
    BST happinessTree;

    size_t pos = 0;

    while(true)
    {
        size_t namePos = jsonText.find("\"name\":\"", pos);

        if(namePos == string::npos)
            break;

        namePos += 8;

        size_t endName = jsonText.find("\"", namePos);

        string name =
            jsonText.substr(namePos,
                            endName - namePos);

        size_t happinessPos =
            jsonText.find("\"happiness\":", endName);

        happinessPos += 12;

        size_t endHappy =
            jsonText.find("}", happinessPos);

        int happiness =
            stoi(
                jsonText.substr(
                    happinessPos,
                    endHappy - happinessPos
                )
            );

        adjacencyList.insert(name);

        Building b;
        b.name = name;
        b.happiness = happiness;

        happinessTree.insert(b);

        pos = endHappy;
    }

    Building happiest =
        happinessTree.getMax();

    ofstream state("../data/state.json");

    state << "{\n";
    state << "  \"totalBuildings\": "
          << adjacencyList.size()
          << ",\n";

    state << "  \"happiestBuilding\": {\n";
    state << "    \"name\": \""
          << happiest.name
          << "\",\n";

    state << "    \"happiness\": "
          << happiest.happiness
          << "\n";

    state << "  }\n";
    state << "}\n";

    state.close();

    cout << "\n=== BUILDING LIST ===\n";
    adjacencyList.display();

    cout << "\n=== HAPPINESS TREE ===\n";
    happinessTree.print();

    cout << "\nstate.json generado correctamente\n";

    return 0;
}
