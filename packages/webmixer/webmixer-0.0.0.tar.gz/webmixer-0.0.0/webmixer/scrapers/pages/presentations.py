#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from bs4 import BeautifulSoup
from ricecooker.utils import downloader

from webmixer.messages import MESSAGES
from webmixer.scrapers.pages.base import HTMLPageScraper


class PresentationScraper(HTMLPageScraper):
    thumbnail = None         # Logo for source
    source = ""              # Name of source
    img_selector = ('img',)  # Selector for images
    img_attr='src'           # Image attribute

    @classmethod
    def test(self, url):
        return False  # Must implement a subclass to use

    def process(self):
        # Read URL and generate slideshow html
        contents = BeautifulSoup(downloader.read(self.url, loadjs=self.loadjs), 'html.parser')
        images = []
        for img  in contents.find_all(*self.img_selector):
            images.append(self.write_url(img[self.img_attr], directory="slides"))
        return self.generate_slideshow(images)

    def to_zip(self, filename=None):
        contents = self.process()
        return self.write_contents(filename or self.get_filename(self.url), contents)

    def generate_slideshow(self, images):
        # <body>
        page = BeautifulSoup('', 'html5lib')
        page.body['style'] = 'background-color: black; height: 100vh; margin: 0px;'
        page.body['class'] = ['collapsed']
        page.body['onclick'] = 'closeDropdown()'

        # <style>
        style = self.create_tag('style')
        style.string = '#gallery {width: 100vw;}\n'\
                    '#progress, #navigation, .wrapper, #gallery {max-width: 900px;}\n'\
                    'button {cursor: pointer}\n'\
                    'button:disabled { cursor: not-allowed; opacity: 0.5; }\n'\
                    'body.fullscreen .wrapper {max-width: 100%;}\n'\
                    'body.fullscreen #gallery, body.fullscreen #navigation, body.fullscreen #progress {max-width: 100%;}\n'\
                    '#counter::after { content: "▲"; padding-left: 10px; font-size: 7pt; vertical-align: middle; }\n'\
                    '#navigation-menu {list-style: none; padding: 0px; overflow-y: auto; overflow-x: none; height: 250px; max-height: 100vh;background: '\
                        'white; width: max-content; margin: 0 auto; margin-top: -275px; border: 1px solid #ddd; display: none; position: relative;}\n'\
                    '#navigation-menu li:not(:first-child) {border-top: 1px solid #ddd; }'\
                    '#navigation-menu li:hover { background-color: #ddd; }\n'

        style.string += '#progressbar {{ height: 10px; background-color: {}; transition: width 0.5s; }}'.format(self.color)

        page.head.append(style)

        # <div class="wrapper">
        wrapper = self.create_tag('div')
        wrapper['style'] = 'width: max-content; margin: 0 auto; text-align: center;'
        page.body.append(wrapper)

        # <img id="gallery"/>
        gallery = self.create_tag('img')
        gallery['id'] = 'gallery'
        gallery['style'] = 'cursor:pointer; height: auto; max-height: calc(100vh - 45px); object-fit: contain; color: white; font-family: sans-serif;'
        gallery['onclick'] = 'updateImage(1)'
        gallery['src'] = images[0]
        wrapper.append(gallery)

        # <div id="progress">
        progress = self.create_tag('div')
        progress['id'] = 'progress'
        progress['style'] = 'background-color: #4E4E4E; width: 100vw; height: 10px;'
        wrapper.append(progress)

        # <div id="progressbar">
        progressbar = self.create_tag('div')
        progressbar['id'] = 'progressbar'
        progress.append(progressbar)

        # <div id="navigation">
        navigation = self.create_tag('div')
        navigation['id'] = 'navigation'
        navigation['style'] = 'background-color:#353535; text-align:center; height: 33px; width: 100vw;'
        wrapper.append(navigation)

        # <button id="next-btn">
        nextbutton = self.create_tag('button')
        nextbutton['id'] = 'next-btn'
        nextbutton.string = '🡒'
        nextbutton['style'] = 'float:right; background-color: transparent; border: none; font-size: 17pt; color: white; width:75px; font-size:16pt;'
        nextbutton['onclick'] = 'updateImage(1)'
        nextbutton['title'] = MESSAGES[self.locale]['next']
        navigation.append(nextbutton)

        # <a id="fullscreen">
        fullscreentoggle = self.create_tag('a')
        fullscreentoggle['id'] = 'fullscreen'
        fullscreentoggle['style'] = 'float:right; color: white; font-size: 15pt; padding: 5px; cursor: pointer;'
        fullscreentoggle['onclick'] = 'toggleFullScreen()'
        fullscreentoggle['title'] = MESSAGES[self.locale]['toggle_fullscreen']
        fullscreentoggle.string = '⤢'
        navigation.append(fullscreentoggle)

        # <button id="prev-btn">
        prevbutton = self.create_tag('button')
        prevbutton['id'] = 'prev-btn'
        prevbutton.string = '🡐'
        prevbutton['style'] = 'float:left; background-color: transparent; border: none; font-size: 17pt; color: white; width:75px; font-size:16pt;'
        prevbutton['onclick'] = 'updateImage(-1)'
        prevbutton['title'] = MESSAGES[self.locale]['previous']
        navigation.append(prevbutton)

        # <div id="attribution">
        if self.source:
            attribution = self.create_tag('div')
            attribution['id'] = 'attribution'
            attribution['style'] = 'float:left; margin-top:3px;'
            navigation.append(attribution)

            # <img id="sourceLogo">
            if self.thumbnail:
                source_logo = self.create_tag('img')
                source_logo['id'] = 'sourceLogo'
                source_logo['src'] = os.path.basename(self.write_url(self.thumbnail, default_ext=".png"))
                source_logo['style'] = 'width: 24px; height: auto; margin-right: 5px;'
                attribution.append(source_logo)

            # <div id="created">
            created = self.create_tag('div')
            created['style'] = 'text-align: left; color: white; font-family: sans-serif; font-size: 7pt; display: inline-block;'
            created['id'] = 'created'
            created.string = MESSAGES[self.locale]['presentation_source']
            attribution.append(created)

            # <div id="sourceText">
            source_text = self.create_tag('div')
            source_text.string = self.source
            source_text['style'] = 'font-size: 12pt;'
            created.append(source_text)

        # <div id='center'>
        center_nav = self.create_tag('div')
        navigation.append(center_nav)

        # <div id='counter'>
        counter = self.create_tag('div')
        counter['id'] = 'counter'
        counter['style'] = 'padding-top: 5px; color: white; cursor: pointer; font-family: sans-serif;'
        counter['onclick'] = 'openDropdown(event)'
        center_nav.append(counter)

        # <ul id="navigation-menu">
        navmenu = self.create_tag('ul')
        navmenu['id'] = 'navigation-menu'
        center_nav.append(navmenu)

        for index, img  in enumerate(images):
            # <li>
            navmenuitem = self.create_tag('li')
            navmenuitem['style'] = 'font-family: sans-serif; text-align: left; padding: 10px 25px; cursor: pointer;'
            navmenuitem['onclick'] = 'jumpToImage({})'.format(index)
            navmenu.append(navmenuitem)

            # <img class="slide"> Slide #
            slideimg = self.create_tag('img')
            slideimg['class'] = ['slide']
            slideimg['src'] = img
            slideimg['style'] = 'width: 150px; vertical-align: middle; font-size: 12pt; margin-right: 20px;'
            navmenuitem.append(slideimg)
            navmenuitem.append(MESSAGES[self.locale]['slide'].format(index + 1))

        # <script>
        script = self.create_tag('script')
        script.string = "let images = [{images}]; \n"\
            "let index = 0;\n"\
            "let menuExpanded = false;\n"\
            "let img = document.getElementById('gallery');\n"\
            "let prevbutton = document.getElementById('prev-btn');\n"\
            "let nextbutton = document.getElementById('next-btn');\n"\
            "let countText = document.getElementById('counter');\n"\
            "let progress = document.getElementById('progress');\n"\
            "let menu = document.getElementById('navigation-menu');"\
            .format(images=','.join(['\"{}\"'.format(i) for i in images]))

        script.string += "function updateImage(step) {\n"\
            "  if(index + step >= 0 && index + step < images.length)\n"\
            "    index += step;\n"\
            "  jumpToImage(index);\n"\
            "}"

        script.string += "function jumpToImage(step) {\n"\
            "  index = step;\n"\
            "  countText.innerHTML = index + 1 + ' / ' + images.length;\n"\
            "  img.setAttribute('src', images[index]);\n"\
            "  countText.innerHTML = index + 1 + ' / ' + images.length;\n"\
            "  img.setAttribute('src', images[index]);\n"\
            "  (index === 0)? prevbutton.setAttribute('disabled', 'disabled') : prevbutton.removeAttribute('disabled');\n"\
            "  (index === images.length - 1)? nextbutton.setAttribute('disabled', 'disabled') : nextbutton.removeAttribute('disabled');\n"\
            "  progress.children[0].setAttribute('style', 'width:' + ((index + 1) / images.length * 100) + '%;')\n"\
            "}\n"

        script.string += "function toggleFullScreen() {\n"\
            "if ((document.fullScreenElement && document.fullScreenElement !== null) ||(!document.mozFullScreen && !document.webkitIsFullScreen)) {\n"\
            "document.body.setAttribute('class', 'fullscreen');\n"\
            "if (document.documentElement.requestFullScreen) { document.documentElement.requestFullScreen();} \n"\
            "else if (document.documentElement.mozRequestFullScreen) { document.documentElement.mozRequestFullScreen(); } \n"\
            "else if (document.documentElement.webkitRequestFullScreen) { document.documentElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT); }\n"\
            "} else {\n"\
            "document.body.setAttribute('class', 'collapsed');\n"\
            "if (document.cancelFullScreen) { document.cancelFullScreen(); }\n"\
            "else if (document.mozCancelFullScreen) { document.mozCancelFullScreen(); }\n"\
            "else if (document.webkitCancelFullScreen) { document.webkitCancelFullScreen(); }\n"\
            "}\n"\
            "}\n"

        script.string += "function closeDropdown() {\n"\
            "menu.setAttribute('style', 'display: none;');\n"\
            "menuExpanded = false;\n"\
            "}\n"

        script.string += "function openDropdown(event) {\n"\
            "event.stopPropagation();\n"\
            "menu.setAttribute('style', (menuExpanded)? 'display:none;' : 'display:block;');\n"\
            "menuExpanded = !menuExpanded;\n"\
            "}\n"

        script.string += 'updateImage(0);'

        page.body.append(script)

        return page.prettify()



########## PRESENTATION SUBCLASSES ##########

class SlideShareScraper(PresentationScraper):
    thumbnail = "https://is1-ssl.mzstatic.com/image/thumb/Purple113/v4/03/df/99/03df99d1-48c0-d976-c0f3-3ad4a6af5b90/source/200x200bb.jpg"
    source = "SlideShare"
    img_selector = ('img', {'class': 'slide_image'})
    img_attr='data-normal'
    color = '#007BB6'

    @classmethod
    def test(self, url):
        return 'slideshare.net' in url
