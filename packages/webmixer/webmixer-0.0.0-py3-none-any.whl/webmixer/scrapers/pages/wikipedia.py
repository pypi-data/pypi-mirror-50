#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
from ricecooker.config import LOGGER

from webmixer.exceptions import EXCEPTIONS
from webmixer.scrapers.pages.base import HTMLPageScraper
from webmixer.scrapers.tags import VideoTag


class WikipediaVideoTag(VideoTag):
    selector = ('div', {'class': 'PopUpMediaTransform'})

    def process(self):
        if self.tag.get('videopayload'):
            video = BeautifulSoup(self.tag['videopayload'], 'html.parser')
            video.video['style'] = 'width: 100%; height: auto;'
            video.video['preload'] = 'auto'
            self.mark_tag_to_skip(video.video)
            for source in video.find_all('source'):
                try:
                    source['src'] = self.write_url(source['src'], directory='media')
                except EXCEPTIONS as e:
                    LOGGER.warning(str(e))
                    source.decompose()
            self.tag.replaceWith(video.video)


class WikipediaScraper(HTMLPageScraper):
    scrape_subpages = False
    main_area_selector = ('div', {'id': "content"})
    partially_scrapable = True
    omit_list = [
        ('span', {'class': 'mw-editsection'}),
        ('a', {'class': 'mw-jump-link'}),
        ('div', {'class': 'navbox'}),
        ('div', {'class': 'mw-hidden-catlinks'})
    ]
    extra_tags = [WikipediaVideoTag]

    @classmethod
    def test(self, url):
        return 'wikipedia' in url or 'wikibooks' in url

    def preprocess(self, contents):
        for style in contents.find_all('link', {'rel': 'stylesheet'}):
            if style.get('href') and 'load.php' in style['href']:
                style.decompose()

        for script in contents.find_all('script'):
            if script.get('src') and 'load.php' in script['src']:
                script.decompose()

    def postprocess(self, contents):
        # Wikipedia uses a load.php file to load all the styles, so add the more common styling manually
        style_tag = self.create_tag('style')
        style_tag.string = "body { font-family: sans-serif; padding: 2%;} a {text-decoration: none;}"\
            "h1, h2 {font-family: 'Linux Libertine','Georgia','Times',serif;border-bottom: 1px solid #a2a9b1; font-weight:normal; margin-bottom: 0.25em;}"\
            "h2, h3, h4, h5, h6 {overflow: hidden;margin-bottom: .25em;} h3{font-size: 13pt;}"\
            ".toc {display: table; zoom: 1; border: 1px solid #a2a9b1; background-color: #f8f9fa;padding: 7px;}"\
            ".toc h2 {font-size: 100%; font-family: sans-serif; border: none; font-weight: bold; text-align: center; margin: 0;}"\
            ".toc ul { list-style-type: none; list-style-image: none;margin-left: 0; padding: 0; margin-top: 10px;}"\
            ".toc ul li {margin-bottom: 7px; font-size: 10pt;} .toc ul ul {margin: 0 0 0 2em;} .toc .tocnumber {color: #222;}"\
            ".thumbinner { border: 1px solid #c8ccd1; padding: 3px; background-color: #f8f9fa; font-size: 94%; text-align: center; overflow: hidden;}"\
            ".thumbimage {background-color: #fff; border: 1px solid #c8ccd1;} .thumbcaption {font-size: 10pt; text-align: left;padding: 3px;}"\
            ".tright { clear: right; float: right; margin: 0.5em 0 1.3em 1.4em;}"\
            ".catlinks { text-align: left; border: 1px solid #a2a9b1; background-color: #f8f9fa; padding: 5px; margin-top: 1em; clear: both;margin-bottom:50px;}"\
            ".catlinks ul { display: inline; list-style: none none; padding: 0;} .catlinks li { display: inline-block; margin: 0.125em 0;padding: 0 0.5em;}"\
            ".infobox { border: 1px solid #B4BBC8; background-color: #f9f9f9; margin: .5em 0 .7em 1.2em; padding: .4em; clear: right; float: right; font-size: 90%; line-height: 1.5em;width: 22.5em;}"\
            ".wikitable {background-color: #f8f9fa; color: #222; margin: 1em 0; border: 1px solid #a2a9b1; border-collapse: collapse;}"\
            ".wikitable th {background-color: #eaecf0; text-align: center;} .wikitable th, .wikitable td {border: 1px solid #a2a9b1;padding: 0.2em 0.4em;}"\
            ".gallery { text-align: center; } li.gallerybox { display: inline-block; }"\
            ".hlist ul { margin: 0; padding: 0; } .hlist ul ul {display: inline;} .hlist li {display: inline; font-size: 8pt;} .hlist li:not(:last-child)::after {content: ' · ';font-weight: bold;}"\
            ".reflist { font-size: 9pt; }"

        contents.head.append(style_tag)
