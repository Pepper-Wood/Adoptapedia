// (( Writing this in code so it's easier to read ))

// Complete directory of files that I have within the Adoptapedia folder on my desktop:
// Numbers have been added in front of the text documents so as to "alphabetize" them in a logical order. Those with 000 prefaces are files that are actively edited within the program and are the core databases
00-ALL.txt					// complete collection of all the groups already stored. This is the main file that is accessed by everything
00-INPUT.txt				// list of groups to add as well as their corresponding categories
00-NOTIFICATIONS.txt		// stores htmled versions of the groups written in INPUT.txt

// Single integer prefaces are for the separate categories as labelled by number
0-all_text.txt				// complete list of all the adoptable groups stored
1-all_accepted.txt			// adoptable groups that accept all kinds of adopts
2-species.txt				// adopt groups that accept only species-related adopts
3-fandom.txt				// adopt groups made for specific fandoms
4-payment.txt				// adopt groups that only accept a certain form of payment
5-quality.txt				// adopt groups that only accept adopts deemed of a certain standard of quality
6-bases.txt					// groups that offer bases to use for adopts
7-agencies.txt				// RP-based adoptable agencies where you can purchase an adopt to use within the world

// The following are the .cpp files used to modify the .txt files
add_groups.cpp				// adds groups within the INPUT.txt file to the group directory and formats .txt files accordingly
add_groups.exe
add_groups.exe.stackdump
notify_new_groups.cpp		// transforms the groups listed in INPUT.txt to NOTIFICATIONS.txt to make sending notifications easier
notify_new_groups.exe
README.cpp					// the file that you are currently reading ;)
