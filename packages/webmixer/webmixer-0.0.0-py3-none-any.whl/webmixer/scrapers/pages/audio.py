#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import re
from bs4 import BeautifulSoup
from ricecooker.utils import downloader
from le_utils.constants import content_kinds
from webmixer.scrapers.base import AudioScraper, WebVideoScraper

class SoundCloudScraper(WebVideoScraper):
    default_ext = '.mp3'
    kind = content_kinds.AUDIO
    directory = 'audio'

    @classmethod
    def test(self, url):
        return 'soundcloud' in url and 'search?' not in url and 'playlists' not in url

    def to_tag(self, filename=None):
        # Get image if there is one
        div = self.create_tag('div')
        contents = BeautifulSoup(downloader.read(self.url, loadjs=True), 'html5lib')
        image = contents.find('div', {'class': 'sc-artwork'})
        if image:
            url = re.search(r'background-image:url\(([^\)]+)\)', image.find('span')['style']).group(1)
            img = self.create_tag('img')
            img['src'] = self.write_url(url, directory='webimg', default_ext='.png')
            img['style'] = 'width:300px;'
            div.append(img)
        audio_tag = self.create_tag('audio')
        audio_tag['controls'] = 'controls'
        audio_tag['style'] = 'margin-left: auto; margin-right: auto;'
        source_tag = self.create_tag('source')
        source_tag['src'] = self.to_zip(filename=filename)
        audio_tag.append(source_tag)
        div.append(audio_tag)

        return div


class IVooxScraper(AudioScraper):
    @classmethod
    def test(self, url):
        return 'ivoox.com' in url

    def download_file(self, write_to_path):
        audio_id = re.search(r'(?:player_ek_)([^_]+)(?:_2_1\.html)', self.url).group(1)
        with open(write_to_path, 'wb') as fobj:
            fobj.write(downloader.read('http://www.ivoox.com/listenembeded_mn_{}_1.m4a?source=EMBEDEDHTML5'.format(audio_id)))

    def to_zip(self, filename=None):
        audio_id = re.search(r'(?:player_ek_)([^_]+)(?:_2_1\.html)', self.url).group(1)
        return self.write_url('http://www.ivoox.com/listenembeded_mn_{}_1.m4a?source=EMBEDEDHTML5'.format(audio_id))
