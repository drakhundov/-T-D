import os

import requests
from bs4 import BeautifulSoup, Tag

os.system("rm -f $(ls -a | grep txt)")

URL = "https://www.sis.itu.edu.tr/TR/ogrenci/ders-programi/ders-programi.php?seviye=LS"
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
# codes like AKM, SNT used for class names.
class_codes_lst = [
    child["value"]
    for child in list(soup.find(attrs={"name": "derskodu"}).children)
    if isinstance(child, Tag)
]
del class_codes_lst[0]
header = None
for class_code in class_codes_lst:
    response_file_name = f"{class_code.lower()}.txt"
    response_file = open(response_file_name, "w")
    class_page = requests.get(URL + f"&derskodu={class_code}").text
    soup = BeautifulSoup(class_page, "html.parser")
    class_table = soup.find("table")
    if header is None:
        header = []
        for col in class_table.find_all("tr")[1].children:
            header.append(col.text)
    rows = list(class_table.children)[2:]
    if len(rows) == 1:
        response_file.close()
        os.remove(response_file_name)
        continue
    # skip the heades.
    for row in rows:
        if row != " ":
            for i, col in enumerate(row.children):
                response_file.write(f"{header[i]}: {col.text}\n")
                print(f"{header[i]}: {col.text}")
            response_file.write("\n\n\n")
            print("\n\n\n")
    response_file.close()
