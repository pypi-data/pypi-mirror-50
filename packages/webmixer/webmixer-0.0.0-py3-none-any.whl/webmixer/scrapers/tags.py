#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import cssutils
import logging
import os

from le_utils.constants import content_kinds
from ricecooker.config import LOGGER
from ricecooker.utils import downloader

from webmixer.exceptions import EXCEPTIONS, UnscrapableSourceException
from webmixer.scrapers.base import BasicScraper
from webmixer.utils import guess_scraper

cssutils.log.setLevel(logging.FATAL)  # Reduce cssutils output


class BasicScraperTag(BasicScraper):
    selector = None            # BeautifulSoup selector to find tag (e.g. ('a', {'class': 'link'}))
    default_attribute = 'src'  # Attribute that references files
    default_ext = None         # Extension to use if link doesn't have an extension
    directory = None           # Directory to write tag files to
    attributes = None          # Any attributes to assign to a tag
    scrape_subpages = True     # Determines whether to scrape any linked pages
    extra_scrapers = None      # Any additional scrapers to use for scraping linked pages

    def __init__(self, tag, url, attribute=None, scrape_subpages=True, extra_scrapers=None, color='rgb(153, 97, 137)', **kwargs):
        """
            tag (BeautifulSoup tag): tag to scrape
            attribute (str): tag's attribute where link is found (e.g. 'src' or 'data-src')
        """
        super(BasicScraperTag, self).__init__(url, **kwargs)
        self.attributes = self.attributes or {}
        self.tag = tag
        self.attribute = attribute or self.default_attribute
        self.link = self.tag.get(self.attribute) and self.get_relative_url(self.tag.get(self.attribute)).strip('%20')
        self.scrape_subpages = scrape_subpages
        self.extra_scrapers = extra_scrapers or []
        self.color = color

    def format_url(self, zipper_path):
        """
            Returns the zipper path with any additional query params from the original URL
            Args:
                zipper_path (str): path to file within zip file
        """
        if '#' in self.link:
            zipper_path += '#' + self.link.split('#')[-1]
        if '?' in self.link:
            zipper_path += '?' + self.link.split('?')[-1]
        return zipper_path

    def scrape(self):
        """
            Scrapes the tag and handles potential exceptions
            Returns the path to the zipped file
        """
        if 'skip-scrape' in (self.tag.get('class') or []):
            return
        try:
            # Set attributes based on attributes dict
            for key, value in self.attributes.items():
                if key == 'style':
                    self.tag[key] = ';'.join([(self.tag.get(key) or '').rstrip(';'), value])
                else:
                    self.tag[key] = value

            # Process the tag and return the zipped file
            zippath = self.process()
            self.mark_tag_to_skip(self.tag)
            return zippath
        except EXCEPTIONS as e:
            LOGGER.warning('Broken source found at {} ({})'.format(self.url, self.link))
            self.handle_error()
        except UnscrapableSourceException:
            LOGGER.warning('Unscrapable source found at {} ({})'.format(self.url, self.link))
            self.handle_unscrapable()
        except KeyError as e:
            LOGGER.warning('Key error at {} ({})'.format(self.url, str(e)))

    def process(self):
        """
            Make the tag usable from within an html zip by downloading any referenced files
            Returns the path to the zipped file
        """
        self.tag[self.attribute] = self.format_url(self.write_url(self.link))
        return self.tag[self.attribute]

    def handle_error(self):
        """
            Handle any broken links (defaults to replacing with broken message)
        """
        self.tag.replaceWith(self.create_broken_link_message(self.link))

    def handle_unscrapable(self):
        """
            Handle any unscrapable links (defaults to replacing with unscrapable message)
        """
        self.tag.replaceWith(self.create_copy_link_message(self.link))


########## FILE-BASED TAGS ##########

class ImageTag(BasicScraperTag):
    default_ext = '.png'
    directory = "img"
    selector = ('img',)

    def process(self):
        # Skip any base64 images
        if self.link and 'data:image' not in self.link:
            return super(ImageTag, self).process()

class MediaTag(BasicScraperTag):
    """ Video/audio tags """
    directory = "media"
    attributes = {
        'controls': 'controls',
        'preload': 'auto'
    }
    def process(self):
        if self.tag.find('source'):
            for source in self.tag.find_all('source'):
                self.source_class(source, self.zipper, self.url)
        else:
            return super(MediaTag, self).process()

class SourceTag(BasicScraperTag):
    selector = ('source',)

    def handle_error(self):
        self.tag.decompose()

class AudioSourceTag(SourceTag):
    default_ext = '.mp3'

class VideoSourceTag(BasicScraperTag):
    default_ext = '.mp4'

class AudioTag(MediaTag):
    default_ext = '.mp3'
    source_class = AudioSourceTag
    selector = ('audio',)

class VideoTag(MediaTag):
    default_ext = '.mp4'
    source_class = VideoSourceTag
    selector = ('video',)

class EmbedTag(LinkedPageTag):
    default_ext = '.pdf'
    directory = 'files'
    attributes = {
        'style': 'width:100%; height:500px;max-height: 100vh'
    }
    selector = ('embed',)

    def process(self):
        scraper = self.get_scraper()
        scraper.to_zip(filename=self.get_filename(self.link))



########## LINKED TAGS ##########

class LinkedPageTag(BasicScraperTag):
    def get_scraper(self):
        scraper = guess_scraper(self.link, scrapers=self.extra_scrapers, locale=self.locale, triaged=self.triaged, zipper=self.zipper)
        if not scraper:
            downloader.read(self.link) # Will raise an error if this is broken
            raise UnscrapableSourceException
        return scraper

class LinkTag(LinkedPageTag):
    default_attribute = 'href'
    default_ext = '.html'
    attributes = {
        'target': ''
    }
    selector = ('a',)

    def process(self):
        # Skip links that don't link to outside sources
        if not self.link or 'javascript:void' in self.link \
            or self.tag[self.attribute].startswith("#") or self.tag[self.attribute] == '/':
            return

        # Turn any email links to plain text
        elif 'mailto' in self.link:
            self.tag.replaceWith(self.tag.text)

        # Turn creativecommons links to text (or images if found)
        elif 'creativecommons.org' in self.link:
            # Some links use the image as the link
            new_text = self.create_tag('b')
            new_text.string = self.tag.find('img').get('alt') if self.tag.find('img') else self.tag.text
            self.tag.replaceWith(new_text)

        # Don't scrape any subpages if scrape_subpages if False
        elif not self.scrape_subpages:
            self.handle_error()

        # If the link hasn't been triaged yet, scrape it
        elif not self.triaged.get(self.link):
            self.triaged[self.link] = self.get_filename(self.link)

            if not self.zipper.contains(self.triaged[self.link]):
                scraper = self.get_scraper()
                self.triaged[self.link] = scraper.to_zip()
            self.tag[self.attribute] = self.triaged[self.link]

        # If the link has been triaged, just set the attribute
        else:
            self.tag[self.attribute] = self.triaged[self.link]

    def handle_error(self):
        # Replace link with plaintext or any child images
        img = self.tag.find('img')
        if img:
            self.tag.replaceWith(img)
        else:
            self.tag.replaceWith(self.tag.text)
            self.tag['style'] = 'font-weight: bold;'

    def handle_unscrapable(self):
        # Replace link with plaintext and the url
        new_tag = self.create_tag('span')
        bold_tag = self.create_tag('b')
        bold_tag.string = self.tag.text
        new_tag.append(bold_tag)
        new_tag.append('({})'.format(self.link))
        self.tag.replaceWith(new_tag)


class IframeTag(LinkedPageTag):
    selector = ('iframe',)
    default_ext = '.html'
    attributes = {
        'style': 'resize: both;'
    }

    def process(self):
        if not self.link:
            pass
        elif 'googletagmanager' in self.link or 'googleads' in self.link:
            self.tag.decompose()
        else:
            scraper = self.get_scraper()

            # If it's a plain file, replace with a new tag
            # Otherwise, just link to the page
            if scraper.kind != content_kinds.HTML5:
                new_tag = scraper.to_tag()
                self.tag.replaceWith(new_tag)
                self.tag = new_tag
            else:
                self.tag[self.attribute] = scraper.to_zip()



########## OTHER TAGS ##########

class StyleTag(BasicScraperTag):
    default_ext = '.css'
    default_attribute = 'href'
    directory = 'css'
    selector = ('link', {'rel': 'stylesheet'})

    def process(self):
        if 'fonts' in self.link:  # Omit google fonts
            self.tag.decompose()
            return

        # Parse urls in css (using parseString because it is much faster than parseUrl)
        style_sheet = downloader.read(self.link).decode('utf-8-sig', errors='ignore')
        sheet = cssutils.parseString(style_sheet)
        for css_url in cssutils.getUrls(sheet):
            if not css_url.startswith('data:image') and not css_url.startswith('data:application'):
                try:
                    style_sheet = style_sheet.replace(css_url, os.path.basename(self.write_url(css_url, url=self.link, default_ext='.png')))
                except EXCEPTIONS as e:
                    LOGGER.warn('Unable to download stylesheet url at {} ({})'.format(self.url, str(e)))

        self.tag[self.attribute] = self.format_url(self.write_contents(self.get_filename(self.link), style_sheet))
        return self.tag[self.attribute]

    def handle_error(self):
        self.tag.decompose()


class ScriptTag(BasicScraperTag):
    directory = 'js'
    default_ext = '.js'
    selector = ('script',)

    def process(self):
        if self.tag.string and 'google' in self.tag.string:
            self.tag.decompose()
        elif not self.link:
            return
        elif 'google' in self.link:
            self.tag.decompose()
        else:
            return super(ScriptTag, self).process()

    def handle_error(self):
        # Just remove scripts that are broken
        self.tag.decompose()


COMMON_TAGS = [
    ImageTag,
    StyleTag,
    ScriptTag,
    VideoTag,
    AudioTag,
    EmbedTag,
    LinkTag,
    IframeTag,
]
