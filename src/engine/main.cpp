#include <iostream>
#include <fstream>

#include "json.hpp"

using namespace std;
using json = nlohmann::json;

/*
    Se incluyen los otros .cpp
    porque el proyecto no usa headers.
*/
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

    json data;
    input >> data;

    LinkedList adjacencyList;
    BST happinessTree;

    for(auto& building : data["buildings"])
    {
        string name = building["name"];
        int happiness = building["happiness"];

        adjacencyList.insert(name);

        Building b;
        b.name = name;
        b.happiness = happiness;

        happinessTree.insert(b);
    }

    Building happiest = happinessTree.getMax();

    json output;

    output["totalBuildings"] =
        adjacencyList.size();

    output["happiestBuilding"]["name"] =
        happiest.name;

    output["happiestBuilding"]["happiness"] =
        happiest.happiness;

    ofstream state("../data/state.json");

    state << output.dump(4);

    state.close();

    cout << "===== BUILDINGS =====" << endl;
    adjacencyList.display();

    cout << endl;
    cout << "===== BST ORDER =====" << endl;
    happinessTree.print();

    cout << endl;
    cout << "state.json generado correctamente"
         << endl;

    return 0;
}
