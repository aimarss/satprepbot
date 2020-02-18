from bs4 import BeautifulSoup
import lxml
import json

words = []
with open("words.txt") as f:
    soup = BeautifulSoup(f, "lxml")
    trs = soup.find_all("tr")
    for tr in trs:
        word = ""
        for i, child in enumerate(tr.children):
            if i == 5:
                word = child.string
        words.append(word)

with open("meanings.txt", "w+") as f:
    json.dump(words, f)
