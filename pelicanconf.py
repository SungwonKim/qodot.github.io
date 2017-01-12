from __future__ import unicode_literals

AUTHOR = 'qodot'
SITENAME = 'waiting for qodot'
SITEURL = 'https://qodot.github.io'
PATH = 'content'
STATIC_PATHS = ['images']

TIMEZONE = 'Asia/Seoul'
DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_ATOM = 'category/%s/feeds/atom.xml'
CATEGORY_FEED_RSS = 'category/%s/feeds/rss.xml'

TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

LINKS = (
    ('* github', 'https://github.com/qodot'),
    ('* facebook', 'https://www.facebook.com/daewon.seo.5'),
    ('* rateyourmusic', 'https://rateyourmusic.com/~qodot'),
    ('* lastfm', 'http://www.last.fm/user/qodot'),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

from os.path import expanduser
home = expanduser("~")

FAVICON = 'images/favicon.png'

THEME = home + '/pelican/themes/Casper2Pelican'

# Casper2Pelican theme
AUTHOR_PIC_URL = '/images/profile.png'
AUTHOR_BIO = 'Python Developer'
AUTHOR_LOCATION = 'Seoul, South Korea'
DEFAULT_HEADER_IMAGE = '/images/default_header.png'
ARCHIVE_HEADER_IMAGE = '/images/archive_header.png'

PLUGIN_PATHS = [home + '/pelican/plugins']
PLUGINS = ['related_posts.related_posts']

# custom for Casper2Pelican theme
CATEGORIES = [
    ('@ py', 'category/py.html'),
    ('@ env', 'category/env.html'),
]

DISQUS_SITENAME = 'qodot'
GOOGLE_ANALYTICS = 'UA-83522208-2'

DELETE_OUTPUT_DIRECTORY = True
