# CincyBarScraper
Scrape the Cincinnati Bar website for phone numbers from a CSV list of names

Usage: python scrape.py sourcefile.csv outfile.csv

The source file should be a standard CSV with Firstname/Lastname as columns, no headers.

The script searches the site with the firstname and truncated last name, and returns the phone number of the first result found.  The last name is truncated to the first "," to remove any suffixes (e.g. "Jr.", "III", etc.). If your last name column does not delimit suffixes in the last name with a comma, names with suffixes may return zero results.

