#!/usr/bin/env python3
import re
import os
from pathlib import Path
from datetime import datetime

from _settings import *

def generate_site():
	''' Traverses the PUBLICATION_QUEUE and calls generate_post on items. Then calls generate_index.'''
	feed_posts = []
	archive_items = []
	add_basics("{}/style.css".format(TEMPLATE_DIRECTORY))
	Path(PUBLICATION_QUEUE).mkdir(parents=True, exist_ok=True)
	for _file in sorted(Path(PUBLICATION_QUEUE).iterdir(), key=lambda f: f.stem, reverse=True):
		if _file.stem == '.DS_Store':
			# TODO: Replace with actual safeguard against badly formed filenames.
			continue
		else:
			generate_post(_file, "{}/post_template.html".format(TEMPLATE_DIRECTORY))
			feed_posts.append(generate_feed_item(_file, '{}/feed_item_template.xml'.format(TEMPLATE_DIRECTORY)))
			archive_items.append(generate_archive_item(_file, '{}/archive_item_template.html'.format(TEMPLATE_DIRECTORY)))
	generate_index(PUBLISHED_DIRECTORY, "{}/index_template.html".format(TEMPLATE_DIRECTORY))
	generate_about("{}/about.html".format(TEMPLATE_DIRECTORY))
	generate_feed(feed_posts, "{}/feed_template.xml".format(TEMPLATE_DIRECTORY))
	generate_archive(archive_items, "{}/archive_template.html".format(TEMPLATE_DIRECTORY))

def add_basics(path_to_style):
	with open(path_to_style, 'r') as _st:
		with open('style.css', 'w') as _target:
			_target.write(_st.read())

def generate_about(path_to_about):
	with open(path_to_about, 'r') as _ab:
		_str = _ab.read()
		_str = _str.replace('<!#SITE_URL#>', SITE_URL) \
							.replace('<!#SITE_TITLE#>', SITE_TITLE) \
							.replace('<!#SITE_DESCRIPTION#>', SITE_DESCRIPTION)
		with open('about.html', 'w') as _target:
			_target.write(_str)

def generate_index(published_path, template_path):
	''' Takes the published files and generates the homepage for the blog. '''
	articles = []
	for _file in sorted(Path(published_path).iterdir(), key=lambda f: f.stat().st_mtime):
		with open(_file, 'r') as _f:
			_str = _f.read()
			matched = re.findall(r'<article>[\s\S]+<\/article>', _str, re.MULTILINE)
			if matched:
				articles.append(matched[0])

	with open(template_path, 'r') as _t:
		_str = _t.read()
		_str = _str.replace('<!#SITE_URL#>', SITE_URL) \
							.replace('<!#SITE_TITLE#>', SITE_TITLE) \
							.replace('<!#SITE_DESCRIPTION#>', SITE_DESCRIPTION)
		_str = _str.replace('<!#ARTICLES#>', '\n'.join(articles[:15]))

		with open('index.html', 'w') as _index:
			_index.write(_str)

def generate_archive(archive_links, template_path):
	''' Takes the published files and generates a list of articles. '''

	with open(template_path, 'r') as _t:
		_str = _t.read()
		_str = _str.replace('<!#SITE_URL#>', SITE_URL) \
							.replace('<!#SITE_TITLE#>', SITE_TITLE) \
							.replace('<!#SITE_DESCRIPTION#>', SITE_DESCRIPTION)
		_str = _str.replace('<!#POST_LINKS#>', '\n'.join(archive_links))

		with open('blog/archive.html', 'w') as _index:
			_index.write(_str)

def generate_archive_item(file_path, template_path):
	path, html_path, dates = parse_filePath(file_path)

	with open(template_path, 'r') as _t:
		_str = _t.read()
		md_file_name = Path(path).resolve().stem
		dates= dates.split('/')
		_datetime = "{}-{}-{}".format(dates[0], dates[1], dates[2])
		_readable_datetime = "{}".format(datetime.strptime(_datetime, "%Y-%m-%d").strftime("%a, %d %b %Y"))
		_str = _str.replace('<!#POST_URL#>', '/{}'.format(html_path.lower())) \
					.replace('<!#POST_SLUG#>', "{}-{}".format(_datetime, md_file_name)) \
					.replace('<!#POST_DATE#>', _readable_datetime) \
					.replace('<!#POST_TITLE#>', md_file_name.replace('-', ' ').title())
		return _str

def generate_post(file_path, template_path):
	''' Calls parse_filePath & and parse_markdown_file to generate an HTML file for the single post.'''
	path, html_path, dates = parse_filePath(file_path)
	html = parse_markdown_file(file_path)

	with open(template_path, 'r') as _t:
		_str = _t.read()
		md_file_name = Path(path).resolve().stem
		dates = dates.split('/')
		_datetime = "{}-{}-{}".format(dates[0], dates[1], dates[2])
		_readable_datetime = "{}".format(datetime.strptime(_datetime, "%Y-%m-%d").strftime("%a, %d %b %Y"))
		_str = _str.replace('<!#TITLE#>', md_file_name.replace('-', ' ')) \
					.replace('<!#SITE_URL#>', SITE_URL) \
					.replace('<!#SITE_TITLE#>', SITE_TITLE) \
					.replace('<!#SITE_DESCRIPTION#>', SITE_DESCRIPTION) \
					.replace("<!#POST_LINK#>", html_path.lower()) \
					.replace('<!#POST_HEADER#>', md_file_name.replace('-', ' ').title()) \
					.replace('<!#POST_BODY#>', html) \
					.replace('<!#POST_DATE#>', '<time datetime="{}">{}</time>'.format(_datetime, _readable_datetime))

		with open(path, 'w') as _f:
			_f.write(_str)

def generate_feed_item(file_path, template_path):
	''' Takes a file path and generates a feed item snippet. '''
	path, html_path, dates = parse_filePath(file_path)
	html = parse_markdown_file(file_path).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

	with open(template_path, 'r') as _t:
		_str = _t.read()
		md_file_name = Path(path).resolve().stem
		dates = dates.split('/')
		_datetime = "{}-{}-{}-{}-{}".format(dates[0], dates[1], dates[2], dates[3], dates[4])
		_readable_datetime = "{}".format(datetime.strptime(_datetime, "%Y-%m-%d-%H-%M").strftime("%a, %d %b %Y %H:%M"))
		_str = _str.replace('<!#TITLE#>', md_file_name.replace('-', ' ')) \
					.replace('<!#LINK#>', "{}/{}".format(SITE_URL, html_path.lower())) \
					.replace("<!#ITEM_DESCRIPTION#>", html) \
					.replace('<!#ITEM_PUB_DATE#>', _readable_datetime)

		return _str

def generate_feed(feed_items, template_path):
	''' Fills out missing pieces on xml and add items. '''
	with open(template_path, 'r') as _t:
		_str = _t.read()
		_readable_datetime = '{}'.format(datetime.now().strftime("%a, %d %b %Y %H:%M"))
		_str = _str.replace('<!#PAGE_TITLE#>', SITE_TITLE) \
					.replace('<!#PAGE_DESCRIPTION#>', SITE_DESCRIPTION) \
					.replace('<!#PAGE_URL#>', SITE_URL) \
					.replace('<!#LAST_BUILD_DATE#>', _readable_datetime) \
					.replace('<!#ITEMS#>', ''.join(feed_items))

		Path(XML_ROOT).mkdir(parents=True, exist_ok=True)
		with open('{}/rss.xml'.format(XML_ROOT), 'w') as _feed:
			_feed.write(_str)

def parse_filePath(file_path):
	''' Takes the draft file and parses path from filename. '''
	file_name = Path(file_path).resolve().stem
	split_name = file_name.split('_')
	_name = split_name[1].replace('"', '').replace('.', '').replace(',', '').replace('(', '').replace(')', '').replace('!', '').replace('ü', 'u')
	dates = split_name[0].replace('-', '/')
	_dates = dates.split('/')
	path_date = "{}/{}/{}".format(_dates[0], _dates[1], _dates[2])
	Path(PUBLISHED_DIRECTORY).mkdir(parents=True, exist_ok=True)
	canonical_path = "{}/{}.html".format(PUBLISHED_DIRECTORY, _name.lower())

	date_path = "{}/{}".format(PUBLISHED_ROOT, path_date)
	Path(date_path).mkdir(parents=True, exist_ok=True)

	if Path("{}/{}.html".format(date_path, _name.lower())).is_symlink() == False:
		Path("{}/{}.html".format(date_path, _name.lower())).symlink_to(Path(os.path.abspath(canonical_path)))

	return (canonical_path, "{}/{}/{}.html".format(PUBLISHED_ROOT, path_date, _name), dates)

''' Markdown Parser '''

def parse_markdown_file(file_path):
	''' Takes the draft file and converts Markdown to HTML.'''
	with open(file_path, 'r') as _f:
		_str = ""
		for line in _f:
			if line == '' or line == '\n':
				line = line
			if line.startswith('#'):
				line = transform_header(line)
			else:
				line = transform_blocks(line)
			_str += line
		return (wrap_paragraphs(_str))

def transform_header(mkd):
	re_head = re.compile(r'^(#{1,6})(.*$)')
	h_count = re.match(r'^#{1,6}', mkd).span()[1]

	mkd = re.sub(re_head, r'<h{count}>\2</h{count}>'.format(count=h_count), mkd)
	return mkd

def transform_blocks(mkd):
	re_open_brck = re.compile("<(?!img)")
	re_close_brck = re.compile("([^\/])>")
	re_hr = re.compile(r'^(\*|-)+\s?(\*|-)+\s?(\*|-)$')
	re_emph = re.compile(r'((\*)(.+?)(\*))')
	re_str = re.compile(r'((\*\*|__)(.+?)(\*\*|__))')
	re_lnk = re.compile(r'\[(.*?)\]\((.+?)("(.*)")?\)')

	re_quo = re.compile(r'((`)(.+?)(`))')
	re_list = re.compile(r'((^-|\*|\+)\s(.*\n))+')

	re_olist = re.compile(r'^(\d+.\s)(.*)\n')

	mkd = re.sub(re_open_brck, '&lt;', mkd)
	mkd = re.sub(re_close_brck, r'\1&gt;', mkd)
	mkd = re.sub(re_hr, '<hr />', mkd)
	mkd = re.sub(re_emph, r'<em>\3</em>', mkd)
	mkd = re.sub(re_str, r'<strong>\3</strong>', mkd)
	mkd = re.sub(re_lnk, r'<a href="\2" title="\4">\1</a>', mkd)

	mkd = re.sub(re_quo, r'<code>\3</code>', mkd)
	mkd = re.sub(re_list, r'<li>\3</li>', mkd)
	mkd = re.sub(re_olist, r'<li>\1\2</li>', mkd)
	return mkd

def wrap_paragraphs(html):
	re_code_block = re.compile(r'^((^\t))[^\r\n]+((\r|\n|\r\n)[^\r\n]+)*', re.MULTILINE)
	re_code_line = re.compile(r'\t(.*)')
	re_block_quote = re.compile(r'^>(.*\n)+?(\n\n)', re.MULTILINE)
	re_para = re.compile(r'^((?!^<|\t|^>))[^\r\n]+((\r|\n|\r\n)[^\r\n]+)*', re.MULTILINE)
	re_olist = re.compile(r'(<li>)(\d+\.\s)(.*)(<\/li>)+')
	re_linum = re.compile(r'<li>(\d+\.\s)')
	re_list = re.compile(r'(<li>.*\n<\/li>)+', re.MULTILINE)
	re_artifact = re.compile(r'(<.*>)>')
	re_leading_arrow = re.compile(r'(\n|^)>(.*)')

	html = re.sub(re_block_quote, r'<blockquote>\n\g<0></blockquote>\n', html)
	html = re.sub(re_code_block, r'<pre>\n\g<0>\n</pre>', html)
	html = re.sub(re_code_line, '<code>\g<1></code>', html)
	html = re.sub(re_olist, r'<ol class="ordered-inline">\g<0></ol>', html)
	html = re.sub(re_linum, r'<li>', html)
	html = re.sub(re_list, r'<ul class="unordered-inline">\g<0></ul>', html)
	html = re.sub(re_artifact, r'\g<1>', html)
	html = re.sub(re_leading_arrow, r'\g<1>\g<2>', html)
	html = re.sub(re_para, '<p>\g<0>\n</p>', html)
	return html