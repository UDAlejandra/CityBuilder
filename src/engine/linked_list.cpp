#include <iostream>
#include <string>

using namespace std;

struct BuildingNode
{
    string name;
    BuildingNode* next;

    BuildingNode(string n)
    {
        name = n;
        next = nullptr;
    }
};

class LinkedList
{
private:
    BuildingNode* head;

public:

    LinkedList()
    {
        head = nullptr;
    }

    void insert(string name)
    {
        BuildingNode* newNode = new BuildingNode(name);

        if(head == nullptr)
        {
            head = newNode;
            return;
        }

        BuildingNode* temp = head;

        while(temp->next != nullptr)
            temp = temp->next;

        temp->next = newNode;
    }

    int size()
    {
        int count = 0;

        BuildingNode* temp = head;

        while(temp != nullptr)
        {
            count++;
            temp = temp->next;
        }

        return count;
    }

    void display()
    {
        BuildingNode* temp = head;

        while(temp != nullptr)
        {
            cout << temp->name << " -> ";
            temp = temp->next;
        }

        cout << "NULL" << endl;
    }
};
