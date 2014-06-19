

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


typedef std::map<std::string, std::vector<int> > adoptapedicmap;
// within the program, the overarching one will be referred to as a_map
typedef std::map<std::string, std::vector<int> >::iterator a_map_it;
// iterator to be used when cycling through the map to determine 

// --------------------------------------------------------------------------------
// Add a new group to the adoptapedic map
void add(adoptapedicmap &a_map, const std::string &spotlight) {
	int zero_vector[] = {0}; // this will be used as the default vector setting when groups are installed
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
			// don't insert it only if the word already exists, but have it remain as spotlight in the event that categories are to be edited
			if (a_map.find(spotlight)!=a_map.end()) { //duplicate not found
				add(a_map, spotlight); // add it to a_map 
			} // don't do anything if duplicate is found
		}
		else if (x.size() == 1) { // if the input is a number rather than a word
			// convert to int and append this number to the spotlight's vector if it doesn't exist prior
			num = std::atoi(x);
			if (std::find((a_map.find(spotlight)->second).begin(), (a_map.find(spotlight)->second).end(), num)==(a_map.find(spotlight)->second).end()) { // duplicate not found
				(a_map.find(spotlight)->second).push_back(num); // add on the new directory that the group will be a part of
			}
		}
	}
}

// --------------------------------------------------------------------------------
void write_to_ALL(adoptapedicmap &a_map, std::ofstream &out_str) {
	for (a_map_it iterator = a_map.begin(); iterator != a_map.edn(); iterator++) {
		// iterator->first = group name
		out_str << iterator->first;
		// iterator->second = vector of ints for categories
		for (unsigned int i=1; i<(iterator->second).size(); i++) { // print out categories except for the 0
			out_str << " " << (iterator->second[i]);
		}
		out_str << std::endl;
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

// ================================================================================
int main(int argc, char* argv[]) {
	adoptapedicmap a_map;
	
	// ALL.txt - file that stores the information of all the groups already stored
	// open ALL.txt and read into a_map
	std::ifstream all_str("ALL.txt");
	if (!all_str.good()) {
		std::cerr << "Could not open ALL.txt to read\n";
		return 1;
	}
	read_words(a_map, all_str);
	
	// INPUT.txt - file that stores the information for new groups to be added
	// open INPUT.txt and read it into a_map as well, thereby combinging the two
	std::ifstream input_str("INPUT.txt");
	if (!input_str.good()) {
		std::cerr << "Could not open INPUT.txt to read\n";
		return 1;
	}
	read_words(a_map, input_str);
	
	// open up ALL.txt so that it can be rewritten with the combined text
	std::ofstream all_str_rewrite("ALL.txt");
	if (all_str_rewrite.is_open()) {
		write_to_ALL(a_map, all_str_rewrite);
	} else { return 0; }
	
	// rewrite each separate .txt category file.
	// all_text.txt - All Adoptable Groups
	std::ofstream all_txt_str("all_text.txt");
	if (all_txt_str.is_open()) {
		write_to_txt(a_map, all_txt_str, 0);
	} else { return 0; }
	
	// all_accepted.txt - Groups that accept all types of adopts
	std::ofstream all_accepted_str("all_accepted.txt");
	if (all_accepted_str.is_open()) {
		write_to_txt(a_map, all_accepted_str, 1);
	} else { return 0; }
	
	// species.txt - Species Specific Groups
	std::ofstream species_txt_str("species.txt");
	if (species_txt_str.is_open()) {
		write_to_txt(a_map, species_txt_str, 2);
	} else { return 0; }
	
	// fandom.txt - Fandom Specific Groups
	std::ofstream fandom_txt_str("fandom.txt");
	if (fandom_txt_str.is_open()) {
		write_to_txt(a_map, fandom_txt_str, 3);
	} else { return 0; }
	
	// payment.txt - Payment Specific Groups
	std::ofstream payment_txt_str("payment.txt");
	if (payment_txt_str.is_open()) {
		write_to_txt(a_map, payment_txt_str, 4);
	} else { return 0; }
	
	// quality.txt - Groups with a Quality Filter
	std::ofstream quality_txt_str("quality.txt");
	if (quality_txt_str.is_open()) {
		write_to_txt(a_map, quality_txt_str, 5);
	} else { return 0; }
	
	// bases.txt - Groups for Adoptable Bases
	std::ofstream bases_txt_str("bases.txt");
	if (bases_txt_str.is_open()) {
		write_to_txt(a_map, bases_txt_str, 6);
	} else { return 0; }
	
	// agencies.txt - Adoption Agencies
	std::ofstream agencies_txt_str("agencies.txt");
	if (agencies_txt_str.is_open()) {
		write_to_txt(a_map, agencies_txt_str, 7);
	} else { return 0; }
}
