import markdown
from bs4 import BeautifulSoup

with open("C:\Users\\ademps03\Desktop\static documentation project\md\demodocument.md", "r", encoding="utf-8") as input_file:
    text = input_file.read()
html = markdown.markdown(text, extensions=['fenced_code', 'tables'])

new_html = BeautifulSoup(html, "lxml")

tableOfContents = []
id = ""

#tocHeading = new_html.new_tag("h1")
#tocHeading['id'] = "toc_heading"
#new_html.

h1 = new_html.find_all('h1')

for tag in h1:
    tag['class'] = "document-title"
    tag['id'] = "xxx"

h2 = new_html.find_all('h2')

for tag in h2:
    id = tag.contents[0].replace(" ", "_").lower()
    tag['class'] = "pmod"
    tag['id'] = id
    tableOfContents.append(id)

h3 = new_html.find_all('h3')

for tag in h3:
    id = tag.contents[0].replace(" ", "_").lower()
    tag['class'] = "pmod"
    tag['id'] = id
    tableOfContents.append(id)

h4 = new_html.find_all('h4')

for tag in h4:
    id = tag.contents[0].replace(" ", "_").lower()
    tag['class'] = "pmod"
    tag['id'] = id
    tableOfContents.append(id)

table = new_html.find_all('table')

for tag in table:
    tag['class'] = "table"

# finished setting up tags, generate table of contents
for id in tableOfContents:
    newAnchor = new_html.new_tag("a")
    newAnchor['href'] = "javascript:void(0)"
    newAnchor['onclick'] = "document.getElementById(\'" + id + "\').scrollIntoView()"
    newAnchor.append(id)
    #new_html.append(newAnchor)
    new_html.find(id="xxx").append(newAnchor)





#code = new_html.find_all('code')
# <a href="javascript:void(0)" onclick="document.getElementById('here').scrollIntoView()">go here</a>

#for tag in code:
#    tag['class'] = "border border-info"

with open("C:\Users\\ademps03\Desktop\static documentation project\md\demodocument.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
    output_file.write(str(new_html))