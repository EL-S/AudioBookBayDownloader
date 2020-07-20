# AudioBookBayDownloader
Download torrent/magnet files from ABB

The config contains many configurable values to alter the functionality of the script.
Duplicates are currently ignored on separate runs, however, a full scan is still required for now.
All requirements can be quickly installed with 'pip install -r requirements.txt'.
Open an issue if you have a feature request or a problem!

Requirements:

* beautifulsoup4==4.9.1
* bs4==0.0.1
* lxml==4.5.0
* requests==2.23.0

Considering the following features:
* An automatic 'all' category for downloading every magnet
* Threading
* Automatic folder sorting
* Progress bars
* Test if login token works before a scan
* Option between magnet and torrent file in the config

Here is an example config (all fields are required):

```
directory:Torrents/
login_token:your token here (get it from browser cookies)
base_url:http://audiobookbay.nl
avoid_duplicates:True
user_agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36
categories:litrpg,postapocalyptic
tags:english
search_terms:a
search_extras:&cat=36021%2C-121
auto_run:True
wait_time:3600
torrent_list:list.txt
silent:False
```

The wait time is in seconds.
I recommend not using the search terms at all unless you understand the inclusion and exclusion extras, use the following below for a specific category:

```
directory:Torrents/
login_token:your token here (get it from browser cookies)
base_url:http://audiobookbay.nl
avoid_duplicates:True
user_agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36
categories:litrpg
tags:
search_terms:
search_extras:
auto_run:True
wait_time:3600
torrent_list:list.txt
silent:False
```

Currently tags, search_terms and categories are all handled separately, but it is possible I might add a custom url and url formatter as an option.

The availiable genres to request are the same as the url of the page. A quick list can be found below:

* Postapocalyptic
* Action
* Adventure
* Art
* Autobiography-Biographies
* Business
* Computer
* Contemporary
* Crime
* Detective
* Doctor-Who-sci-fi
* Education
* Fantasy
* General-Fiction
* Historical-Fiction
* History
* Horror
* Humor
* Lecture
* LGBT
* Literature
* LitRPG
* General-Non-fiction
* Mystery
* Paranormal
* Plays-Theater
* Poetry
* Political
* Radio-Productions
* Romance
* Sci-Fi
* Science
* Self-help
* Spiritual & Religious
* Sports
* Suspense
* Thriller
* True-Crime
* Tutorial
* Westerns

The following 'Category Modifiers' should also work:


* Anthology
* Bestsellers
* Classic
* Documentary
* Full-Cast
* Libertarian
* Military
* Novel
* Short-Story

As should the following 'Age' Categories:

* Children
* Teen & Young Adult
* Adults
* The Undead
