import markdown
from bs4 import BeautifulSoup

with open("././md/pat.md", "r", encoding="utf-8") as input_file:
    text = input_file.read()
html = markdown.markdown(text, extensions=['fenced_code', 'tables'])

new_html = BeautifulSoup(html, "lxml")

#print(new_html)

h1 = new_html.find_all('h1')

for tag in h1:
    tag['class'] = "pmod"

h2 = new_html.find_all('h2')

for tag in h2:
    tag['class'] = "document-title"

#code = new_html.find_all('code')

#for tag in code:
#    tag['class'] = "border border-info"

with open("././md/pat.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
    output_file.write(str(new_html))