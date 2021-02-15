# Given a list of topic pages with various discussion posts, pulls the link for each discussion post
# to a csv. Topic page must be set to public. Topic pages are linked in "startinglinks.csv"

from bs4 import BeautifulSoup
import requests
import csv

outfile = open('WW_multiplepages.csv', 'w', newline='')
writer = csv.writer(outfile)

infile = open('discussionpages.csv', 'r')
reader = csv.reader(infile)

for row in reader: # iterate over each link provided
    source = requests.get(''.join(row)).text #Need to convert from list object to string with join method

    soup = BeautifulSoup(source, 'lxml')

    for entry in soup.find_all(attrs={"class": "pagination-last"}):
        if (entry):
            writer.writerow([''.join(row), entry.get_text()])

outfile.close()
infile.close()