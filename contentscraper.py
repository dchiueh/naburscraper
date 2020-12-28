# Given a list of dedicated discussion post pages, pulls page content to a csv.
# Pages must be set to public.

from bs4 import BeautifulSoup
import requests
import csv

outfile = open('scrapedcontent.csv', 'w', newline='')
writer = csv.writer(outfile)
writer.writerow(["Content Type", "Creation Date", "Username", "Title", "Content", "Group"]) #Heading

infile = open('discussionpages.csv', 'r')
reader = csv.reader(infile)

for row in reader: # iterate over each link provided
    source = requests.get(''.join(row)).text #Need to convert from list object to string with join method

    soup = BeautifulSoup(source, 'lxml')

    #Load main discussion post

    date = soup.find(attrs={"property": "article:published_time"}) #needs some processing
    date = date.get('content')
    date = date[:10]
    username = soup.find(attrs={"property": "article:author"}).get('content')
    username = username.removeprefix("https://gvnews.ning.com/members/")
    title = soup.find(attrs={"property": "og:title"}).get('content')
    content = str(soup.find("section", class_="entry-content"))
    content = content.removeprefix("<section class=\"entry-content cf\">")
    content = content.removesuffix("</section>")
    content = content.strip()
    group = soup.find(attrs={"property": "article:section"})
    group = group.get('content')

    writer.writerow(["Discussion", date, username, title, content, group])

    for comment in soup.find_all("li", class_="comments-comment"):
        date = comment.get("data-comment-created-date")[:10]
        username = comment.find_next("a", class_="avatar-frame")
        username = username.get('href')
        username = username.removeprefix("/members/")
        content = str(comment.find_next("div", class_="comments-text entry-content"))
        content = content.removeprefix("<div class=\"comments-text entry-content\">")
        content = content.removesuffix("</div>")

        referent = comment.find("span", class_="comments-replyingTo")
        if (referent) : # if you can find this class
            types = "Reply to a reply"
            content = "<p> @" + referent.get_text().removeprefix(" > ") + " " + content
        else :
            types = "Reply"

        writer.writerow([types, date, username, "", content, ""])

outfile.close()
infile.close()