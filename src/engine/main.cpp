#include <iostream>
#include <fstream>

using namespace std;

int main() {

    ofstream state("state.json");

    state << "{\n";
    state << "   \"game\":\"City Builder\",\n";
    state << "   \"status\":\"running\"\n";
    state << "}\n";

    state.close();

    cout << "state.json generado correctamente" << endl;

    return 0;
}
