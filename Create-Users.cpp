/*
Author: Alireza Yazdani
Description:
	this program takes a CSV file as its input and then seperates the matriculation numbers and then creates linux users with these matriculation numbers

Program Algrythm:
	1-Take CSV file as an input
	2-Take out matriculation numbers
	3-Put the Matricuation numbers in an array
	4-Write Them To A Bash Script File With Code For Creating User And Password👎️
		the bash code should be in the program
*/
#include <iostream>	// required for taking input from user and giving output message
#include <stdio.h>	// required for bash script
#include <stdlib.h>	// required for bash script
#include <string.h>	// required for string type
#include <fstream>	// required for opening a file for reading and writing
#include <sstream>	// required to take out numbers from a string
#include <ctime>	// for password generator function
/*
using std::cout;
using std::cin;
using std::endl;
using std::string;
using std::ifstream;
using std::ofstream;
*/
using namespace std; // instead of all above we can use this


// GLOBAL VARIABLES START HERE
string MatNums[20]; // array of matriculation numbers
// GLOBAL VARIABLES END HERE


// FUNCTIONS START HERE
// ---------------------
// take out matriculation numbers
int GetMatNum(string s) {
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

// take out year
int GetYear() {
	ifstream in("read.csv"); // Open CSV file for reading
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

// create random password
string PassGen() {
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
// to take CSV file, seperate matriculation numbers and put it in a string array
void takeCSV() {
	ifstream in("read.csv"); // Open CSV file for reading
	string s;
	// reads line by line in CSV file and put them in string s
	int loopcounter = 0;
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
			MatNums[loopcounter] = to_string (a);
			loopcounter++;
		}
	}
}


// to create users in linux using shell command
void CrUse(string USERNAME, string PASSWORD, string YEAR) {
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

// to delete created users
void UserDel(string USERNAME, string YEAR) {
	char command[100];	// character array to put in system function
	string deleteuser = "sudo userdel -r st" + YEAR + "_" + USERNAME;	// string with the deleting command
	strcpy(command, deleteuser.c_str());	// copy string to array of characters
	system(command);	// run the array of characters as a shell command
	cout << "User " << "st" << YEAR << "_" << USERNAME << " deleted" << endl;	// output comment
}

// ------------------
// FUNCTIONS END HERE

int main() {
	string year = to_string(GetYear());
	int function;
	// get CSV file and take out Matriculation Numbers
	takeCSV(); // takes CSV file, seperates matriculation numbers, put them in an array
	cout << "For adding Users press 1" << endl;
	cout << "For deleting Users press 2" << endl;
	cin >> function;
	if(function == 1) {
		for (int i = 0; i<20; i++) {
			CrUse(MatNums[i], PassGen(), year);
		}
	}else if(function == 2) {
		for (int i = 0; i<20; i++) {
			UserDel(MatNums[i], year);
		}
	}else {
		cout << "invalid input" << endl;
	}

	return 0;
}
