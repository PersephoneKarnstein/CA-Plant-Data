# CA-Plant-Data
A quick and dirty set of tools for getting data from the CalFlora and CalScape California native plant databases that their built-in search features are not optimized for returning

Because these were all written as one-off tools for me to use and are relatively simple, none of them are either well-commented nor optimized for other uses except by muddling around in the code.

However, as stated, they are all fairly simple to understand and their uses are as follows:

==============
bog_plants.py
==============
Reads in an Excel spreadsheet of plant names (in the code as "plants2.xlsx"), and checks which one of them enjoy growing in standing water. Can be easily edited to check for other drainage types or other properties that Calscape lists but won't search by.

==============
plantcoords.py
==============
The most involved tool of the set to use. Requires the user to save the "weeddata" response from a calflora plant distribution map (e.g. https://www.calflora.org/entry/dgrid.html?crn=348) as a file before using. The function is then called with the file in the terminal call (e.g. "python plantcoords.py Androsace_elongata.txt"). The program will then strip out the useless data and return an Excel spreadsheet of the Latitude and Longitude of each observation.

==============
plants.py
==============
A very simple scraper that, given the url of a search on the CalFlora database, will return the name of every plant (even if multiple pages of results are returned) in an Excel file.

==============
overlap.py
==============
Another tool that only works given a specific extant file, but fairly easily generalizable. Given an Excel spreadsheet in which each column is titled with the name of a biome followed by a list of plants found in that biome as scraped by plants.py, finds which plants occur in multiple biomes. It then checks that (significantly shorter) list of plant names against the CalScape database to see which require the least water. Finally, prints its results to the terminal.
