from bs4 import BeautifulSoup
import requests
from base64 import b64decode

directory = "Torrents/"
login_token = ""
category = "litrpg"

headers = {'Cookie':f'PHPSESSID={login_token}'}

base_url = "http://audiobookbay.nl"
url = f"{base_url}/audio-books/type/{category}/"

html = requests.get(url).text
tree = BeautifulSoup(html, 'lxml')

pages = int(tree.find('a', {'title':'»»'}).get("href").split("/")[-2])
print(f"Downloading: {pages} pages")

torrent_links = []
for page_number in range(1,pages+1):
    if page_number == 1:
        page_url = url
    else:
        page_url = f"{url}page/{page_number}/"
    html = requests.get(page_url, headers=headers).text
    tree = BeautifulSoup(html, 'lxml')
    no_base_64 = [span.find('a',{'rel':'nofollow'}).get('href').replace('dl-now','download') for span in tree.find_all('span',{'class':'postComments'})]
    base_64 = [BeautifulSoup(b64decode(div.text),'lxml').find('a',{'rel':'nofollow'}).get('href').replace('dl-now','download') for div in tree.find_all('div',{'class':'post re-ab'})]
    torrent_links.extend(no_base_64)
    torrent_links.extend(base_64)
    print(f"Downloaded: page {page_number}")

print(torrent_links)
print(len(torrent_links))

for torrent_link in torrent_links:
    download_link = base_url+torrent_link
    print(download_link)
    response = requests.get(download_link, headers=headers)
    torrent_data = response.content
    with open(directory+response.headers['Content-Disposition'].split("=")[1].strip('"'), "wb") as file:
        file.write(torrent_data)
