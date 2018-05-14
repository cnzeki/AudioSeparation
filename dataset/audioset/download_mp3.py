# -*- coding:utf-8 -*-  
from __future__ import print_function
import re
import random
import sys
import os
import requests
import threadpool

def load_class_labels(label_path):
    dict = {}
    f = open(label_path,'r')
    # skip header
    f.readline()
    # records
    for line in f.readlines():
        line = line.strip()
        id_mid, name = line.split(',"')
        id, mid = id_mid.split(',')
        name = name.replace('"','')
        dict[mid] = (name,id)
    f.close()
    return dict

def makedirs(path):
    dir,fname = os.path.split(path)
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except:
            pass
                
def parse_line(line):
    line = line.strip()
    mid, start, end, names = line.split(', ')
    names = names.replace('"','')
    names = names.split(',')
    return mid, start, end, names
    
    
def process_line(line, dst_dir):
    id, start, end, names = parse_line(line)
    print("downloading %s %s %s" % (id, start,end))
    # skip if exists
    dst_path = '%s\\%s.mp3' % (dst_dir,id)
    dst_all = '%s\\%s_all.mp3' % (dst_dir,id)
    dst_clip = '%s\\%s_clip.mp3' % (dst_dir,id)
    if os.path.exists(dst_path):
        return True
    # download mps
    cmd_str = '..\\youtube-dl --extract-audio --audio-format mp3 --audio-quality 1 \
      --output \"%s\" \"https://youtube.com/watch?v=%s\" ' % (dst_all, id)
    os.system(cmd_str) 
    if not os.path.exists(dst_all):
        return False    
    # clip
    cmd_str = 'ffmpeg -loglevel quiet -y -i \"%s\" -ar 22050 \
      -ss \"%s\" -to \"%s\" \"%s\"' %(dst_all,start, end, dst_clip)
    os.system(cmd_str) 
    
    # rename
    os.rename(dst_clip, dst_path) 
    # cleanup
    os.remove(dst_all)
    #print(p.read())
    return True
    
    
def download_filelist_st(log_file,dst_dir):  
    f = open(log_file,'r')
    # skip header
    f.readline()
    f.readline()
    f.readline()
    # records
    for line in f.readlines():
        process_line(line, dst_dir)
    f.close()

def download_filelist_mt(log_file, dst_dir, class_filter=None, threads = 2):  
    f = open(log_file,'r')
    # skip header
    f.readline()
    f.readline()
    f.readline()
    # records
    data = []
    for line in f.readlines():
        line = line.strip()
        ok = True
        if class_filter:
            ok = False
            id, start, end, names = parse_line(line)
            if len(names) == 1 and names[0] in class_filter:
                ok = True
        if ok:
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
    makedirs(dst_dir)
    #class_filter = load_class_labels('select_class.csv')
    class_filter = None
    if len(sys.argv) > 2:  
        dst_dir = sys.argv[2]
    download_filelist_mt(list_file, dst_dir, class_filter, 3)