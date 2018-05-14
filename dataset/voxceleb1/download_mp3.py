# -*- coding:utf-8 -*-  
from __future__ import print_function
import re
import random
import sys
import os
import requests
import threadpool

def makedirs(path):
    dir,fname = os.path.split(path)
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except:
            pass
            
def download_url(url, path):
    r = requests.get(url) 
    with open(path, "wb") as f:
        f.write(r.content)
        

def process_line(line, dst_dir):
    line = line.strip()
    dst_path = '%s\\%s.mp3' % (dst_dir,line)
    if os.path.exists(dst_path):
        print('Skip %s' % (line))
        return True
    cmd_str = '..\\youtube-dl.exe --extract-audio --audio-format mp3 --audio-quality 1 --output %s\\%s.mp3 %s' % (dst_dir,line,line)
    #p = os.popen(cmd_str)  
    p = os.system(cmd_str)  
    #print(cmd_str)
    #print(p.read())
    return True
    
def download_filelist_st(log_file,dst_dir):  
    f = open(log_file,'r')
    # skip header
    f.readline()
    # records
    for line in f.readlines():
        process_line(line, dst_dir)
    f.close()

def download_filelist_mt(log_file,dst_dir, threads = 3):  
    f = open(log_file,'r')
    # skip header
    f.readline()
    # records
    data = []
    start = True
    for line in f.readlines():
        line = line.strip()
        #if line == 'gmq3OrirtfY':
        #    start = True
        if start:
            data.append(((line, dst_dir),None))
    f.close()
    # add to pool
    pool = threadpool.ThreadPool(threads)
    reqs = threadpool.makeRequests(process_line, data)
    [pool.putRequest(req) for req in reqs]
    pool.wait()
    
    
if __name__ == '__main__':
    list_file = sys.argv[1]
    dst_dir = 'mp3'
    if len(sys.argv) > 2:  
        dst_dir = sys.argv[2]
    download_filelist_mt(list_file, dst_dir)