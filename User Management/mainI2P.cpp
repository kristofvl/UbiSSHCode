#include <iostream>
#include "I2P.h"

using namespace std;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Please specify a CSV file." << endl;
        return 1;
    }
    string filename = argv[1];
    int function;
    cout << "For adding Users press 1" << endl;
    cout << "For deleting Users press 2" << endl;
    cin >> function;
    UserManager userManager;
    userManager.ManageUsers(filename, function);
    return 0;
}
