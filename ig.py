import json
import shutil
import requests as r
from bs4 import BeautifulSoup
from argparse import ArgumentParser

def save_file(url, filename):
	raw = r.get(url, stream=True)
	with open(filename, 'wb') as f:
		shutil.copyfileobj(raw.raw, f)

def get_content(url):
	url = r.get(url).text
	bs = BeautifulSoup(url, 'html.parser')
	script = bs.find_all('script')[2].text
	content = json.loads(script.split(' = ')[1][:-1])
	if 'edge_sidecar_to_children' in url:
		c = content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
		for i in range(len(c)):
			if 'video_url' in str(c[i]):
		 		t = "VID"
		 		c = content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges'][i]['node']['video_url']
		 		save_file(c, c.split('/')[-1])
		 		print("[%s] from username %s\nsaved to %s" %(t, content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username'], c.split('/')[-1]))
			else:
				t = "IMG"
				c = content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges'][i]['node']['display_url']
				save_file(c, c.split('/')[-1])
				print("[%s] from username %s\nsaved to %s" %(t, content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username'], c.split('/')[-1]))
	else:
		if 'video_url' in url:
			t = "VID"
			c = content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['video_url']
		else:
			t = "IMG"
			c = content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['display_url']
		save_file(c, c.split('/')[-1])
		print("[%s] from username %s\nsaved to %s" %(t, content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username'], c.split('/')[-1]))

def fetch_profile(url):
	url = r.get(url).text
	bs = BeautifulSoup(url, 'html.parser')
	script = bs.find_all('script')[2].text
	content = json.loads(script.split(' = ')[1][:-1])
	basic = bs.find_all(attrs={'property':'og:description'})[0]['content'].split(' - ')[0]
	full_name = content['entry_data']['ProfilePage'][0]['graphql']['user']['full_name']
	uname = content['entry_data']['ProfilePage'][0]['graphql']['user']['username']
	priv = content['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']
	hd_pic = content['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd']
	result = {'basic':basic, 'full_name':full_name, 'uname':uname, 'priv':priv, 'hd_pic':hd_pic}
	return result

def display_info(data):
	info = "[+] Username: %s\n[+] Full Name: %s\n[+] Private Account: %s\n[+] Other: %s" %(data['uname'], data['full_name'], data['priv'], data['basic'])
	print(info)

def save_pp(data):
	save_file(data['hd_pic'], data['hd_pic'].split('/')[-1])
	print("%s profile picture saved to %s" %(data['uname'], data['hd_pic'].split('/')[-1]))

if __name__ == '__main__':
	parser = ArgumentParser(description="Simple Instagram Toolkit")
	parser.add_argument('-u', '--url', dest="url", help="Save image from instagram's post URL")
	parser.add_argument('-i', '--info', dest="info", help="Retrieve data from given username")
	parser.add_argument('-p', '--profile-pic', dest="pp", help="Save profile photo from given username")
	args = parser.parse_args()

	if args.url != None:
		get_content(args.url)
	elif args.info != None:
		display_info(fetch_profile(args.info))
	elif args.pp != None:
		save_pp(fetch_profile(args.pp))
