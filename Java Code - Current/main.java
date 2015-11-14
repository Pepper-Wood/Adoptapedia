// STEP 1) Create a parsing function for the "groups to add" google form
// STEP 2) Create a parsing function for pre-existing groups
// STEP 3) Merge the two
//		-- duplicate entries have their categories merged
//		  -- i.e. "GroupA" is in the "Species specific" category
//		  -- "GroupA" already exists in "Payment specific" category
//		  -- "GroupA" now exists in "Species Specific" and "Payment specific" categories

// STEP 4) Parse a given webpage and update watcher count for directory
// STEP 5) Parsing a Google Doc of groups to delete
//		-- removes entries from the over-arching data structure
//      -- clear the document when finished

// STEP 6) Formatting outputs to pre-existing spreadsheet and the journal-formatted outputs
// STEP 7) Script to automatically update deviantArt pages????