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
#include <cstdlib>

typedef std::map<std::string, std::vector<int> > adoptapedicmap;
// within the program, the overarching one will be referred to as a_map
typedef std::map<std::string, std::vector<int> >::iterator a_map_it;
// iterator to be used when cycling through the map

// --------------------------------------------------------------------------------
// Helper function that returns true if the input from the text file begins with a semi-colon,
// indicating that the value is the number of watchers the group has
bool detect_if_wc(std::string &word) {
	std::string::iterator itr = word.begin();
	if (*itr == ';') {
		return true;
	} else { return false; }
}

// --------------------------------------------------------------------------------
// Returns true if a duplicate is found and false if the spotlight isn't already in a_map
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
void read_words(adoptapedicmap &a_map, std::set<std::string> &notifications, std::ifstream & text_str, const bool &input_bool) {
	std::string x; // input variable
	std::string spotlight; // this stores the group name being processed while it's being added to categories
	int num; // used for itoa conversion
	std::string wc_string;
	int watcher_count;
	while (text_str >> x) {
		if (x.size() > 1) { // if the input is a word
			spotlight = x; // set spotlight as x
			for (int i=0; spotlight[i]; i++) {
				spotlight[i] = tolower(spotlight[i]); // make the word all lower case
			}
			// don't insert it only if the word already exists, but have it remain as spotlight in the event that categories are to be edited
			if (!duplicate_found(a_map, spotlight)) { //duplicate not found
				add(a_map, spotlight); // add it to a_map
				if (input_bool) {
					notifications.insert(spotlight); // add it to the notifications set
				}
			} // don't do anything if duplicate is found
		} else if (x.size() <= 2) { // if the input is a number rather than a word
			// convert to int and append this number to the spotlight's vector if it doesn't exist prior
			int num = atoi(x.c_str());
			if (std::find((a_map.find(spotlight)->second).begin(), (a_map.find(spotlight)->second).end(), num)==(a_map.find(spotlight)->second).end()) { // duplicate not found
				a_map[spotlight].push_back(num);
				//((a_map.find(spotlight))->second).push_back(num); // add on the new directory that the group will be a part of
			}
		} else if (detect_if_wc(x)) { // this indicates that the number is the number of watchers present in the group
			wc_string = x; // stands for watcher_count
			wc_string.erase(0,1); // remove the ; in front of the watcher count
			// now, the rest of the string needs to be converted into a number.
			watcher_count = atoi(wc_string.c_str());
			
			// convert the number to a category and append appropriately
			if ((watcher_count >= 1) and (watcher_count < 100)) {
				// if watcher_count is between 1 and 100, append an 8
				a_map[spotlight].push_back(8);
			} else if ((watcher_count >= 100) and (watcher_count < 500)) {
				// if watcher_count is between 100 and 500, append a 9
				a_map[spotlight].push_back(9);
			} else if ((watcher_count >= 500) and (watcher_count < 1000)) {
				// if watcher_count is between 500 and 1000, append a 10
				a_map[spotlight].push_back(10);
			} else if ((watcher_count >= 1000) and (watcher_count < 2000)) {
				// if watcher_count is between 1000 and 2000, append an 11
				a_map[spotlight].push_back(11);
			} else if ((watcher_count >= 2000) and (watcher_count < 3000)) {
				// if watcher_count is between 2000 and 3000, append a 12
				a_map[spotlight].push_back(12);
			} else if ((watcher_count >= 3000)) {
				// if watcher_count is over 3000, append a 13
				a_map[spotlight].push_back(13);
			}
		}
	}
}


// --------------------------------------------------------------------------------
// Simple function that goes through the 00-DELETE.txt file and removes entries that
// were inserted with misspellings and/or have been deactivated.
void delete_words(adoptapedicmap &a_map, std::ifstream & delete_str) {
	std::string x; // input variable
	while (delete_str >> x) {
		a_map.erase(x);
	}
}

// --------------------------------------------------------------------------------
// This goes through and updates the number of watchers that each group has in a way
// that allows input to be read line by line in the cygwin window rather than typed
// by hand into a .txt file that requires much more precise work in going line by line
// and remembering the categories available.
void update_watcher_counts(adoptapedicmap &a_map) {
	for (a_map_it iterator = a_map.begin(); iterator != a_map.end(); iterator++) {
		// remove numbers 8 through 13 from each group's individual category vector
		// in the future, see if the following could possibly be made into a separate remove function
		std::vector<int>::iterator itr = std::find((iterator->second).begin(), (iterator->second).end(), 8);	// erase 8
		if (itr != (iterator->second).end()) { (iterator->second).erase(itr); }
		itr = std::find((iterator->second).begin(), (iterator->second).end(), 9);	// erase 9
		if (itr != (iterator->second).end()) { (iterator->second).erase(itr); }
		itr = std::find((iterator->second).begin(), (iterator->second).end(), 10);	// erase 10
		if (itr != (iterator->second).end()) { (iterator->second).erase(itr); }
		itr = std::find((iterator->second).begin(), (iterator->second).end(), 11);	// erase 11
		if (itr != (iterator->second).end()) { (iterator->second).erase(itr); }
		itr = std::find((iterator->second).begin(), (iterator->second).end(), 12);	// erase 12
		if (itr != (iterator->second).end()) { (iterator->second).erase(itr); }
		itr = std::find((iterator->second).begin(), (iterator->second).end(), 13);	// erase 13
		if (itr != (iterator->second).end()) { (iterator->second).erase(itr); }
		
		int watcher_count;
		// prompt the user for input
		
		// print out the name of the group followed by enough spaces to make the numbers line up
		std::cout << (iterator->first);
		for (unsigned int i=0; i<(30-((iterator->first).size())); i++) { std::cout << " "; }
		std::cin >> watcher_count;
		
		// ## in the future, see if the below code can be made into a function since I repeat
		//    this same code in the read_words function as well
		if ((watcher_count >= 1) and (watcher_count < 100)) {
			// if watcher_count is between 1 and 100, append an 8
			a_map[(iterator->first)].push_back(8);
		} else if ((watcher_count >= 100) and (watcher_count < 500)) {
			// if watcher_count is between 100 and 500, append a 9
			a_map[(iterator->first)].push_back(9);
		} else if ((watcher_count >= 500) and (watcher_count < 1000)) {
			// if watcher_count is between 500 and 1000, append a 10
			a_map[(iterator->first)].push_back(10);
		} else if ((watcher_count >= 1000) and (watcher_count < 2000)) {
			// if watcher_count is between 1000 and 2000, append an 11
			a_map[(iterator->first)].push_back(11);
		} else if ((watcher_count >= 2000) and (watcher_count < 3000)) {
			// if watcher_count is between 2000 and 3000, append a 12
			a_map[(iterator->first)].push_back(12);
		} else if (watcher_count >= 3000) {
			// if watcher_count is over 3000, append a 13
			a_map[(iterator->first)].push_back(13);
		}
	}
}

// --------------------------------------------------------------------------------
// Rewrites 00-ALL.txt in a way such that it can be re-read through by this program
// and modified as such.
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
// Rewrite journal files to their respective .txt documents. Note, I personally find this method
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
	std::set<std::string> notifications; // create a set specifically to check for new added groups.
	
	// 00-ALL.txt - file that stores the information of all the groups already stored
	// open ALL.txt and read into a_map
	std::ifstream all_str("00-ALL.txt");
	if (!all_str.good()) {
		std::cerr << "Could not open 00-ALL.txt to read\n";
		return 1;
	}
	read_words(a_map, notifications, all_str, false);
	
	// variable to determine which set of actions is performed
	int response;
	std::cout << "1) Add groups\n2) Update watcher counts\n  Your selection :::   ";
	std::cin >> response;
	
	if (response == 1) {
		// 00-DELETE.txt contains a list of groups that have deactivated and as thus need to be removed
		// from the directory.
		std::ifstream delete_str("00-DELETE.txt");
		if (!delete_str.good()) {
			std::cerr << "Could not open 00-DELETE.txt to read\n";
			return 1;
		}
		delete_words(a_map, delete_str);
		
		// 00-INPUT.txt - file that stores the information for new groups to be added
		// open INPUT.txt and read it into a_map as well, thereby combinging the two
		std::ifstream input_str("00-INPUT.txt");
		if (!input_str.good()) {
			std::cerr << "Could not open 00-INPUT.txt to read\n";
			return 1;
		}
		read_words(a_map, notifications, input_str, true);
	}
	
	// update the watcher counts using the helper function to use as a prompter
	if (response == 2) { update_watcher_counts(a_map); }
	
	// open up ALL.txt so that it can be rewritten with the combined text
	std::ofstream all_str_rewrite("00-ALL.txt");
	if (all_str_rewrite.is_open()) {
		write_to_ALL(a_map, all_str_rewrite);
	} else { return 0; }
	all_str_rewrite.close();
	
	if (response == 1) {
		// rewrite each separate .txt category file.
		// all_text.txt - All Adoptable Groups
		std::ofstream all_txt_str("0-all_text.txt");
		if (all_txt_str.is_open()) {
			write_to_txt(a_map, all_txt_str, 0);
		} else { return 0; }
		all_txt_str.close();
		
		// all_accepted.txt - Groups that accept all types of adopts
		std::ofstream all_accepted_str("1-all_accepted.txt");
		if (all_accepted_str.is_open()) {
			write_to_txt(a_map, all_accepted_str, 1);
		} else { return 0; }
		all_accepted_str.close();
		
		// species.txt - Species Specific Groups
		std::ofstream species_txt_str("2-species.txt");
		if (species_txt_str.is_open()) {
			write_to_txt(a_map, species_txt_str, 2);
		} else { return 0; }
		species_txt_str.close();
		
		// fandom.txt - Fandom Specific Groups
		std::ofstream fandom_txt_str("3-fandom.txt");
		if (fandom_txt_str.is_open()) {
			write_to_txt(a_map, fandom_txt_str, 3);
		} else { return 0; }
		fandom_txt_str.close();
		
		// payment.txt - Payment Specific Groups
		std::ofstream payment_txt_str("4-payment.txt");
		if (payment_txt_str.is_open()) {
			write_to_txt(a_map, payment_txt_str, 4);
		} else { return 0; }
		payment_txt_str.close();
		
		// quality.txt - Groups with a Quality Filter
		std::ofstream quality_txt_str("5-quality.txt");
		if (quality_txt_str.is_open()) {
			write_to_txt(a_map, quality_txt_str, 5);
		} else { return 0; }
		quality_txt_str.close();
		
		// bases.txt - Groups for Adoptable Bases
		std::ofstream bases_txt_str("6-bases.txt");
		if (bases_txt_str.is_open()) {
			write_to_txt(a_map, bases_txt_str, 6);
		} else { return 0; }
		bases_txt_str.close();
		
		// agencies.txt - Adoption Agencies
		std::ofstream agencies_txt_str("7-agencies.txt");
		if (agencies_txt_str.is_open()) {
			write_to_txt(a_map, agencies_txt_str, 7);
		} else { return 0; }
		agencies_txt_str.close();
	}
	
	// 8-1_100.txt - Groups with between 1 and 100 watchers
	std::ofstream eight_txt_str("8-1_100.txt");
	if (eight_txt_str.is_open()) {
		write_to_txt(a_map, eight_txt_str, 8);
	} else { return 0; }
	eight_txt_str.close();
	
	// 9-100_500.txt - Groups with between 100 and 500 watchers
	std::ofstream nine_txt_str("9-100_500.txt");
	if (nine_txt_str.is_open()) {
		write_to_txt(a_map, nine_txt_str, 9);
	} else { return 0; }
	nine_txt_str.close();
	
	// 10-500_1000.txt - Groups with between 500 and 1000 watchers
	std::ofstream ten_txt_str("10-500_1000.txt");
	if (ten_txt_str.is_open()) {
		write_to_txt(a_map, ten_txt_str, 10);
	} else { return 0; }
	ten_txt_str.close();
	
	// 11-1000_2000.txt - Groups with between 1000 and 2000 watchers
	std::ofstream eleven_txt_str("11-1000_2000.txt");
	if (eleven_txt_str.is_open()) {
		write_to_txt(a_map, eleven_txt_str, 11);
	} else { return 0; }
	eleven_txt_str.close();
	
	// 12-2000_3000.txt - Groups with between 2000 and 3000 watchers
	std::ofstream twelve_txt_str("12-2000_3000.txt");
	if (twelve_txt_str.is_open()) {
		write_to_txt(a_map, twelve_txt_str, 12);
	} else { return 0; }
	twelve_txt_str.close();
	
	// 13-3000+.txt - Groups with more than 3000 watchers
	std::ofstream thirteen_txt_str("13-3000+.txt");
	if (thirteen_txt_str.is_open()) {
		write_to_txt(a_map, thirteen_txt_str, 13);
	} else { return 0; }
	thirteen_txt_str.close();
	
	if (response == 1) {
		// open up NOTIFICATIONS.txt so that it can be rewritten with the combined text
		std::ofstream n_str("00-NOTIFICATIONS.txt");
		if (n_str.is_open()) {
			write_to_notification_list(notifications, n_str);
		} else { return 0; }
		n_str.close();
	}
	
	// output ending statements
	if (response == 1) {
		std::cout << "Finished adding groups." << std::endl;
		std::cout << "There are currently " << (a_map.size()) << " groups in the directory." << std::endl;
	} else if (response == 2) {
		std::cout << "====================================" << std::endl;
		std::cout << "Finished updating watcher counts! :D" << std::endl;
	}
}
