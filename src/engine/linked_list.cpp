/*
Variant: City Builder
Students:Angel Ivan Lopez
Maria Alejandra Ortiz
Jenny Vanesa Leon
*/

#include <iostream>
#include <string>

using namespace std;

struct ListNode
{
    string name;
    ListNode *next;

    ListNode(string n)
    {
        name = n;
        next = nullptr;
    }
};

class LinkedList
{
private:
    ListNode *head;

public:
    LinkedList()
    {
        head = nullptr;
    }

    void insert(string name)
    {
        ListNode *newNode = new ListNode(name);

        if (head == nullptr)
        {
            head = newNode;
            return;
        }

        ListNode *temp = head;

        while (temp->next != nullptr)
            temp = temp->next;

        temp->next = newNode;
    }

    int size()
    {
        int count = 0;

        ListNode *temp = head;

        while (temp != nullptr)
        {
            count++;
            temp = temp->next;
        }

        return count;
    }

    void display()
    {
        ListNode *temp = head;

        while (temp != nullptr)
        {
            cout << temp->name << " -> ";
            temp = temp->next;
        }

        cout << "NULL" << endl;
    }
};
