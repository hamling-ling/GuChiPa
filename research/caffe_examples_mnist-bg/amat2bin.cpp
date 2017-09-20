#include <iostream>
#include <string>
#include <fstream>
#include <iostream>
#include <cstdint>
#include <cmath>

//cat orig.amat | sed -e "s/\s\s\s/\\n/g" > nl.txt
//g++ amattest.cpp -std=c++11

using namespace std;

uint8_t float2GrayScale(float fval)
{
  float fscale = fval*255.0;
  uint8_t uval = 0xFF;
  if(fscale > 255.0) {
    uval = 0xFF;
  } else {
    uval = (uint8_t)(0xFF & (int)round(fval*255.0));
  }
  return uval;
}

bool readImage(ifstream& fin, uint8_t data[28*28+1])
{
	int counter = 0;
	float fval = 0.0f;
	while(fin >> fval) {
		//cout << "\"" << fval << "\"" << endl;
		data[counter] = float2GrayScale(fval);
		counter++;
		if(counter == 28*28) {
			break;
		}
	}
	if(fin.eof() && counter > 0) {
		cerr << "unexpected file length line=" << counter << endl;
		return false;
	}
	fin >> fval;
	data[counter] = (uint8_t)fval;
	return true;
}

int main(int argc, char** argv)
{
  	if(argc < 2) {
    	cout << "give input filename and output filename" << endl;
    	return 1;
    }
  
    ifstream fin(argv[1], ios::in);
	ofstream fout(argv[2], ios::out|ios::trunc|ios::binary);

	while(!fin.eof()) {
		uint8_t data[28*28+1] = {0};
		if(!readImage(fin, data)) {
			cerr << "error" << endl;
			return 1;
		}
		fout.write((const char*)data, sizeof(data));
	}

    fin.close();
    fout.close();
    
    return 0;
}
