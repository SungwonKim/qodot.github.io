#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'qodot'
SITENAME = 'waiting for qodot'
SITEURL = 'http://qodot.github.io'
PATH = 'content'

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

SOCIAL = (
    ('facebook', 'https://www.facebook.com/daewon.seo.5'),
    ('github', 'https://github.com/qodot'),
    ('rateyourmusic', 'https://rateyourmusic.com/~qodot'),
    ('lastfm', 'http://www.last.fm/user/qodot'),
)

# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

from os.path import expanduser
home = expanduser("~")

THEME = home + '/pelican-themes/pelican-bootstrap3'
DISQUS_SITENAME = 'qodot'
GOOGLE_ANALYTICS = 'UA-61719953-2'

# pelican-bootstrap3 theme settings
FAVICON = 'images/favicon.png'
BOOTSTRAP_NAVBAR_INVERSE = True

DISPLAY_BREADCRUMBS = True
DISPLAY_CATEGORY_IN_BREADCRUMBS = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True

DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True

ADDTHIS_PROFILE = 'qodot'
