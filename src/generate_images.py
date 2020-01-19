from pathlib import Path
from PIL import Image

from _settings import *
		
def generate_thumbnails(image_dir, sizes):
	image_list = [p for p in Path(image_dir).iterdir() if p.is_file() and \
		'thumb' not in p.name and p.suffix == '.jpg']
	for img in image_list:
		try:
			for sz in sizes.items():
				thumb_name = '{}/{}_thumb_{}{}'.format(image_dir, img.stem, sz[0], img.suffix)
				if Path(thumb_name).is_file() == False:				
					thumb = Image.open(img)
					thumb.thumbnail(sz[1])
					thumb.save(thumb_name)
		except IOError:
			pass
			
def generate_relative_links(image_dir):
	image_list = [p for p in Path(image_dir).iterdir() if p.is_file() and \
		'thumb' not in p.name and p.suffix == '.jpg']
	imgs = {}
	for img in image_list:
		imgs[img.stem] = {'full': "{}/{}".format(PHOTOGRAPHY_URL, img.name), \
							'large': "{}_thumb_{}{}".format(img.stem, 'large', img.suffix),
							'medium': "{}_thumb_{}{}".format(img.stem, 'medium', img.suffix),
							'small': "{}_thumb_{}{}".format(img.stem, 'small', img.suffix)}
	return imgs
	
def generate_html_list(images):
	html = "\t<div class=image-box>\n"
	for img in images.items():
		print(img)
		img_tag = "\t\t<a href={}><img src='{}' class=image /></a>\n".format(img[1]['full'], img[1]['medium'])
		html += img_tag
	html += "\n\t</div>"
	return html
	
def generate_html_for_image(image):
	return "\t<img src='{}/{}' class=image />\n".format(PHOTOGRAPHY_URL, image)
	
def generate_photography_site(path_to_template):
	images = generate_html_list(generate_relative_links(IMAGE_DIRECTORY))
	with open(path_to_template, 'r') as _template:
		_str = _template.read()
		_str = _str.replace('<!#SITE_URL>', SITE_URL).replace('<!#SITE_TITLE#>', SITE_TITLE) \
					.replace('<!#SITE_DESCRIPTION#>', SITE_DESCRIPTION).replace('<!#IMAGES#>', images)
		with open('photography.html', 'w') as _target:
			_target.write(_str)
			
def generate_picture_site(path_to_template, image):
	img_html = generate_html_for_image(image)
	with open(path_to_template, 'r') as _template:
		_str = _template.read()
		_str = _str.replace('<!#SITE_URL>', SITE_URL).replace('<!#SITE_TITLE#>', SITE_TITLE) \
					.replace('<!#SITE_DESCRIPTION#>', SITE_DESCRIPTION).replace('<!#IMAGE#>', img_html)
		with open('{}/{}.html'.format(PHOTOGRAPHY_URL, image), 'w') as _target:
			_target.write(_str)
			
def generate_photography():
	generate_thumbnails(IMAGE_DIRECTORY, THUMBNAIL_SIZES)
	image_list = [p for p in Path(IMAGE_DIRECTORY).iterdir() if p.is_file() and \
		'thumb' not in p.name and p.suffix == '.jpg']
	for img in image_list:
		generate_picture_site(TEMPLATE_DIRECTORY + "/picture.html", img.stem)
	generate_photography_site(TEMPLATE_DIRECTORY + "/photography.html")