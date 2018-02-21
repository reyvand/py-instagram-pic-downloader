# Instagram Media Downloader

### Features
- Save single/multiple image
- Save single/multiple video

### Usage
```sh
$ python ig.py --help
$ python ig.py -u posturl
```

### Example
```sh
$ python ig.py -u https://www.instagram.com/p/BfcIuhQnMKt/?taken-by=9gag
[IMG] from username 9gag
saved to 28157065_139303333552258_3669066724180754432_n.jpg
```

### Requirements
- Python3
- Libraries :
 -- json
 -- shutil
 -- requests
 -- bs4
 -- argparse