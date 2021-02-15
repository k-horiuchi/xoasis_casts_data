import requests
import json
import time
from bs4 import BeautifulSoup
url = "https://x-oasis.com/casts"
html = requests.get(url)
data = BeautifulSoup(html.text, "html.parser")

# キャスト一覧を取得
casts = [cast.text for cast in data.select(".cast-title > span > a")]
### print(casts)

# キャスト一覧のURLを取得
casts_link = ["https://x-oasis.com" + cast['href'] for cast in data.select(".cast-title > span > a")]
### print(casts_link)

# キャストの属性を取得
casts_elements = data.select(".cast-elements > div > ul")
casts_elements_array = []
for elements in casts_elements:
    array = []
    for element in elements:
        if element != '\n':
            array.append(element.text)
    casts_elements_array.append(array)
### print(casts_elements_array)

# キャストの対応可能範囲を取得
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
### print(casts_play_titles_array)

# キャストごとに情報をjson化させる
all_casts_datas = []
for index, cast in enumerate(casts):
    casts_datas = []
    casts_datas.append({"url" : casts_link[index]})
    casts_datas.append({"elements" : casts_elements_array[index]})
    casts_datas.append({"play" : casts_play_titles_array[index]})
    all_casts_datas.append({casts[index] : casts_datas})

with open('index.json', 'w' ,encoding="utf_8") as f:
    f.write(json.dumps(all_casts_datas, sort_keys=True, ensure_ascii=False, indent=2))