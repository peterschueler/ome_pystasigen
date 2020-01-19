#!/usr/bin/env python3
import os
import argparse
from datetime import datetime
from pathlib import Path

from settings import PUBLICATION_QUEUE
from generate_html import generate_site
from generate_images import generate_photography

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--settings_dir', help='Specifies a custom settings script. (Does not work yet!)')
parser.add_argument('-t', '--template_dir', help='Specifies a custom template directory. (Does not work yet!)')
parser.add_argument('-o', '--output_dir', help='Specifices a custom output directory. (Does not work yet!)')
parser.add_argument('-p', '--publish', help='Specifies a Markdown draft to publish.')
parser.add_argument('-r', '--regenerate', help='Regenerates the site.', action='store_true')
parser.add_argument('-i', '--publish_images', help='Generates thumbnails and publishes all images.')
args = parser.parse_args()

def publish_post(post):
	file = Path(post)
	with open(file, 'r') as _p:
		current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
		name = file.stem
		data = _p.read()

		Path(PUBLICATION_QUEUE).mkdir(parents=True, exist_ok=True)
		with open("{}/{}_{}.md".format(PUBLICATION_QUEUE, current_date, name), 'w') as _f:
			_f.write(data)
		file.unlink()

def main():
	if args.publish != None:
		publish_post(args.publish)
		generate_site()
	if args.regenerate != None:
		generate_site()
		generate_photography()
	if args.publish_pictures != None:
		generate_photography()

if __name__ == '__main__':
	main()