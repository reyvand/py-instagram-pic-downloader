import json
import shutil
import requests as r
from bs4 import BeautifulSoup
from argparse import ArgumentParser

def save_file(url, filename):
	raw = r.get(url, stream=True)
	#ext = "."+raw.headers['Content-Type'].split('/')[1]
	with open(filename, 'wb') as f:
		shutil.copyfileobj(raw.raw, f)

def get_image(url):
	url = r.get(url).text
	bs = BeautifulSoup(url, 'html.parser')
	script = bs.find_all('script')[2].text
	content = json.loads(script.split(' = ')[1][:-1])
	if 'edge_sidecar_to_children' in url:
		c = content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
		for i in range(len(c)):
			if 'video_url' in str(c[i]):
		 		print(content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges'][i]['node']['video_url'])
			else:
				print(content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges'][i]['node']['display_url'])
	else:
		if 'video_url' in url:
			t = "VID"
			c = content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['video_url']
		else:
			t = "IMG"
			c = content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['display_url']
		save_file(c, c.split('/')[-1])
		print("[%s] from username %s\nsaved to %s" %(t, content['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username'], c.split('/')[-1]))

if __name__ == '__main__':
	parser = ArgumentParser(description="Instagram Picture/Video Downloader")
	parser.add_argument('-u', '--url', dest="url", help="Instagram's post URL")
	args = parser.parse_args()

	get_image(args.url)