# VIC-Polling-Place-Validator
This short script was written to assist Antony Green with the 2018 Victoria State Election. The script detects polling places whose venues.  or addresses have changed since the last State election.

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
