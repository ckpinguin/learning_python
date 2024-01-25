from bs4 import BeautifulSoup


with open("website.html", "r") as file:
    contents = file.read()

soup = BeautifulSoup(contents, "html.parser")

all_anchor_tags = soup.find_all(name="a")
for tag in all_anchor_tags:
    # print(tag)
    # print(tag.get("href"))
    pass

heading = soup.find(name="h1", id="name")
# print(heading)

section_heading = soup.find(name="h3", class_="heading")
# print(section_heading)

company_url = soup.select(selector=".heading")
print(company_url)
