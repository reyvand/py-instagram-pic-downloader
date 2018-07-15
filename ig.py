import os
import json
import shutil
import requests as r
from bs4 import BeautifulSoup
from argparse import ArgumentParser

def save_file(url, filename, userdir):
	if not os.path.exists(userdir):
		os.makedirs(userdir)
	filename = userdir+"/"+filename.split('?')[0]
	raw = r.get(url, stream=True)
	with open(filename, 'wb') as f:
		shutil.copyfileobj(raw.raw, f)

def find_raw(urlcontent, cookie=''):
	if cookie != '':
		print("Load cookie from file %s" %(cookie))
		custom_header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', 'Cookie':open(cookie).read()}
	else:
		custom_header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'}
	content = BeautifulSoup(r.get(urlcontent, headers=custom_header).text, 'html.parser')
	sc = content.find_all('script')
	for s in sc:
		if 'window._sharedData = {' in s.text:
			return json.loads(s.text.split(' = ')[1][:-1])
			break

def get_content(url, cookie=''):
	try:
		content = find_raw(url, cookie)
		if 'edge_sidecar_to_children' in str(content):
			c = content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
			for i in range(len(c)):
				if 'video_url' in str(c[i]):
			 		t = "VID"
			 		c = content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges'][i]['node']['video_url']
			 		save_file(c, c.split('/')[-1], content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username'])
			 		print("[%s] from username %s\nsaved to %s/%s" %(t, content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username'], content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username'], c.split('/')[-1]))
				else:
					t = "IMG"
					c = content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges'][i]['node']['display_url']
					save_file(c, c.split('/')[-1], content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username'])
					print("[%s] from username %s\nsaved to %s/%s" %(t, content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username'], content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username'], c.split('/')[-1].split('?')[0]))
		else:
			if 'video_url' in url:
				t = "VID"
				c = content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['video_url']
			else:
				t = "IMG"
				c = content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['display_url']
			save_file(c, c.split('/')[-1], content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username'])
			print("[%s] from username %s\nsaved to %s/%s" %(t, content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username'], content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username'], c.split('/')[-1].split('?')[0]))
	except:
		print("Post not found. Maybe it's from private account ?")

def fetch_profile(url):
	content = find_raw(url)
	basic = BeautifulSoup(r.get(url).text, 'html.parser').find_all(attrs={'property':'og:description'})[0]['content'].split(' - ')[0]
	full_name = content['entry_data']['ProfilePage'][0]['graphql']['user']['full_name']
	uname = content['entry_data']['ProfilePage'][0]['graphql']['user']['username']
	priv = content['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']
	hd_pic = content['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd']
	result = {'basic':basic, 'full_name':full_name, 'uname':uname, 'priv':priv, 'hd_pic':hd_pic}
	return result

def display_info(data):
	info = "[+] Username: %s\n[+] Full Name: %s\n[+] Private Account: %s\n[+] Other: %s" %(data['uname'], data['full_name'], data['priv'], data['basic'])
	return info

def save_pp(data):
	save_file(data['hd_pic'], 'pp_'+data['hd_pic'].split('/')[-1], data['uname'])
	print("%s profile picture saved to %s" %(data['uname'], data['uname']+'/pp_'+data['hd_pic'].split('/')[-1].split('?')[0]))

def save_all(url):
	content = find_raw(url)
	info = display_info(fetch_profile(url)) 
	print(info+"\n")
	if fetch_profile(url)['priv'] == True:
		print("\nPrivate Account")
	else:
		detailuser = content['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']
		print("[-] %s total post: %s\n" %(fetch_profile(url)['uname'],detailuser['count']))
		for i in range(len(detailuser['edges'])):
			posturl = "https://instagram.com/p/"+detailuser['edges'][i]['node']['shortcode']
			get_content(posturl)


if __name__ == '__main__':
	parser = ArgumentParser(description="Simple Instagram Toolkit")
	parser.add_argument('-u', '--url', dest="url", help="Save image from instagram's post URL")
	parser.add_argument('-i', '--info', dest="info", help="Retrieve data from given username")
	parser.add_argument('-p', '--profile-pic', dest="pp", help="Save profile photo from given username")
	parser.add_argument('-a', '--save-all', dest="all", help="Save all posts picture/video from given username")
	parser.add_argument('-c', '--cookie', dest="cookie", help="Load cookie from file")
	args = parser.parse_args()

	if args.url != None:
		if args.cookie != None:
			get_content(args.url, args.cookie)
		else:
			get_content(args.url)
	elif args.info != None:
		print(display_info(fetch_profile(args.info)))
	elif args.pp != None:
		save_pp(fetch_profile(args.pp))
	elif args.all != None:
		save_all(args.all)