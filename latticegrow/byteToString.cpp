#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

typedef unsigned char BYTE;

int main() {
    // Open the file in binary mode and seek to the end to get size
    ifstream file("testGauge1", ios::binary | ios::ate);
    if (!file.is_open()) {
        cerr << "Error opening file" << endl;
        return 1;
    }

    streamsize fileSize = file.tellg();
    file.seekg(0, ios::beg);

    // Vector automatically manages memory allocation and cleanup
    vector<BYTE> byteArray(fileSize);
    if (file.read((char*)byteArray.data(), fileSize)) {
        cout << "Successfully read " << fileSize << " bytes." << endl;
    }

    return 0;
}