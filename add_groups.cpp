// The basis for the program will be reading in line input from .txt documents
// and then modifying output text documents as opposed to reading in lines from
// an excel spreadsheet

// DIRECTORY OF TEXT DOCUMENTS
 // Raw text documents for inputs
  // 00-INPUT.txt - file that stores the information for new groups to be added
  // 00-ALL.txt - file that stores the information of all the groups already stored
 // Formatted text documents for outputs
  // 0-all_text.txt - All Adoptable Groups
  // 1-all_accepted.txt - Groups that accept all types of adopts
  // 2-species.txt - Species Specific Groups
  // 3-fandom.txt - Fandom Specific Groups
  // 4-payment.txt - Payment Specific Groups
  // 5-quality.txt - Groups with a Quality Filter
  // 6-bases.txt - Groups for Adoptable Bases
  // 7-agencies.txt - Adoption Agencies

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
#include <set>

typedef std::map<std::string, std::vector<int> > adoptapedicmap;
// within the program, the overarching one will be referred to as a_map
typedef std::map<std::string, std::vector<int> >::iterator a_map_it;
// iterator to be used when cycling through the map

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
// returns true if a duplicate is found and false if the spotlight isn't already in a_map
bool duplicate_found(adoptapedicmap &a_map, const std::string &spotlight) {
	for (a_map_it iterator = a_map.begin(); iterator != a_map.end(); iterator++) {
		// iterator->first = group name
		if ((iterator->first) == spotlight) {
			return true;
		}
	}
	return false;
}

// --------------------------------------------------------------------------------
// Add a new group to the adoptapedic map
void add(adoptapedicmap &a_map, const std::string &spotlight) {
	std::vector<int> zero_vector;
	// zero_vector.push_back(0); // this will be used as the default vector setting when groups are installed
	a_map.insert(std::pair<std::string,std::vector<int> >(spotlight, zero_vector));
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
			for (int i=0; spotlight[i]; i++) {
				spotlight[i] = tolower(spotlight[i]); // make the word all lower case
			}
			// don't insert it only if the word already exists, but have it remain as spotlight in the event that categories are to be edited
			if (!duplicate_found(a_map, spotlight)) { //duplicate not found
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
// Separate read_words function to account for the separate 00-NOTIFICATIONS.txt document
void read_words_input(adoptapedicmap &a_map, std::set<std::string> &notifications, std::ifstream & text_str) {
	std::string x; // input variable
	std::string spotlight; // this stores the group name being processed while it's being added to categories
	int num; // used for itoa conversion
	while (text_str >> x) {
		if (x.size() > 1) { // if the input is a word
			spotlight = x; // set spotlight as x
			for (int i=0; spotlight[i]; i++) spotlight[i] = tolower(spotlight[i]); // make the word all lower case
			// don't insert it only if the word already exists, but have it remain as spotlight in the event that categories are to be edited
			if (!duplicate_found(a_map, spotlight)) { //duplicate not found
				add(a_map, spotlight); // add it to a_map
				notifications.insert(spotlight); // add it to the notifications set
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
void write_to_ALL(adoptapedicmap &a_map, std::ofstream &out_str) {
	for (a_map_it iterator = a_map.begin(); iterator != a_map.end(); iterator++) {
		// iterator->first = group name
		out_str << iterator->first;
		// iterator->second = vector of ints for categories
		for (unsigned int i=0; i<(iterator->second).size(); i++) { // print out categories except for the 0
			out_str << " " << (iterator->second)[i];
		}
		out_str << "\n";
	}
}

// --------------------------------------------------------------------------------
// rewrite journal files to their respective .txt documents. Note, I personally find this method
// to be inefficient because it only lets me take in one output stream at a time and have to cycle
// through the map each time, resulting in O(klog(n)) runtime with k as the number of output documents
// and n as the number of elements stored in the map. At the moment, that runtime is at 22.
void write_to_complete_list(adoptapedicmap &a_map, std::ofstream &out_str) {
	for (a_map_it iterator = a_map.begin(); iterator != a_map.end(); iterator++) {
		// just go ahead and print everything
		out_str << ":icon" << iterator->first << ": :dev" << iterator->first << ":" << std::endl;
	}
}

// --------------------------------------------------------------------------------
// rewrite journal files to their respective .txt documents. Note, I personally find this method
// to be inefficient because it only lets me take in one output stream at a time and have to cycle
// through the map each time, resulting in O(klog(n)) runtime with k as the number of output documents
// and n as the number of elements stored in the map. At the moment, that runtime is at 22.
void write_to_txt(adoptapedicmap &a_map, std::ofstream &out_str, const int & category_num) {
	for (a_map_it iterator = a_map.begin(); iterator != a_map.end(); iterator++) {
		// check if the examined group belongs in the specified category
		if ((std::find(iterator->second.begin(), iterator->second.end(), category_num))!=iterator->second.end()) {
			out_str << ":icon" << iterator->first << ": :dev" << iterator->first << ":" << std::endl;
		}
	}
}

// --------------------------------------------------------------------------------
// Specific write function for the notification set.
void write_to_notification_list(std::set<std::string> &notifications, std::ofstream &out_str) {
	for (std::set<std::string>::iterator iterator = notifications.begin(); iterator != notifications.end(); iterator++) {
		out_str << ":icon" << *iterator << ":" << std::endl;
	}
}

// ================================================================================
int main(int argc, char* argv[]) {
	adoptapedicmap a_map;
	
	// ALL.txt - file that stores the information of all the groups already stored
	// open ALL.txt and read into a_map
	std::ifstream all_str("00-ALL.txt");
	
	if (!all_str.good()) {
		std::cerr << "Could not open 00-ALL.txt to read\n";
		return 1;
	}
	read_words(a_map, all_str);
	std::set<std::string> notifications; // create a set specifically to check for new added groups.
	
	// INPUT.txt - file that stores the information for new groups to be added
	// open INPUT.txt and read it into a_map as well, thereby combinging the two
	std::ifstream input_str("00-INPUT.txt");
	if (!input_str.good()) {
		std::cerr << "Could not open 00-INPUT.txt to read\n";
		return 1;
	}
	read_words_input(a_map, notifications, input_str);
	
	// open up ALL.txt so that it can be rewritten with the combined text
	std::ofstream all_str_rewrite("00-ALL.txt");
	if (all_str_rewrite.is_open()) {
		write_to_ALL(a_map, all_str_rewrite);
	} else { return 0; }
	
	// rewrite each separate .txt category file.
	// all_text.txt - All Adoptable Groups
	std::ofstream all_txt_str("0-all_text.txt");
	if (all_txt_str.is_open()) {
		write_to_complete_list(a_map, all_txt_str);
	} else { return 0; }
	
	// all_accepted.txt - Groups that accept all types of adopts
	std::ofstream all_accepted_str("1-all_accepted.txt");
	if (all_accepted_str.is_open()) {
		write_to_txt(a_map, all_accepted_str, 1);
	} else { return 0; }
	
	// species.txt - Species Specific Groups
	std::ofstream species_txt_str("2-species.txt");
	if (species_txt_str.is_open()) {
		write_to_txt(a_map, species_txt_str, 2);
	} else { return 0; }
	
	// fandom.txt - Fandom Specific Groups
	std::ofstream fandom_txt_str("3-fandom.txt");
	if (fandom_txt_str.is_open()) {
		write_to_txt(a_map, fandom_txt_str, 3);
	} else { return 0; }
	
	// payment.txt - Payment Specific Groups
	std::ofstream payment_txt_str("4-payment.txt");
	if (payment_txt_str.is_open()) {
		write_to_txt(a_map, payment_txt_str, 4);
	} else { return 0; }
	
	// quality.txt - Groups with a Quality Filter
	std::ofstream quality_txt_str("5-quality.txt");
	if (quality_txt_str.is_open()) {
		write_to_txt(a_map, quality_txt_str, 5);
	} else { return 0; }
	
	// bases.txt - Groups for Adoptable Bases
	std::ofstream bases_txt_str("6-bases.txt");
	if (bases_txt_str.is_open()) {
		write_to_txt(a_map, bases_txt_str, 6);
	} else { return 0; }
	
	// agencies.txt - Adoption Agencies
	std::ofstream agencies_txt_str("7-agencies.txt");
	if (agencies_txt_str.is_open()) {
		write_to_txt(a_map, agencies_txt_str, 7);
	} else { return 0; }
	
	// open up NOTIFICATIONS.txt so that it can be rewritten with the combined text
	std::ofstream n_str("00-NOTIFICATIONS.txt");
	if (n_str.is_open()) {
		write_to_notification_list(notifications, n_str);
	} else { return 0; }
	
	std::cout << "Finished adding groups." << std::endl;
	std::cout << "There are currently " << (a_map.size()) << " groups in the directory." << std::endl;
}
