import markdown
from bs4 import BeautifulSoup

with open("PITSelfServiceGuide2.md", "r", encoding="utf-8") as input_file:
    text = input_file.read()
html = markdown.markdown(text)

new_html = BeautifulSoup(html, "lxml")

h1 = new_html.find_all('h1')

for tag in h1:
    tag['class'] = "pmod"

h2 = new_html.find_all('h2')

for tag in h2:
    tag['class'] = "document-title"

#new_html.
#new_html.find_all("h1")['class'] = "pmod"
#new_html.find_all("h2")['class'] = "document-title"
#new_html.find("h3")['class'] = "heading"
#new_html.find("table")['class'] = "table"
#new_html.find("ul")['class'] = "list-group"
#new_html.find("li")['class'] = "list-group-item"

with open("PITSelfServiceGuide2.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
    output_file.write(str(new_html))