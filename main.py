from bs4 import BeautifulSoup
import requests
from base64 import b64decode
from config_loader import settings
import os
import time

categories = settings['categories'].split(",")
tags = settings['tags'].split(",")
search_terms = settings['search_terms'].split(",")
search_extras = settings['search_extras'].split(",")

headers = {'Cookie':f'PHPSESSID={settings["login_token"]}','user-agent':settings['user_agent']}

def init():
    global torrent_links
    torrent_links = []
    if not os.path.exists(settings['directory']):
        os.makedirs(settings['directory'])

def load_history():
    global history
    history = []
    try:
        with open(settings['torrent_list'], "r") as file:
            for download_url in file:
                download_url = download_url.strip()
                if download_url not in history:
                    history.append(download_url)
    except:
        pass

def save_history():
    try:
        with open(settings['torrent_list'], "w") as file:
            for download_url in history:
                download_url = download_url.strip()
                file.write(download_url+"\n")
    except Exception as e:
        print(e,"error saving, dumping history")
        print(history)

def download_link(download_url):
    try:
        response = requests.get(download_url, headers=headers)
        torrent_data = response.content
        with open(settings['directory']+response.headers['Content-Disposition'].split("=")[1].strip('"'), "wb") as file:
            file.write(torrent_data)
        if not settings['silent']:
            print(download_url)
        history.append(download_url)
    except KeyError:
        print("Did you forget to add your login_token in the config?")
        quit()
    except Exception as e:
        print(e)
        download_link(download_url)
        
def download_links():
    for torrent_link in torrent_links:
        download_url = settings['base_url']+torrent_link
        if download_url not in history or not settings['avoid_duplicates']:
            download_link(download_url)

def get_links(url,normal=True):
    html = requests.get(url).text
    tree = BeautifulSoup(html, 'lxml')

    pages = int(tree.find('a', {'title':'»»'}).get("href").split("/")[-2])
    if not settings['silent']:
        if normal:
            print(f"Downloading: {pages} pages of {url.split('/')[-2]}")
        else:
            print(f"Downloading: {pages} pages of {url.split('/')[-1]}")

    for page_number in range(1,pages+1):
        try:
            if page_number == 1:
                page_url = url
            else:
                if normal:
                    page_url = f"{url}page/{page_number}/"
                else:
                    page_url = f"{base_url}page/{page_number}/{url.split(base_url)[1]}"
            html = requests.get(page_url, headers=headers).text
            tree = BeautifulSoup(html, 'lxml')
            no_base_64 = [span.find('a',{'rel':'nofollow'}).get('href').replace('dl-now','download') for span in tree.find_all('span',{'class':'postComments'})]
            base_64 = [BeautifulSoup(b64decode(div.text),'lxml').find('a',{'rel':'nofollow'}).get('href').replace('dl-now','download') for div in tree.find_all('div',{'class':'post re-ab'})]
            torrent_links.extend(no_base_64)
            torrent_links.extend(base_64)
            if not settings['silent']:
                print(f"Downloaded: page {page_number}")
        except:
            get_links(url,normal)

def get_category(category):
    if category:
        url = f"{settings['base_url']}/audio-books/type/{category}/"
        get_links(url)

def get_tag(tag):
    if tag:
        url = f"{settings['base_url']}/audio-books/tag/{tag}/"
        get_links(url)

def get_search_term(search_term,search_extra=None):
    if search_term:
        url = f"{settings['base_url']}/?s={search_term}"
        if search_extra:
            url+=search_extra
        get_links(url,False)

load_history()

while True:
    init()
    
    for category in categories:
        get_category(category)
    for tag in tags:
        get_tag(tag)
    for search_term,search_extra in zip(search_terms,search_extras):
        get_search_term(search_term,search_extra)

    download_links()
    save_history()
    
    if not settings['auto_run']:
        break
    if not settings['silent']:
        print(f"Searching again in {int(settings['wait_time'])/3600} hours.")
    time.sleep(int(settings['wait_time']))
