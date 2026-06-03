/* ==========================================
   Team Number: 3
   Variant Name: Happiness score tree (BST)
   Student Names: Ivan Lopez, Maria Ortiz, Jenny Leon
   ========================================== */

#include <iostream>
#include <string>

using namespace std;

struct Building {

    string name;
    int happiness;
};

struct TreeNode {

    Building data;
    TreeNode* left;
    TreeNode* right;
};

class BST {

private:

    TreeNode* root;

    TreeNode* insert(TreeNode* node, Building b) {

        if(node == nullptr) {

            TreeNode* newNode = new TreeNode;

            newNode->data = b;
            newNode->left = nullptr;
            newNode->right = nullptr;

            return newNode;
        }

        if(b.happiness < node->data.happiness)
            node->left = insert(node->left, b);
        else
            node->right = insert(node->right, b);

        return node;
    }

    void inorder(TreeNode* node) {

        if(node == nullptr)
            return;

        inorder(node->left);

        cout
            << node->data.name
            << " "
            << node->data.happiness
            << endl;

        inorder(node->right);
    }

public:

    BST() {
        root = nullptr;
    }

    void insert(Building b) {
        root = insert(root, b);
    }

    void print() {
        inorder(root);
    }
};
