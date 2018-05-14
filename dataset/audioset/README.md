# AudioSet multithread downloader

## Tools

- install ffmpeg
- run `python get_youtube-dl.py` to get the latest version to `youtube-dl` tool for downloading `youtube`  resources

## Steps

1. Download meta files from https://research.google.com/audioset/ including:
```
balanced_train_segments.csv
class_labels_indices.csv
unbalanced_train_segments.csv [optional]
```

2. To download `balanced` set run:
```
python balanced_train_segments.csv
```
 	audio files will be in the `mp3` dir

3. To download the `unbalanced` set , run with `python balanced_train_segments.csv` 

