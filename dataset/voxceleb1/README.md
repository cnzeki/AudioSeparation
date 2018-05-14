# VoxCeleb multithread downloader

## Tools

- install ffmpeg
- run `python get_youtube-dl.py` to get the latest version to `youtube-dl` tool for downloading `youtube`  resources

## Steps

1. Download files from http://www.robots.ox.ac.uk/~vgg/data/voxceleb/ 
  download vexceleb1.zip , extract here to get the `list.txt` file

2. Run
```
python download_mp3.py list.txt
```

​	downloaded files will be in the `mp3` directory.