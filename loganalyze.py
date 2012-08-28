#!/usr/bin/env python

# We need yaml because the config file is yaml
import yaml

# We're working with files, so we need os too
import os

# We will use regular expressions to find ip addresses
import re

# We are doing some string operations, so we need the string librar
import string

# Let's do some configuration first and figure out
# where the log file is and what it is called.

# Open the configuration file and read its contents:
configFile = open('loganalyze.cfg')
configText = configFile.read()
configFile.close()

# The configuration file is yaml so load it as a dictionary.
# For now the keys are 'auth-log-location' and 'auth-log-name'
# configurationParams is a dictionary containing these.
configurationParams = yaml.load(configText)

# Get the value for the name of the auth.log and its location:
# And get the location and name for our output ban-file:
authLogFileLocation = configurationParams['auth-log-location']
authLogFile = configurationParams['auth-log-name']
banFileLocation = configurationParams['blacklist-ban-file-location']
banFile = configurationParams['blacklist-ban-file-name']

# Now add the Log location and log-file name together to get 
# the full path:
authLogPath = authLogFileLocation + authLogFile
# Do the same for our ban file:
banFilePath = banFileLocation + banFile

# Now let's open the auth.log file

# Try to find it based on the config file path and filename:
try:
	authLogContents = open(''.join(authLogPath))
	authLogText = authLogContents.read()
	authLogContents.close()
# If we can't find it, tell the user:
except IOError:
	print "Error: auth.log file or path not found!"

# We want to search the log file for this phrase:

# Add this too: "Invalid user "
hackerNoticeText = "Failed password for"
#hackerNoticeText = ['Invalid user', 'Failed password for']
#hackerNoticeText = "Failed password for" or "Invalid user"

# Store each line in the string authlogText in a list called
# authLogTextEntries
authLogTextLineEntries = authLogText.splitlines(True)


# Search the list items entries for the pattern and store positives
# in a list called hackerAttempts

# Set up our Regex pattern to look for ip addresses ie. 91.205.189.15

ipMatcher = re.compile(r'((([2][5][0-5]|([2][0-4]|[1][0-9]|[0-9])?[0-9])\.){3})([2][5][0-5]|([2][0-4]|[1][0-9]|[0-9])?[0-9])')

hackerAttempts = []

for i, s in enumerate(authLogTextLineEntries):
     if hackerNoticeText in s:
        hackerAttempts.append(authLogTextLineEntries[i])

# A list of IP's that have attempted to authenticate and failed
matches = []

for s in hackerAttempts:
    m = ipMatcher.search(s)
    if m is not None:
        #matches.append(m.group(0))
        matches.append(m.group())

# Remove any duplicate entries by turning the list into a set.
uniqueMatches = list(set(matches))

# Let's write the results out to a file
'''
Try to:
Open the file for appending, a
Go to the end of the file, 2
Write the matches with newlines
Finally, close the file.
If an error occurs, tell the user.
'''
try:
	banFileContents = open(''.join(banFilePath), "a") 
	banFileContents.seek(2)
	banFileContents.write('\n'.join(uniqueMatches))
	banFileContents.close()
except IOError:
	print "Error: ban file or path not found!"

