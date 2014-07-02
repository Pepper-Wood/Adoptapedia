// This code is a really simple modification of the original add_groups code that edits the INPUT.txt
// file and transforms it into a list of icons to be clicked on within the admin area to post messages
// alerting them of their addition.



// the basis for the program will be reading in line input from .txt documents
// and then modifying output text documents as opposed to reading in lines from
// an excel spreadsheet

// PROCESS
// 0) convert the category text documents into category vectors
// 1) convert input text document to a vector of strings ((use a prompter for this))
//		create spotlight variable
// 2) cycle through input vector
//		- if string.length > 1 (as in, not a category)
//			set string.length as spotlight
//		- elif string.length == 1 (as in, category)
//			append spotlight to the designated category vector
//		continue advancing until you reach the end of the input vector
// 3) cycle through each category vector to modify the text documents ((set this to one function
//	  and simply have it read in the names of the categories

// DIRECTORY OF TEXT DOCUMENTS
 // Raw text documents for inputs
  // INPUT.txt - file that stores the information for new groups to be added
  // ALL.txt - file that stores the information of all the groups already stored
 // Formatted text documents for outputs
  // all_text.txt - All Adoptable Groups
  // all_accepted.txt - Groups that accept all types of adopts
  // species.txt - Species Specific Groups
  // fandom.txt - Fandom Specific Groups
  // payment.txt - Payment Specific Groups
  // quality.txt - Groups with a Quality Filter
  // bases.txt - Groups for Adoptable Bases
  // agencies.txt - Adoption Agencies

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <iomanip>
#include <cmath>
#include <algorithm>
#include <string>
#include <map>
#include <utility>
#include <cctype>

typedef std::map<std::string, std::vector<int> > adoptapedicmap;
// within the program, the overarching one will be referred to as a_map
typedef std::map<std::string, std::vector<int> >::iterator a_map_it;
// iterator to be used when cycling through the map to determine 

// --------------------------------------------------------------------------------
// I wasn't able to get atoi to work for the moment, so I made my own quick
// helper function instead.
int convert_str_to_int(const std::string &input) {
	if (input == "0") {
		return 0;
	} else if (input == "1") {
		return 1;
	} else if (input == "2") {
		return 2;
	} else if (input == "3") {
		return 3;
	} else if (input == "4") {
		return 4;
	} else if (input == "5") {
		return 5;
	} else if (input == "6") {
		return 6;
	} else if (input == "7") {
		return 7;
	} else if (input == "8") {
		return 8;
	} else if (input == "9") {
		return 9;
	}
}

// --------------------------------------------------------------------------------
// Add a new group to the adoptapedic map
void add(adoptapedicmap &a_map, const std::string &spotlight) {
	std::vector<int> zero_vector;
	zero_vector.push_back(0); // this will be used as the default vector setting when groups are installed
	a_map.insert(std::make_pair<std::string,std::vector<int> >(spotlight, zero_vector));
}

// --------------------------------------------------------------------------------
// Read in text document and transform into vector of strings
void read_words(adoptapedicmap &a_map, std::ifstream & text_str) {
	std::string x; // input variable
	std::string spotlight; // this stores the group name being processed while it's being added to categories
	int num; // used for itoa conversion
	while (text_str >> x) {
		if (x.size() > 1) { // if the input is a word
			spotlight = x; // set spotlight as x
			for (int i=0; spotlight[i]; i++) spotlight[i] = tolower(spotlight[i]); // make the word all lower case
			// don't insert it only if the word already exists, but have it remain as spotlight in the event that categories are to be edited
			if (a_map.find(spotlight)!=a_map.end()) { //duplicate not found
				add(a_map, spotlight); // add it to a_map 
			} // don't do anything if duplicate is found
		} else if (x.size() == 1) { // if the input is a number rather than a word
			// convert to int and append this number to the spotlight's vector if it doesn't exist prior
			// int num = std::atoi(x);
			int num = convert_str_to_int(x);
			if (std::find((a_map.find(spotlight)->second).begin(), (a_map.find(spotlight)->second).end(), num)==(a_map.find(spotlight)->second).end()) { // duplicate not found
				a_map[spotlight].push_back(num);
				//((a_map.find(spotlight))->second).push_back(num); // add on the new directory that the group will be a part of
			}
		}
	}
}

// --------------------------------------------------------------------------------
// rewrite journal file to its respective .txt document.
void write_to_notification_list(adoptapedicmap &a_map, std::ofstream &out_str) {
	for (a_map_it iterator = a_map.begin(); iterator != a_map.end(); iterator++) {
		// just go ahead and print everything
		out_str << ":icon" << iterator->first << ":" << std::endl;
	}
}

// ================================================================================
int main(int argc, char* argv[]) {
	adoptapedicmap a_map;
	
	// INPUT.txt - file that stores the information for new groups to be added
	// open INPUT.txt and read it into a_map as well, thereby combinging the two
	std::ifstream input_str("00-INPUT.txt");
	if (!input_str.good()) {
		std::cerr << "Could not open INPUT.txt to read\n";
		return 1;
	}
	read_words(a_map, input_str);
	
	// open up NOTIFICATIONS.txt so that it can be rewritten with the combined text
	std::ofstream n_str("00-NOTIFICATIONS.txt");
	if (n_str.is_open()) {
		write_to_notification_list(a_map, n_str);
	} else { return 0; }
	
	std::cout << "Notification list updated." << std::endl;
}
