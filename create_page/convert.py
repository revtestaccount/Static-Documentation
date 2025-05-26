import markdown
from bs4 import BeautifulSoup

with open("demodocument.md", "r", encoding="utf-8") as input_file:
    text = input_file.read()
html = markdown.markdown(text, extensions=['fenced_code', 'tables'])

new_html = BeautifulSoup(html, "lxml")

h1 = new_html.find_all('h1')

for tag in h1:
    tag['class'] = "document-title"
    tag['id'] = "title"

h2 = new_html.find_all('h2')

for tag in h2:
    id = tag.contents[0].replace(" ", "_").lower()
    tag['class'] = "pmod"
    tag['id'] = id

h3 = new_html.find_all('h3')

for tag in h3:
    id = tag.contents[0].replace(" ", "_").lower()
    tag['class'] = "pmod"
    tag['id'] = id

h4 = new_html.find_all('h4')

for tag in h4:
    id = tag.contents[0].replace(" ", "_").lower()
    tag['class'] = "pmod"
    tag['id'] = id

table = new_html.find_all('table')

for tag in table:
    tag['class'] = "table"

# create table of contents
toc_heading = new_html.new_tag("h2")
toc_heading.string = "Table of Contents"
toc_heading['class'] = "pmod"
new_html.find(id="title").insert_after(toc_heading)

toc = new_html.new_tag('ul')
toc['id'] = "toc"
toc_heading.insert_after(toc)

all = new_html.find_all()

for tag in all:

    if tag.name == 'h2': # duplicated code here, to do / clean up after styling for toc is determined
        item = new_html.new_tag('li')
        link = new_html.new_tag('a')
        link['href'] = "javascript:void(0)"
        link['onclick'] = "document.getElementById(\'" + str(tag.get('id')) + "\').scrollIntoView()"
        link.string = tag.contents[0]
        item.append(link)
        new_html.find(id="toc").append(item)
    if tag.name == 'h3':
        item = new_html.new_tag('li')
        link = new_html.new_tag('a')
        link['href'] = "javascript:void(0)"
        link['onclick'] = "document.getElementById(\'" + str(tag.get('id')) + "\').scrollIntoView()"
        link.string = tag.contents[0]
        item.append(link)
        new_html.find(id="toc").append(item)
    if tag.name == 'h4':
        item = new_html.new_tag('li')
        link = new_html.new_tag('a')
        link['href'] = "javascript:void(0)"
        link['onclick'] = "document.getElementById(\'" + str(tag.get('id')) + "\').scrollIntoView()"
        link.string = tag.contents[0]
        item.append(link)
        new_html.find(id="toc").append(item)

with open("demodocument.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
    output_file.write(str(new_html))