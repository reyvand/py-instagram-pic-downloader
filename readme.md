
# Simple Instagram Toolkit

### Features
- Save single/multiple image
- Save single/multiple video
- Display basic information for given username
- Save profile picture from given username (in 320x320 dimension)
- Save all available post for given username (not private account) [bug]
- Load cookie from file (you must save a full cookie from authenticated user into a file)

### Usage
```sh
usage: ig.py [-h] [-u URL] [-i INFO] [-p PP] [-a ALL] [-c COOKIE]

Simple Instagram Toolkit

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Save image from instagram's post URL
  -i INFO, --info INFO  Retrieve data from given username
  -p PP, --profile-pic PP
                        Save profile photo from given username
  -a ALL, --save-all ALL
                        Save all posts picture/video from given username
  -c COOKIE, --cookie COOKIE
                        Load cookie from file
```

### Example
```sh
$ python ig.py -u https://www.instagram.com/p/BfcIuhQnMKt/?taken-by=9gag
[IMG] from username 9gag
saved to 28157065_139303333552258_3669066724180754432_n.jpg
$ python ig.py -i https://www.instagram.com/reyvand__/
[+] Username: reyvand__
[+] Full Name: reyvand
[+] Private Account: False
[+] Other: 137 Followers, 172 Following, 12 Posts
$ python ig.py -p https://www.instagram.com/reyvand__/
reyvand__ profile picture saved to 24274132_142176299768499_8138924706221785088_n.jpg
```

### Requirements
* Python3
* Libraries :
	* os
	* json
  * shutil
  * requests
  * bs4
  * argparse
