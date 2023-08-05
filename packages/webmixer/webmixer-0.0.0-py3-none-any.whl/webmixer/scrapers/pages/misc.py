#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import requests
import re
import youtube_dl
from bs4 import BeautifulSoup
from ricecooker.utils import downloader
from pages import HTMLPageScraper

class ThingLinkScraper(HTMLPageScraper):
    partially_scrapable = True
    loadjs = True
    scrape_subpages = False
    omit_list = [
        ('nav', {'class': 'item-header'}),
    ]

    @classmethod
    def test(self, url):
        return 'thinglink.com' in url

    def preprocess(self, contents):
        thinglink_id = self.url.split('/')[-1]

        for script in contents.find_all('script'):
            if script.get('src') and 'embed.js' in script['src']:
                response = requests.get('https://www.thinglink.com/api/tags?url={}'.format(thinglink_id))
                script_contents = downloader.read(self.get_relative_url(script['src'])).decode('utf-8')
                tag_data = json.loads(response.content)

                if tag_data[thinglink_id].get('image'):
                    tag_data[thinglink_id]['image'] = ImageScraper(tag_data[thinglink_id]['image'], zipper=self.zipper).to_zip()

                for thing in tag_data[thinglink_id]['things']:
                    if thing['thingUrl']:
                        try:
                            thing['thingUrl'] = WebVideoScraper(thing['thingUrl'], zipper=self.zipper).to_zip()
                            thing['contentUrl'] = thing['thingUrl']
                            thing['icon'] = ImageScraper(thing['icon'], zipper=self.zipper).to_zip()
                        except youtube_dl.utils.DownloadError as e:
                            LOGGER.warning('Youtube download error on thinglink page ({})'.format(str(e)))
                    if thing.get('nubbin'):
                        self.write_url('https://cdn.thinglink.me/api/nubbin/{}/plain'.format(thing['nubbin']), filename='nubbin-{}-plain.png'.format(thing['nubbin']), directory="thinglink")
                        self.write_url('https://cdn.thinglink.me/api/nubbin/{}/highlight'.format(thing['nubbin']), filename='nubbin-{}-highlight.png'.format(thing['nubbin']), directory="thinglink")
                        self.write_url('https://cdn.thinglink.me/api/nubbin/{}/hover'.format(thing['nubbin']), filename='nubbin-{}-hover.png'.format(thing['nubbin']), directory="thinglink")
                        self.write_url('https://cdn.thinglink.me/api/nubbin/{}/hoverlink'.format(thing['nubbin']), filename='nubbin-{}-hoverlink.png'.format(thing['nubbin']), directory="thinglink")

                script_contents = script_contents.replace('d.ajax({url:A+"/api/tags",data:u,dataType:"jsonp",success:z})', 'z({})'.format(json.dumps(tag_data)))
                script_contents = script_contents.replace('n.getJSON(A+"/api/internal/logThingAccess?callback=?",{thing:y,sceneId:w,e:"hover",referer:t.referer,dwell:v});', '')
                script_contents = script_contents.replace('n.getJSON(t.getApiBaseUrl()+"/api/internal/logThingAccess?callback=?",{time:y,sceneId:v,thing:w,e:"hoverend",referer:t.referer})', '')
                script_contents = script_contents.replace('n.getJSON(t.getApiBaseUrl()+"/api/internal/logSceneAccess?callback=?",{time:z,sceneId:w,referer:t.referer,dwell:v,event:"scene.hover"})', '')
                script_contents = script_contents.replace('n.getJSON(t.getApiBaseUrl()+"/api/internal/logSceneAccess?callback=?",{sceneId:v,referer:t.referer,event:"scene.view",channelId:b.getChannelId(x)})', '')
                script_contents = script_contents.replace('n.getJSON(B+"/api/internal/logThingAccess?callback=?",z,C);', '')

                icon_str = 'k.src=l;return"style=\\"background-image: url(\'"+l+"\') !important;\\"'
                script_contents = script_contents.replace(icon_str, 'var slices=l.split("/"); l="thinglink/"+slices.slice(slices.length-3,slices.length).join("-")+".png";{}'.format(icon_str))
                script['src'] = self.write_contents('thinglink-{}-embed.js'.format(thinglink_id), script_contents, directory="thinglink")
                self.mark_tag_to_skip(script)

    def postprocess(self, contents):
        style_tag = self.create_tag('style')
        style_tag.string = '.tlExceededViewsLimit, .tlThingText:not(.tlVariantVideoThing) .tlThingClose, .tlSidebar, .tlThinglinkSite {visibility: hidden !important;} .tlFourDotsButton, .btnViewOnSS {pointer-events: none;} .tlFourDotsButton .btn, .tlFourDotsButton .arrowRight {display: none !important;}'
        contents.head.append(style_tag)
        for script in contents.find_all('script'):
            if not script.string or 'skip-scrape' in (script.get('class') or []):
                continue
            elif 'preloadImages' in script.string:
                regex = r"(?:'|\")([^'\"]+)(?:'|\"),"
                for match in re.finditer(regex, script.string, re.MULTILINE):
                    new_str = match.group(0).replace(match.group(1), self.write_url(match.group(1), default_ext=".png", directory="thinglink"))
                    script.string = script.text.replace(match.group(0), new_str)
            elif re.search(r"var url\s*=\s*(?:'|\")([^'\"]+)(?:'|\")", script.string, re.MULTILINE):
                regex = r"url\s*=\s*(?:'|\")([^'\"]+)(?:'|\")"
                for match in re.finditer(regex, script.string, re.MULTILINE):
                    new_str = match.group(0).replace(match.group(1), self.write_url(match.group(1), default_ext=".png", directory="thinglink"))
                    script.string = script.text.replace(match.group(0), new_str)
            elif 'doresize' in script.string:
                match = re.search(r'\$tlJQ\(document\)\.ready\(function\(\) \{\s+(doresize\(\);)', script.string)
                new_str = match.group(0).replace(match.group(1), 'doresize(); __thinglink.reposition(); __thinglink.rebuild();')
                script.string = script.text.replace(match.group(0), new_str)

        for nubbin in contents.find_all('div', {'class': 'nubbin'}):
            for subnubbin in nubbin.find_all('div'):
                if not subnubbin.get('style'):
                    continue
                regex = r"\((?:'|\")*(http[^'\"]+)(?:'|\")*\)"
                for match in re.finditer(regex, subnubbin['style'], re.MULTILINE):
                    subnubbin['style'] = subnubbin['style'].replace(match.group(1), self.write_url(match.group(1), default_ext=".png", directory="thinglink"))


class EducaplayScraper(HTMLPageScraper):
    loadjs = True
    scrape_subpages = False
    partially_scrapable = True
    omit_list = [
        ('ins', {'class': 'adsbygoogle'})
    ]
    media_directory = "media"

    @classmethod
    def test(self, url):
        return 'educaplay.com' in url

    def preprocess(self, contents):
        for script in contents.find_all('script'):
            if script.get('src') and 'xapiEventos.js' in script['src']:
                script_contents = downloader.read(self.get_relative_url(script['src'])).decode('utf-8')
                script_contents = script_contents.replace('img.src=rutaRecursos+imagen;', 'img.src = "img/" + imagen;');
                script_contents = script_contents.replace('/snd_html5/', '{}/-snd_html5-'.format(self.media_directory))
                script['src'] = self.write_contents(self.get_filename(self.url, default_ext='.js'), script_contents, directory="js")
                self.mark_tag_to_skip(script)
            elif script.string and 'socializarPage' in script.string:
                script.decompose()  # Remove share on social media links

    def postprocess(self, contents):
        style_tag = self.create_tag('style')
        style_tag.string = '#banner { display: none !important; }'
        contents.head.append(style_tag)
        for audio in contents.find_all('audio'):
            for source in audio.find_all('source'):
                source['src'] = self.write_url(source['src'], directory=self.media_directory)
            self.mark_tag_to_skip(audio)


class GeniallyScraper(HTMLPageScraper):
    scrape_subpages = False

    @classmethod
    def test(self, url):
        return 'genial.ly' in url

    def preprocess(self, contents):
        # Hide certain elements from the page
        style_tag = self.create_tag('style')
        style_tag.string = '.genially-view-logo { pointer-events: none;} .genially-view-navigation-actions,'\
            ' .genially-view-navigation-actions-toggle-button{display: none !important; pointer-events:none;}'
        contents.head.append(style_tag)

        # Prefetch API response and replace script content accordingly
        genial_id = self.url.split('/')[-1]
        response = requests.get('https://view.genial.ly/api/view/{}'.format(genial_id))
        for script in contents.find_all('script'):
            if script.get('src') and 'main' in script['src']:
                script_contents = downloader.read(self.get_relative_url(script['src'])).decode('utf-8')
                genial_data = json.loads(response.content)

                if len(genial_data['Videos']) or len(genial_data['Audios']):
                    LOGGER.error('Unhandled genial.ly video or audio at {}'.format(url))

                if genial_data['Genially']['ImageRender']:
                    genial_data['Genially']['ImageRender'] = self.write_url(genial_data['Genially']['ImageRender'], directory='webimg')
                for image in genial_data['Images']:
                    image['Source'] = self.write_url(image['Source'], directory='webimg')
                for slide in genial_data['Slides']:
                    slide['Background'] = self.write_url(slide['Background'], directory='webimg')
                for code in genial_data['Contents']:
                    code_contents = BeautifulSoup(code['HtmlCode'], 'html.parser')
                    for img in code_contents.find_all('img'):
                        try:
                            img['src'] = self.write_url(img['src'], directory='webimg')
                        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
                            LOGGER.warning("Error processing genial.ly at {} ({})".format(url, str(e)))
                    code['HtmlCode'] = code_contents.prettify()
                script_contents = script_contents.replace('r.a.get(c).then(function(e){return n(e.data)})', 'n({})'.format(json.dumps(genial_data)))
                script['class'] = ['skip-scrape']
                script['src'] = self.write_contents('genial-{}-embed.js'.format(genial_id), script_contents,  directory="js")

