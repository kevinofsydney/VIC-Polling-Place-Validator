
# coding: utf-8

# In[2]:


# Written by Kevin Gatdula for Antony Green @ ABC, assisting with the Victorian State Election 
# @kevinofsydney 2018

# INPUT: 
# This script takes two files, one with the list of Victorian polling places in 2014 and the other for 2018.
# It iterates through the two files to check:
    # PPs that were present at both elections
    # PPs present in 2018 that were not present in 2014 (new PPs)
    # PPs present at both elections whose addresses have changed
    # PPs present in 2014 that are no longer present in 2018 (dead PPs)
    # PPs present at both elections whose VenueName hasn't changed but Address has stayed the same

# OUTPUT:    
# The script can print out a report (to stdout only) the results of the above checks.
# Also, it can print out as a CSV a list of all the polling places whose addresses have changed in 2014. 
# Lastly, it will open Google searches in your default browser (once per 15 seconds) for each of the 
    # polling places whose address have changed. 

# To run: python3 pp_validator.py [20x4.csv] [20x8.csv]
    # Here, 20x4.csv refers to the file name of the older list of polling places (in this case 'VIC2014_PollingPlaces.csv') 
        # while 20x8.csv refers to the new list of polling places (in this case 'VIC2018_PollingPlaces.csv')
    # The script must be in the same directory as the polling place files
    # The polling place files must have the following columns in the same order:
        # Electorate - PollingPlaceName - Address - Locality
        
    # To make the results more meaningful, find and replace in both files (using Excel, etc.) 
        # common words that are typically shortened, especially street suffixes 
        # e.g. 'Street' -> 'St', 'Avenue' -> 'Ave', 'corner' -> 'cnr'
        # The more common ones have been handled, but there are too many cases to cover them exhaustively


# TODO list:
#    1. Load both CSVs [Done]
#    2. Strip trailing whitespace - spaces and tabs [Done]
#    3. Text replace Street with St, Avenue with Ave, Parade with Pde, etc. [Done]
#    4. Ignore case
#    5. PPs whose address hasn't changed [Done]
#    6. PPs whose address has changed [Done]
#    7. PPs that did not exist in 2014 that now exist in 2018 [Done]
#    8. PPs that existed in 2014 that no longer exist in 2018 [Done]
#    9. [Optional?] PPs that were split in 2018 that were not split in 2014 
#    10. [Optional?] PPs that were split in 2014 that were not split in 2018
#    11. [Optional?] Highlight all split PPs, either in 2014 or from 2018, for manual review
#    12. Potential feature: A command-line flag to switch Google searching on or off
#    13. Potential feature: A command-line flag to switch CSV output on or off
#    14. Potential feature: Useful terminal printouts to show script progress (e.g. "13% complete...") [Done]

# In[3]:


import csv
import re
import sys


# In[15]:


# This regex pattern matches the names only so that it ignores any trailing whitespace in the PP name
pat = re.compile('([ \t]*$)')
stpat = re.compile('Street')
stspat = re.compile('Streets')
rdpat = re.compile('Road')
rdspat = re.compile('Roads')
avepat = re.compile('Avenue')
hwypat = re.compile('Highway')
cnrpat = re.compile('[cC]orner')
drpat = re.compile('Drive')
pdepat = re.compile('Parade')


# In[22]:


# Load the 2014 and 2018 polling place CSVs into lists
if len(sys.argv) == 1:
    print("ERROR: No filenames given.")
    sys.exit(1)
elif len(sys.argv) == 2: 
    print("ERROR: Second filename not given.")
    sys.exit(1)

csv_2014 = sys.argv[1]
csv_2018 = sys.argv[2]

# Just kept for legacy purposes
# temp1 = 'VIC2014_PollingPlaces.csv'
# temp2 = 'VIC2018_PollingPlaces.csv'

old_pp_raw = []
new_pp_raw = []

with open(csv_2014, 'r', encoding='utf-8-sig') as csvfile1:   # Note: PP - polling places
    old_pp_raw = list(csv.reader(csvfile1, delimiter=","))
    
    with open(csv_2018, 'r', encoding='utf-8-sig') as csvfile2: # Without UTF-8 argument, byte-order shows up as garbage characters in data
        new_pp_raw = list(csv.reader(csvfile2, delimiter=","))


# In[21]:


# Strips out trailing whitespace in both datasets and converts all road suffixes to shortened form for consistency
for row in old_pp_raw:
    for index, item in enumerate(row):
        row[index] = re.sub(pat, '', row[index])
        row[index] = re.sub(stpat, 'St', row[index])
        row[index] = re.sub(stspat, 'Sts', row[index])
        row[index] = re.sub(rdpat, 'Rd', row[index])
        row[index] = re.sub(rdspat, 'Rds', row[index])
        row[index] = re.sub(avepat, 'Ave', row[index])
        row[index] = re.sub(hwypat, 'Hwy', row[index])
        row[index] = re.sub(cnrpat, 'cnr', row[index])
        row[index] = re.sub(drpat, 'Dr', row[index])
        row[index] = re.sub(pdepat, 'Pde', row[index])
        

for row in new_pp_raw:
    for index, item in enumerate(row):
        row[index] = re.sub(pat, '', row[index])
        row[index] = re.sub(stpat, 'St', row[index])
        row[index] = re.sub(stspat, 'Sts', row[index])
        row[index] = re.sub(rdpat, 'Rd', row[index])
        row[index] = re.sub(rdspat, 'Rds', row[index])
        row[index] = re.sub(avepat, 'Ave', row[index])
        row[index] = re.sub(hwypat, 'Hwy', row[index])
        row[index] = re.sub(cnrpat, 'cnr', row[index])
        row[index] = re.sub(drpat, 'Dr', row[index])
        row[index] = re.sub(pdepat, 'Pde', row[index])


# In[19]:


# The master result list
results = [[], [], [], [], [], [], []]
    # Index 0: PPs that were present at both elections
    # Index 1: PPs present in 2018 that were not present in 2014 (new PPs)
    # Index 2: PPs present at both elections whose addresses have changed
    # Index 3: The old address
    # Index 4: PPs present in 2014 that are no longer present in 2018 (dead PPs)
    # Index 5: PPs present at both elections whose VenueName hasn't changed but Address has stayed the same
    # Index 6: The old VenueName
    
# For each PP in 2018, check if a match exists in 2014
for index, new_row in enumerate(new_pp_raw):
    # Skip the title row
    if index is 0:
        continue 

    matchFound = False

    for index, old_row in enumerate(old_pp_raw):
        # Skip the title row
        if index is 0:
            continue 

        # Form a unique key with Electorate + PollingPlaceName
        # Use this unique key to check if PP was present in 2014
        if str(new_row[0] + new_row[1]) == str(old_row[0] + old_row[1]): 
            matchFound = True

            # If a match is found, check if the VenueName has changed (not including those where address is the same)
            if new_row[2] != old_row[2] and new_row[3] != old_row[3]:
                results[2].append(new_row)
                results[3].append(old_row)
                
            # If a match is found, check if VenueName has changed but Address has stayed the same
            if new_row[2] != old_row[2] and new_row[3] == old_row[3]:
                results[5].append(new_row)
                results[6].append(old_row)
            
            break # First key constructed above should only match once

    if matchFound:
        results[0].append(new_row)
    else:
        results[1].append(new_row)
        
        
# For each PP in 2014, see if any have been removed in 2018
for index, old_row in enumerate(old_pp_raw):
    # Skip title row
    if index is 0:
        continue
        
    matchFound = False
    
    for index, new_row in enumerate(new_pp_raw):
        # Skip title row
        if index is 0:
            continue
        
        # Form a unique key with Electorate + PollingPlaceName
        # Use this unique key to check if PP was present in 2018
        if str(old_row[0] + old_row[1]) == str(new_row[0] + new_row[1]): 
            matchFound = True
            break
        
    if not matchFound:
        results[4].append(old_row)


# In[20]:


# Results printer

print("There were %d polling places in 2014, and there are %d polling places in 2018." % (len(old_pp_raw), len(new_pp_raw)))
print()
print("Differences in these two numbers can be caused by:")
print("\t- Polling places that have been removed or added for the 2018 election")
print("\t- Polling places that are used for more than one electorate are counted multiple times")
print() 
print("There are %d polling places that are new in 2018. (electorate, polling place name)" % (len(results[1])))
for row in results[1]:
    print('\t%s - %s' % (row[0], row[1]))

print()
print("There are %d polling places that were present in 2014 but have been removed for 2018." % (len(results[4])))
for row in results[4]:
    print('\t%s - %s' % (row[0], row[1]))

print()
print("There are %d polling places that were present in both elections but have changed address." % len(results[2]))
for index, row in enumerate(results[2]):
    print('\t%s - %s' % (row[0], row[1]))
    print('\t\tOld: %s, %s, %s' % (results[3][index][2], results[3][index][3], results[3][index][4]))
    print('\t\tNew: %s, %s, %s' % (row[2], row[3], row[4]))
    
print()
print("There are %d polling places that present in both elections whose VenueName has changed but Address has stayed the same." % len(results[5]))
for index, row in enumerate(results[5]):
    print('\t%s - %s' % (row[0], row[1]))
    print('\t\tOld: %s, %s, %s' % (results[6][index][2], results[6][index][3], results[6][index][4]))
    print('\t\tNew: %s, %s, %s' % (row[2], row[3], row[4]))


# In[25]:


# Transform the results into a form that's easy to write to CSV
export_list = []

# [electorate, polling place name, old address, new address]
for index, item in enumerate(results[2]):
    electorate = results[2][index][0]
    pp_name = results[2][index][1]
    old_address = str(results[3][index][3] + ", " + results[3][index][4])
    new_address = str(results[2][index][3] + ", " + results[2][index][4])
    export_list.append([electorate, pp_name, old_address, new_address])

# This section prints out ONLY the PPs which were present at both elections but whose addresses have changed.
# Change OUTPUT to True if you want the script to generate this ouput. Otherwise, it will print to screen. 
OUTPUT = False
if OUTPUT:
    with open('vic_pp_validator_output.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Electorate', 'PollingPlaceName', 'OldAddress', 'NewAddress'])
        for row in export_list:
            writer.writerow(row)
else:
    print("The following polling places were present in both elections but have different addresses.")
    print("Electorate - Polling Place Name - Old Address - New Address")
    for i in export_list:
        print(i)
    print()


# In[35]:


# Run the Google searches to check the distances between the changed polling places
    # I have to run it like this because otherwise I'd have to pay for Google developer API calls
    # Turn SEARCH to True if you want to run the Google searches. 
    # Searches wait between 5-15 seconds to avoid being shut out by Google's anti-robot detection
    
import time
import webbrowser
import random
search_terms = []

SEARCH = False
if SEARCH:
    for index, row in enumerate(results[2]):
        search_terms.append(str(results[3][index][2] + " " + results[3][index][4] + " Victoria to " + " " + row[2] + " " + row[4] + " Victoria"))

    print("INFO: Commencing searches.")
    for i in range(len(search_terms)):
        print("INFO: %d%% complete." % (int(i*100 / len(search_terms))))
        url = "https://www.google.com.au/search?q={}".format(search_terms[i])
        webbrowser.open_new_tab(url)
        time.sleep(random.randint(5, 15))
        
    print("INFO: Searches completed!")

