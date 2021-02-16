import requests
import json
import time
from bs4 import BeautifulSoup
url = "https://x-oasis.com/casts"
html = requests.get(url)
data = BeautifulSoup(html.text, "html.parser")

casts = [cast.text for cast in data.select(".cast-title > span > a")]

casts_link = ["https://x-oasis.com" + cast['href'] for cast in data.select(".cast-title > span > a")]

casts_elements_array = []
casts_elements = data.select(".cast-elements > div > ul")
for elements in casts_elements:
    array = []
    for element in elements:
        if element != '\n':
            array.append(element.text)
    casts_elements_array.append(array)

casts_play_titles_array = []
for link in casts_link:
    cast_html = requests.get(link)
    time.sleep(1)
    cast_data = BeautifulSoup(cast_html.text, "html.parser")
    cast_play_titles = cast_data.select(".play-title")
    array = []
    for cast_play_title in cast_play_titles:
        array.append(cast_play_title.text.replace('（', '(').replace('）', ')'))
    casts_play_titles_array.append(array)

all_casts_datas = []
for index, cast in enumerate(casts):
    all_casts_datas.append({"cast" : casts[index], "url" : casts_link[index], "elements" : casts_elements_array[index], "plays" : casts_play_titles_array[index]})

with open('index.json', 'w' ,encoding="utf_8") as f:
    f.write(json.dumps(all_casts_datas, sort_keys=True, ensure_ascii=False, indent=2))