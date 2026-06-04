/* ==========================================
   Team Number: 3
   Variant Name: main.cpp
   Student Names: Ivan Lopez, Maria Ortiz, Jenny Leon
   ========================================== */


#include <iostream>
#include <fstream>
#include <string>

using namespace std;

#include "linked_list.cpp"
#include "tree.cpp"

int main()
{
    ifstream input("../data/input.json");

    if (!input.is_open())
    {
        cout << "Error abriendo input.json" << endl;
        return 1;
    }

    string jsonText;
    string line;

    while (getline(input, line))
    {
        jsonText += line;
    }

    input.close();

    LinkedList adjacencyList;
    BST happinessTree;

    size_t pos = 0;

    while (true)
    {
        size_t namePos = jsonText.find("\"name\"", pos);

        if (namePos == string::npos)
            break;

        size_t colonPos = jsonText.find(":", namePos);
        size_t firstQuote = jsonText.find("\"", colonPos + 1);
        size_t secondQuote = jsonText.find("\"", firstQuote + 1);

        string name = jsonText.substr(
            firstQuote + 1,
            secondQuote - firstQuote - 1);

        size_t happinessPos =
            jsonText.find("\"happiness\"", secondQuote);

        if (happinessPos == string::npos)
            break;

        size_t happinessColon =
            jsonText.find(":", happinessPos);

        size_t happinessEnd =
            jsonText.find_first_of(",}", happinessColon);

        string happinessStr =
            jsonText.substr(
                happinessColon + 1,
                happinessEnd - happinessColon - 1);

        int happiness = stoi(happinessStr);

        adjacencyList.insert(name);

        Building b;
        b.name = name;
        b.happiness = happiness;

        happinessTree.insert(b);

        pos = happinessEnd;
    }

    cout << "Total edificios: "
         << adjacencyList.size()
         << endl;

    if (adjacencyList.size() == 0)
    {
        cout << "No se encontraron edificios en input.json" << endl;
        return 1;
    }

    Building happiest = happinessTree.getMax();

    ofstream state("../data/state.json");

    if (!state.is_open())
    {
        cout << "Error creando state.json" << endl;
        return 1;
    }

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