#!python

import requests
from bs4 import BeautifulSoup
import sys
import os
import json

import subprocess

youtube = "https://www.youtube.com"
useragent = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

def search_query():
    entered_query = input('Please enter the name of the YouTube video: ')
    query = entered_query.split(' ')
    query = '+'.join(query)
    
    search_url  = youtube + "/results?search_query=" + query
    search_response = requests.get(search_url, headers=useragent)
    if search_response.status_code == 200:
        print(f'Query was successful for "{entered_query}".')
    soup = BeautifulSoup(search_response.content, "html.parser")
    title = []
    ref = []
    all_title_tags = soup.find_all("h3", attrs={"class": "yt-lockup-title"})

    if len(all_title_tags) > 0:    
        title = all_title_tags[0].find('a').contents[0].contents[0]
        video_url = youtube + all_title_tags[0].find('a')['href']
        print('Title:',title)
        print('URL:',video_url)
        return video_url, title
    else:
        print('No results.')
        return None 


def download_from_url(url,title,saveto=None): 
    if saveto != None:
        if not os.path.exists(saveto): os.mkdir(saveto)
        save_dir = saveto
    else:
        save_dir = './'
    
    p = subprocess.Popen(f'youtube-dl -f "bestaudio[ext=m4a]" {url} -o "{os.path.join(save_dir,title)}.m4a"', stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    print(f'Download complete for "{title}"')

def download_from_playlist_url(playlist_url):
    playlist_response = requests.get(playlist_url, headers=useragent)
    playlist_soup = BeautifulSoup(playlist_response.content, "html.parser")
    items = playlist_soup.find_all("li", attrs={"class": "yt-uix-scroller-scroll-unit"})
    playlist_videos = []
    for item in items:
        video_dict = {}
        video_dict['id'] = item['data-video-id']
        video_dict['title'] = item['data-video-title']
        playlist_videos.append(video_dict)

    if len(playlist_videos) == 0:
        print('Invalid URL')
        sys.exit('Please provide a valid URL to a YouTube playlist.')

    for video in playlist_videos:
        id,title = video['id'],video['title']
        vid_url = youtube+'/watch?v='+id
        download_from_url(vid_url, title, 'playlist')

if __name__ == "__main__":
    print('2 modes are currently available:')
    print('1. Search for and download a song.')
    print('2. Download all songs from a playlist.')

    inp = None
    while inp not in ['1','2']:
        print('Make a choice that corresponds to the option numbers.')
        inp = input('Which option do you fancy? > ')
    if inp == '1':
        while True:
            download_from_url(*search_query(),'music')
            print('='*60,'\n')
            print('Would you like to do another?')
    elif inp == '2':
        print('Give us the URL to the playlist, e.g. https://www.youtube.com/watch?v=VagES3pxttQ&list=PLh9R0KdDnt86-neT6YyJCAAp-Wrz4jVcg')
        playlist_url = input('> ')

        download_from_playlist_url(playlist_url)