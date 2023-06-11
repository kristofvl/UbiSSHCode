// I2P.cpp
#include "I2P.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <ctime>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

using namespace std;

UserManager::UserManager() {}

int UserManager::GetMatNum(const string& s) {
    stringstream str_strm;
	str_strm << s; // conert the string s into stringstream
	string temp_str; // make temporary string type variable
	int temp_int; // make temporary integer type variable
	int output = 0;
	while(!str_strm.eof()) {
		temp_str = ""; // clear temp string
		str_strm >> temp_str; // take words to temp_str one b one
		if(stringstream(temp_str) >> temp_int) { // try to convert string
		// since matriculation numbers consist 7 digits, we need to eliminate all other numbers
			if(temp_int >=1000000) { 
				//cout << temp_int << " "; // prints out the matriculation number
				output = temp_int; // puts the matriculation number in output
			}
		}
	}
	return output;
}

int UserManager::GetYear(const string& filename) {
    ifstream in(filename); // Open CSV file for reading
	string s;
	getline(in, s);	// takes the first line, copies it to s string
	int end = size(s);
	for(int i=0; i <= end; i++) { 
		if(s[i] == ',') {  // conert all commas to spaces so the matnumbers get seperated from words
			s[i] = ' ';
		}
	}

	// code started here
	stringstream str_strm;
	str_strm << s; // conert the string s into stringstream
	string temp_str; // make temporary string type variable
	int temp_int; // make temporary integer type variable
	int output = 0;
	while(!str_strm.eof()) {
		temp_str = ""; // clear temp string
		str_strm >> temp_str; // take words to temp_str one b one
		if(stringstream(temp_str) >> temp_int) { // try to convert string
		// since matriculation numbers consist 7 digits, we need to eliminate all other numbers
			if(temp_int >= 2000 && temp_int <= 2500) { 
				//cout << temp_int << " "; // prints out the matriculation number
				output = temp_int; // puts the matriculation number in output
			}
		}
	}
	return output;
}

string UserManager::PassGen() {
    const char alphanum[] = "0123456789!@#%^*abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
	int string_length = sizeof(alphanum)-1;
    	int n = 7;	// password size
    	char Password[n];
    	srand(clock());
    	repeat:
    	for(int i = 0; i < n; i++) {	// Generate Password
    		Password[i] = alphanum[rand() % string_length];
    		if(Password[0] == '#') {
    			goto repeat;
    		}
    	}
    	return Password;
}

void UserManager::TakeCSV(const string& filename) {
    ifstream in(filename); // Open CSV file for reading
	string s;
	// reads line by line in CSV file and put them in string s
	while(getline(in, s)) {	// while there is still line in the csv file, it takes the line and copies to string s
		int end = size(s);
		for(int i=0; i <= end; i++) { 
			if(s[i] == ',') {  // conert all commas to spaces so the matnumbers get seperated from words
				s[i] = ' ';
			}
		}
		// see if there is a matriculation number in that line
		// if matriculation number is present in a line, put in in an array
		int a = GetMatNum(s);
		if(a != 0) {
			MatNums.push_back(to_string (a));
		}
	}
}

void UserManager::CreateLinuxUser(const string& USERNAME, const string& PASSWORD, const string& YEAR) {
    cout << "Username: " << "st" << YEAR << "_" << USERNAME << endl;
	cout << "Password: " << PASSWORD << endl;
	char command[100];	// character array to put in system function
	string stgrp = "sudo groupadd -f student";	// add student group to groups
	strcpy(command, stgrp.c_str());	// convert string to character array and then copy to command character array
	system(command);	// run the code written into character array
	string createuser = "sudo useradd -m -p $(openssl passwd -1 " + PASSWORD + ") " + "st" + YEAR + "_" + USERNAME;
	strcpy(command, createuser.c_str());
	system(command);
	cout << endl;
}

void UserManager::DeleteLinuxUser(const string& USERNAME, const string& YEAR) {
    char command[100];	// character array to put in system function
	string deleteuser = "sudo userdel -r st" + YEAR + "_" + USERNAME;	// string with the deleting command
	strcpy(command, deleteuser.c_str());	// copy string to array of characters
	system(command);	// run the array of characters as a shell command
	cout << "User " << "st" << YEAR << "_" << USERNAME << " deleted" << endl;	// output comment
}

void UserManager::ManageUsers(const string& filename, int function) {
    string year = to_string(GetYear(filename));
    TakeCSV(filename);
    if (function == 1) {
        for (int i = 0; i < MatNums.size(); i++) {
            CreateLinuxUser(MatNums[i], PassGen(), year);
        }
    } else if (function == 2) {
        for (int i = 0; i < 20; i++) {
            DeleteLinuxUser(MatNums[i], year);
        }
    } else {
        cout << "Invalid input" << endl;
    }
}
