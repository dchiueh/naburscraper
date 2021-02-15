# Given a list of dedicated discussion post pages, pulls page content to a csv.
# Pages must be set to public.

from bs4 import BeautifulSoup
import requests
import csv
import os

outfile = open('WW_multiplescrape.csv', 'w', newline='', encoding="utf-8")
writer = csv.writer(outfile)
writer.writerow(["URL", "Content Type", "Creation Date", "Username", "Title", "Content", "Group"]) #Heading


dirloc = r"C:\Users\sdoong\Documents\scraper\WW HTML" 

#calling scandir() function
for file in os.scandir(dirloc):

    if (file.path.endswith(".html") and file.is_file()):
        infile = open(file.path, 'r', encoding="utf-8")
        source = infile.read()

    soup = BeautifulSoup(source, 'lxml')

    #Load main discussion post

    date = soup.find(attrs={"property": "article:published_time"}) #needs some processing
    date = date.get('content')
    date = date[:10]
    username = soup.find(attrs={"property": "article:author"}).get('content')
    username = username.removeprefix("https://wenatcheeworld.ning.com/members/")
    title = soup.find(attrs={"property": "og:title"}).get('content')
    content = str(soup.find("section", class_="entry-content"))
    content = content.removeprefix("<section class=\"entry-content cf\">")
    content = content.removesuffix("</section>")
    content = content.strip()
    group = soup.find(attrs={"property": "article:section"})
    group = group.get('content')

    writer.writerow(["", "Discussion", date, username, title, content, group])

    for comment in soup.find_all("li", class_="comments-comment"):
        date = comment.get("data-comment-created-date")
        #if(date): 
            # date = date[:10]
        print(date)
        username = comment.find_next("a", class_="avatar-frame")
        username = username.get('href')
        username = username.removeprefix("https://wenatcheeworld.ning.com/members/")
        content = str(comment.find_next("div", class_="comments-text entry-content"))
        content = content.removeprefix("<div class=\"comments-text entry-content\">")
        content = content.removesuffix("</div>")

        referent = comment.find("span", class_="comments-replyingTo")
        if (referent) : # if you can find this class
            types = "Reply to a reply"
            content = "<p> @" + referent.get_text().removeprefix(" > ") + " " + content
        else :
            types = "Reply"

        if (date):
            date = date[:10]
            writer.writerow(["", types, date, username, "", content, ""])

outfile.close()
infile.close() 