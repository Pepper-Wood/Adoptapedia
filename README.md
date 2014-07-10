Adoptapedia
===========
This is the program I use to update the deviantArt adoptable group I run called Adoptapedia (found at adoptapedia.deviantart.com). I will be updating it from time to time as I learn of new methods to make the program more efficient.
History
===========
This program is rather special to me as I started this project about 2 years ago when I wanted to make a group just so I could spend my time cataloguing things. So I made a group that kept track of the various kinds of adoptable groups (To define, adoptables are designs that artist make to sell to others who will use the character in any sort of way, whether it be roleplaying or story-writing, etc.).

But after a few weeks or so, the directory grew and grew, making it take much longer to add in entries by hand. At around the same time, I was in a Java programming class within my high school, and as a final project I requested to write this program and submit it for credit. I worked hard, but in the end I wasn't able to finish in time, and had I done so the runtime would have taken forever. Within the program, there are several categories, and I was using Java lists to store them, requiring me to continuously cycle through lists with very low efficiency.

The current status of the project is that it was rewritten in C++, as I have just completed a Data Structures college course. I will be keeping track of future plans for the program as well as modifications I want to do but don't know how to conduct within the program.
Updates
===========
6/19/2014
- add_groups.cpp added to repository. It can't run in its current state due to it not being completely debugged.
- Eventually, I might make the data structure adoptapedicmap a map<string,set<int>> instead of a map<string,vector<int>> to reduce runtime.
- I'd like to figure out a way to store how each group is rated in terms of popularity and community involvement as well as a script that copies the output text documents and edits the journal entries where the dictionary entries are displayed.
- I also want to find out how to manage multiple output streams more effectively since having to reloop through the map for each category results in a runtime of O(klog(n)) with k being the number of categories and n as the number of groups stored. At the moment, the runtime is around 17 seconds.

7/1/2014
- add_groups.cpp fully debugged and works
- runtime for my current file size is maybe 2 seconds, so the runtime shouldn't be something to worry about. However for learning purposes, I still want to address issues.
- Add a ranking system in the future for groups.
- In the future, get atoi to work
- Write a function that clears the text in INPUT.txt
- A prompt for whether groups are to be added or a group deleted.
- Future script that copies the text in the .txt files and replaces the journal entries

7/2/2014
- This is a super quick update since all I did was add notify_groups.cpp and changed the .txt filenames so that they're organized within the Adoptapedia folder on my desktop.
- All previous plans for the program remain the same.

7/3/2014
- Rewrote add_groups.cpp to perform the same task as notify_groups.cpp.
- In the process, there was a bug with the code that prevented it from recognizing new groups not in the directory. That has been addressed and fixed.

7/10/2014
- Renamed add_groups.cpp to main.cpp after beginning to write a separate helper function called update_wc.cpp but realizing that most of the code would be reused.
- Added function that makes updating the number of watchers groups have a bit easier for me.
- Figured out how to implement atoi correctly! :D
- Modififed read_words so that I can just write in the number of watchers a group has into 00-INPUT.txt and have it determine the category that it belongs in
- Maybe eventually I can have the input document read in sub words as categories rather than numbers so it'll be easier for me to remember them off the top of my head.
- I'm going to see if there is a way for me to access the number of watchers a person has through a function rather than by hand so that I could just run a for loop to update the watch count rather than open each individual webpage, write the watch count, and then do the same for the rest of them. As in, get a function to cycle through a list of urls and return the number of watchers to a separate .txt file and then read that in as another list to use in main.cpp.
