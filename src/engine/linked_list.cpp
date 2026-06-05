/* ==========================================
   Team Number: 3
   Variant Name: Building adjacency list
   Student Names: Ivan Lopez, Maria Ortiz, Jenny Leon
   ========================================== */



#include <iostream>
#include <string>

using namespace std;

struct ListNode
{
    int neighborCellID;
    ListNode *next;

    ListNode(int id)
    {
        neighborCellID = id;
        next = nullptr;
    }
};

class AdjacencyList
{
private:
    ListNode *head[64];
    int totalElements;

public:
    AdjacencyList()
    {
        totalElements = 0;
        for (int i = 0; i < 64; i++) head[i] = nullptr;
    }

    void addEdge(int u, int v)
    {
        ListNode *newNode = new ListNode(v);
        newNode->next = head[u];
        head[u] = newNode;

        newNode = new ListNode(u);
        newNode->next = head[v];
        head[v] = newNode;
        
        totalElements++;
    }

    bool isAdjacent(int u, int v)
    {
        ListNode *temp = head[u];
        while (temp != nullptr)
        {
            if (temp->neighborCellID == v) return true;
            temp = temp->next;
        }
        return false;
    }

    int size() { return totalElements; }

    ~AdjacencyList()
    {
        for (int i = 0; i < 64; i++)
        {
            ListNode *current = head[i];
            while (current != nullptr)
            {
                ListNode *next = current->next;
                delete current;
                current = next;
            }
        }
    }
};