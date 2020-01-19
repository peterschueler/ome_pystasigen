import os

PUBLISHED_ROOT = os.environ.get('OME_PUBLISHED_ROOT', 'blog')
XML_ROOT = os.environ.get('OME_XML_ROOT', 'xml')
PUBLISHED_DIRECTORY = os.environ.get('OME_PUBLISHED_DIRECTORY', 'blog/all')
PUBLICATION_QUEUE = os.environ.get('OME_PUBLISH_QUEUE', '../site_source/publication_queue')
TEMPLATE_DIRECTORY = os.environ.get('OME_TEMPLATE_DIRECTORY', '../../templates')

SITE_TITLE = os.environ.get('OME_SITE_TITLE', 'INSERT YOUR SITE TILE i.e. Super Awesome Homepage')
SITE_DESCRIPTION = os.environ.get('OME_SITE_DESCRIPTION', 'INSERT YOUR SITE DESCRIPTION i.e. for all the people')
SITE_URL = os.environ.get('OME_SITE_URL', 'INSERT YOUR URL i.e. https://super_awesome_homepage.example.com/')

IMAGE_DIRECTORY = os.environ.get('OME_IMAGE_DIRECTORY', '../../files/images/photography')
PHOTOGRAPHY_URL = os.environ.get('OME_PHOTOGRAPHY_URL', 'photography')
THUMBNAIL_SIZES = {'small': [300,300], 'medium': [600,600], 'large': [1200,1200]}