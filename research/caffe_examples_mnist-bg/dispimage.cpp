#include <iostream>
#include <string>
#include <fstream>
#include <iostream>
#include <sstream>
#include <cstdio>
#include <iomanip>
#include <cstdint>

//g++ amattest.cpp -std=c++11

using namespace std;


int main(int argc, char** argv)
{
	if(argc < 2) {
    	cout << "give filename and image num" << endl;
    	return 1;
	}
	
    ifstream fin(argv[1], ios::in|ios::binary);

	stringstream ss;
	ss << argv[2];
	int imgNum = 0;
	ss >> imgNum;

	uint8_t data[785] = {0};
	int pos = imgNum*(28*28+1);
    fin.seekg(pos, ios_base::beg);

	fin.read((char*)data, sizeof(data));

    fin.close();
    
    printf("%idx=d\n", imgNum);
    
    for(int i = 0; i < 28; i++) {
        for(int j = 0; j < 28; j++) {
	    uint8_t val = data[i*28+j];
	      if(val < 0x09) {
			  //val = 0x00;
	      }
	      printf("%02x ", (int)val);
	}
	printf("\n");
    }
    printf("label=0x%02x\n", (int)data[784]);

    return 0;
}
