/*
Variant: City Builder
Students:Angel Ivan Lopez
Maria Alejandra Ortiz
Jenny Vanesa Leon
*/
#include <iostream>
#include <string>

using namespace std;

struct Building
{
    string name;
    int happiness;
};

struct TreeNode
{
    Building data;
    TreeNode* left;
    TreeNode* right;

    TreeNode(Building b)
    {
        data = b;
        left = nullptr;
        right = nullptr;
    }
};

class BST
{
private:

    TreeNode* root;

    TreeNode* insert(TreeNode* node, Building b)
    {
        if(node == nullptr)
            return new TreeNode(b);

        if(b.happiness < node->data.happiness)
            node->left = insert(node->left, b);
        else
            node->right = insert(node->right, b);

        return node;
    }

    void inorder(TreeNode* node)
    {
        if(node == nullptr)
            return;

        inorder(node->left);

        cout
            << node->data.name
            << " ("
            << node->data.happiness
            << ")"
            << endl;

        inorder(node->right);
    }

public:

    BST()
    {
        root = nullptr;
    }

    void insert(Building b)
    {
        root = insert(root, b);
    }

    void print()
    {
        inorder(root);
    }

    Building getMax()
    {
        TreeNode* temp = root;

        while(temp->right != nullptr)
            temp = temp->right;

        return temp->data;
    }
};
