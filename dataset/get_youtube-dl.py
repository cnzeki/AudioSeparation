# -*- coding:utf-8 -*-  
from __future__ import print_function
import requests
import os

def download(link, path='.'):
    file_name = link.split('/')[-1]

    print("Downloading file:%s" % file_name)
    r = requests.get(link, stream=True)

    # download started
    nk = 0
    dst_path = os.path.join(path, file_name)
    with open(dst_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                nk += 1
                print("\b\b\b\b\b\b\b%dKb" % (nk), end='')
                f.write(chunk)

    print("%s downloaded!\n" % file_name)
    

url ='http://www.youtube-dl.org/downloads/latest/youtube-dl'
if os.name == 'nt':
    url = url + '.exe'
download(url)
