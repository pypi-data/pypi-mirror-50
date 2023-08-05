#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from bs4 import BeautifulSoup
from ricecooker.utils import downloader, html_writer
from ricecooker.config import LOGGER              # Use LOGGER to print messages
import youtube_dl
import shutil
import tempfile

from le_utils.constants import content_kinds

from webmixer.exceptions import EXCEPTIONS, UnscrapableSourceException
from webmixer.scrapers.base import BasicScraper
from webmixer.scrapers.tags import COMMON_TAGS


class BasicPageScraper(BasicScraper):
    dl_directory = 'downloads'

    @classmethod
    def test(self, url):
        """
            Used to determine if this is the correct scraper to use for a given url
            Args:
                url (str): url to test
            Returns True if scraper is meant to scrape URL
        """
        raise NotImplementedError('Must implement a test method for {}'.format(str(self.__class__)))


    def preprocess(self, contents):
        """
            Place for any operations to occur before main scraping method
            Args:
                contents (BeautifulSoup): contents of page to pre-process
        """
        # Implement in subclasses
        pass

    def process(self):
        return downloader.read(self.url)

    def postprocess(self, contents):
        """
            Place for any operations to occur after main scraping method
            Args:
                contents (BeautifulSoup): contents of page to post-process
        """
        # Implement in subclasses
        pass


    ##### Output methods #####
    def download_file(self, write_to_path):
        """
            Downloads file to write_to_path
            Args:
                write_to_path (str): path to write file to
        """
        with open(write_to_path, 'wb') as fobj:
            fobj.write(self.process())

    def to_file(self, filename=None, directory=None, overwrite=False):
        """
            Download URL as a file
            Args:
                filename (optional str): name of file to write to
                directory (optional str): directory to write to
                overwrite (bool): overwrite file if it exists
        """
        directory = directory or self.directory
        if not os.path.exists(directory):
            os.makedirs(directory)

        write_to_path = os.path.join(directory, filename or self.get_filename(self.url))

        if overwrite or not os.path.exists(write_to_path):
            self.download_file(write_to_path)

        return write_to_path

    def to_zip(self, filename=None):
        """
            Download URL to self.zipper
            Args:
                filename (optional str): name of file to write to
        """
        return self.write_url(self.url, filename=filename)

    def to_tag(self, filename=None):
        """
            Download URL and return a tag based on what kind of scraper this is
            Args:
                filename (optional str): name of file to write to
        """
        raise NotImplementedError('Must implement to_tag function on {}'.format(str(self.__class__)))


######### HTML SCRAPERS ##########

class HTMLPageScraper(BasicPageScraper):
    partially_scrapable = False     # Not all content can be viewed from within Kolibri (e.g. Wikipedia's linked pages)
    scrape_subpages = True          # Determines whether to scrape any subpages within this page
    default_ext = '.html'           # Default extension when writing files to zip
    main_area_selector = None       # Place where main content is (replaces everything in <body> with this)
    omit_list = None                # Specifies which elements to remove from the DOM
    loadjs = False                  # Determines whether to load js when loading the page
    scrapers = None                 # List of additional scrapers to use on this page (e.g. GoogleDriveScraper)
    extra_tags = None               # List of additional tags to look for (e.g. ImageTag)
    color = 'rgb(153, 97, 137)'     # Color to use for messages (consider contrast when setting this)
    kind = content_kinds.HTML5      # Content kind to write to


    def __init__(self, *args, **kwargs):
        super(HTMLPageScraper, self).__init__(*args, **kwargs)
        self.omit_list = self.omit_list or []
        self.omit_list += [
            ('link', {'type': 'image/x-icon'}),
            ('link', {'rel': 'apple-touch-icon'}),
            ('span', {'class': 'external-iframe-src'}),
            ('link', {'rel': 'icon'}),
            ('div', {'class': 'mw-indicators'})
        ]
        self.extra_tags = self.extra_tags or []
        self.scrapers = (self.scrapers or []) + [self.__class__]

    def process(self):
        # Using html.parser as it is better at handling special characters
        contents = BeautifulSoup(downloader.read(self.url, loadjs=self.loadjs), 'html.parser')

        self.preprocess(contents)

        # If a main area is specified, replace body contents with main area
        if self.main_area_selector:
            body = self.create_tag('body')
            body.append(contents.find(*self.main_area_selector))
            contents.body.replaceWith(body)

        # Remove any items to omit
        for item in self.omit_list:
            for element in contents.find_all(*item):
                element.decompose()

        # Scrape tags
        for tag_class in (self.extra_tags + COMMON_TAGS):
            for tag in contents.find_all(*tag_class.selector):
                scraper = tag_class(tag, self.url,
                    zipper=self.zipper,
                    scrape_subpages=self.scrape_subpages,
                    triaged=self.triaged,
                    locale=self.locale,
                    extra_scrapers=self.scrapers,
                    color=self.color
                )
                scraper.scrape()

        self.postprocess(contents)

        return contents.prettify(formatter="minimal").encode('utf-8-sig', 'ignore')

    ##### Output methods #####
    def download_file(self, write_to_path):
        # Generate a .zip file
        with html_writer.HTMLWriter(write_to_path) as zipper:
            try:
                self.zipper = zipper
                self.to_zip(filename='index.html')
            except Exception as e:
                # Any errors here will just say index.html file does not exist, so
                # print out error for more descriptive debugging
                LOGGER.error(str(e))

    def to_file(self, filename=None, **kwargs):
        # Make sure html is being written to a zip file here
        filename = filename or self.get_filename(self.url)
        filename = filename.replace(self.default_ext, '.zip')
        return super(HTMLPageScraper, self).to_file(filename=filename, **kwargs)

    def to_zip(self, filename=None):
        return self.write_contents(filename or self.get_filename(self.url), self.process())


class DefaultScraper(HTMLPageScraper):
    """ Basic HTML page scraper in case no other scrapers match the URL """
    scrape_subpages = False
    loadjs = True

    def __init__(self, *args, **kwargs):
        super(DefaultScraper, self).__init__(*args, **kwargs)
        self.scrapers = [] # Don't scrape any subpages

    @classmethod
    def test(self, url):
        ext = os.path.splitext(url.split('?')[0].split('#')[0])[1].lower()
        return not ext or ext.startswith('.htm')


########## OTHER CONTENT KIND SCRAPERS ##########

class ImageScraper(BasicPageScraper):
    directory = 'img'
    default_ext = '.png'
    kind = content_kinds.SLIDESHOW  # No image type in Studio, so use this

    @classmethod
    def test(self, url):
        return url.lower().endswith('.png') or url.lower().endswith('.jpg')

    def to_file(self, filename=None):
        raise NotImplementedError('Unable to write SLIDESHOW kind to a file')

    def to_tag(self, filename=None):
        try:
            img = self.create_tag('img')
            img['src'] = self.to_zip(filename=filename)
            return img
        except EXCEPTIONS as e:
            LOGGER.error(str(e))
            return self.create_broken_link_message(self.url)


class PDFScraper(BasicPageScraper):
    directory = 'docs'
    default_ext = '.pdf'
    kind = content_kinds.DOCUMENT

    @classmethod
    def test(self, url):
        return url.split('?')[0].lower().endswith('.pdf')

    def to_tag(self, filename=None):
        try:
            embed = self.create_tag('embed')
            embed['src'] = self.to_zip(filename=filename)
            embed['width'] = '100%'
            embed['style'] = 'height: 500px;max-height: 100vh;'
            return embed
        except EXCEPTIONS as e:
            LOGGER.error(str(e))
            return self.create_broken_link_message(self.url)

class EPubScraper(BasicPageScraper):
    directory = 'docs'
    default_ext = '.epub'
    kind = content_kinds.DOCUMENT

    @classmethod
    def test(self, url):
        return url.split('?')[0].lower().endswith('.epub')


class AudioScraper(BasicPageScraper):
    default_ext = '.mp3'
    kind = content_kinds.AUDIO
    directory = 'audio'

    @classmethod
    def test(self, url):
        return url.split('?')[0].lower().endswith('.mp4')

    def to_tag(self, filename=None):
        try:
            audio = self.create_tag('audio')
            audio['controls'] = 'controls'
            audio['style'] = 'width: 100%;'
            source = self.create_tag('source')
            source['src'] = self.to_zip(filename=filename)
            audio.append(source)
            return audio
        except EXCEPTIONS as e:
            LOGGER.error(str(e))
            return self.create_broken_link_message(self.url)


class VideoScraper(BasicPageScraper):
    default_ext = '.mp4'
    kind = content_kinds.VIDEO
    dl_directory = 'videos'
    directory = 'videos'

    @classmethod
    def test(self, url):
        return url.split('?')[0].lower().endswith('.mp4')

    def to_tag(self, filename=None):
        try:
            video = self.create_tag('video')
            video['controls'] = 'controls'
            video['style'] = 'width: 100%;'
            video['preload'] = 'auto'
            source = self.create_tag('source')
            source['src'] = self.to_zip(filename=filename)
            video.append(source)
            return video
        except EXCEPTIONS as e:
            LOGGER.error(str(e))
            return self.create_broken_link_message(self.url)


class WebVideoScraper(VideoScraper):
    """ Videos that can be scraped by youtube_dl """

    @classmethod
    def test(self, url):
        return 'youtube' in url or 'vimeo' in url

    def process(self):
        write_to_path = self.to_file()
        with open(write_to_path) as fobj:
            return fobj.read()

    def download_file(self, write_to_path):
        try:
            dl_settings = {
                'outtmpl': write_to_path,
                'quiet': True,
                'overwrite': True,
                'format': self.default_ext.split('.')[-1],
            }
            with youtube_dl.YoutubeDL(dl_settings) as ydl:
                ydl.download([self.url])
        except (youtube_dl.utils.DownloadError, youtube_dl.utils.ExtractorError) as e:
            raise UnscrapableSourceException(str(e))  # Some errors are region-specific, so allow link

    def to_zip(self, filename=None):
        try:
            tempdir = tempfile.mkdtemp()
            video_path = os.path.join(tempdir, filename or self.get_filename(self.url))
            self.download_file(video_path)
            return self.write_file(video_path)
        except FileNotFoundError as e:
            # Some video links don't work, so youtube dl only partially downloads files but doesn't error out
            # leading to the .mp4 not being found (just a .part file)
            raise UnscrapableSourceException(str(e))
        finally:
            shutil.rmtree(tempdir)

    def to_tag(self, filename=None):
        video = self.create_tag('video')
        video['controls'] = 'controls'
        video['style'] = 'width: 100%;'
        video['preload'] = 'auto'
        source = self.create_tag('source')
        source['src'] = self.to_zip(filename=filename)
        video.append(source)
        return video


class FlashScraper(BasicPageScraper):
    default_ext = '.swf'
    standalone = True
    kind = 'flash'

    @classmethod
    def test(self, url):
        return url.split('?')[0].lower().endswith('.swf')

    def process(self, **kwargs):
        # Automatically throw error
        downloader.read(self.url) # Raises broken link error if fails
        raise UnscrapableSourceException('Cannot scrape Flash content')

    def to_tag(self, **kwargs):
        return self.process()

    def to_zip(self, **kwargs):
        return self.process()


COMMON_SCRAPERS = [
    WebVideoScraper,
    PDFScraper,
    EPubScraper,
    ImageScraper,
    FlashScraper,
    VideoScraper,
    AudioScraper,
]
