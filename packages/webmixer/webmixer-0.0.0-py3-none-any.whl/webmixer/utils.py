#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from bs4 import BeautifulSoup
import re
import hashlib
from urllib.parse import urlparse
from webmixer.messages import MESSAGES


def guess_scraper(url, scrapers=None, allow_default=False, **kwargs):
    """
        Returns scraper where url passes `test` condition
        Args:
            url (str): URL to scrape
            scrapers ([<Scraper>]): other scrapers to test URL against
            allow_defualt (bool): use generic default scraper in case nothing matches
            **kwargs: any additional arguments to pass to scraper
    """
    from webmixer.scrapers.pages.base import COMMON_SCRAPERS, DefaultScraper

    scrapers = scrapers or []
    scrapers += COMMON_SCRAPERS
    if allow_default:
        scrapers.append(DefaultScraper)

    for scraper_class in scrapers:
        if scraper_class.test(url):
            return scraper_class(url, **kwargs)


def generate_filename(link, default_ext=None):
    """
        Returns a filename (str) to use for extracted files
        Args:
            link (str): URL that has been scraped
            default_ext (optional str): if the link doesn't have an extension, use this extension
    """
    _, ext = os.path.splitext(link.split('#')[0].split('?')[0])
    hash_object = hashlib.md5(link.encode('utf-8'))
    return "{}{}".format(hash_object.hexdigest(), ext or default_ext)


def get_absolute_url(url, endpoint=None):
    """
        Returns the absolute url based on the url and endpoint
        Args:
            url (str): base url with domain (e.g. https://domain.com)
            endpoint (str): link to convert to an absolute url (e.g. /image.png)
    """
    endpoint = endpoint.replace('%20', ' ').strip()
    if endpoint.strip().startswith('http'):
        return endpoint
    elif endpoint.startswith('//'):
        return 'https:{}'.format(endpoint)
    elif '../' in endpoint:
        jumps = len(list(section for section in endpoint.split('/') if section == '..'))
        url_sections = url.split('/')[:-(jumps + 1)] + endpoint.split('/')[jumps:]
        return '{}'.format('/'.join(url_sections))
    elif endpoint.startswith('/'):
        parsed = urlparse(url)
        return "{}://{}/{}".format(parsed.scheme, parsed.netloc, endpoint.strip('/'))
    return "/".join(url.split('/')[:-1] + [endpoint])


def create_tag(tag):
    """
        Returns a BeautifulSoup tag
        Args:
            tag (str): tag name to create (e.g. 'p')
    """
    return BeautifulSoup('', 'html.parser').new_tag(tag)


def create_copy_link_message(link, locale='en', color='rgb(153, 97, 137)', partially_scrapable=False, broken=False):
    """
        Returns a div tag with a link to copy/paste into browser
        Args:
            link (str): link to copy/paste
            locale (str): determines language of copy text
            color (str): primary color for element
            partially_scrapable (bool): link was mostly scraped, but doesn't include everything from original site
            broken (bool): link is broken (e.g. site no longer exists)
    """
    div = create_tag('div')
    div['style'] = 'text-align: center;'
    header_msg = ''
    subheader_msg = MESSAGES[locale]['copy_text']

    # Determine message to use for header
    if partially_scrapable:
        header_msg = MESSAGES[locale]['partially_supported']
        subheader_msg = MESSAGES[locale]['partially_supported_copy_text']
    elif broken:
        header_msg = MESSAGES[locale]['broken_link']
    else:
        header_msg = MESSAGES[locale]['not_supported']

    # Add "This content is not able to be viewed from within Kolibri"
    if header_msg:
        header = create_tag('p')
        header['style'] = 'font-size: 12pt;margin-bottom: 0px;color: {};font-weight: bold;'.format(color)
        header.string = header_msg
        div.append(header)

    # Add "Please copy this link in your browser to see the original source"
    subheader = create_tag('p')
    subheader['style'] = 'font-weight: bold;margin-bottom: 10px;color: #555;margin-top:5px;'
    subheader.string = subheader_msg
    div.append(subheader)

    # Add copy link section
    paragraph = create_tag('p')
    div.append(paragraph)
    copytext = create_tag('input')
    copytext['type'] = 'text'
    copytext['value'] = link
    copytext['style'] = 'width: 250px; max-width: 100vw;text-align: center;font-size: 12pt;'\
        'background-color: #EDEDED;border: none;padding: 10px;color: #555;outline:none;'
    copytext['readonly'] = 'readonly'
    copytext['id'] = "".join(re.findall(r"[a-zA-Z]+", link))
    paragraph.append(copytext)

    # Add copy button
    copybutton = create_tag('button')
    copybutton['style'] = 'display: inline-block;cursor: pointer;min-width: 64px;max-width: 100%;min-height: 36px;padding: 0 16px;margin: 8px;'\
        'overflow: hidden;font-size: 14px;font-weight: bold;line-height: 36px;text-align: center;text-decoration: none;text-transform: uppercase;'\
        'white-space: nowrap;cursor: pointer;user-select: none;border: 0;border-radius: 2px;outline: none;background-color:{};color:white;'.format(color)
    copybutton.string = MESSAGES[locale]['copy_button']
    copybutton['id'] = 'btn-{}'.format(copytext['id'])
    copybutton['onclick'] = '{}()'.format(copytext['id'][-15:])  # Keep unique in case there are other copy buttons on the page
    paragraph.append(copybutton)

    # Add copy script
    copyscript = create_tag('script')
    copyscript['class'] = ['skip-scrape']
    copyscript.string = "function {function}(){{ " \
                        "  let text = document.getElementById('{id}');" \
                        "  let button = document.getElementById('btn-{id}');" \
                        "  text.select();" \
                        "  try {{ document.execCommand('copy'); button.innerHTML = '{success}';}}" \
                        "  catch (e) {{ button.innerHTML = '{failed}'; }}" \
                        "  if (window.getSelection) {{window.getSelection().removeAllRanges();}}"\
                        "  setTimeout(() => {{ button.innerHTML = '{text}';}}, 2500);" \
                        "}}".format(
                            id=copytext['id'],
                            function=copytext['id'][-15:],
                            success=MESSAGES[locale]['copy_success'],
                            text=MESSAGES[locale]['copy_button'],
                            failed=MESSAGES[locale]['copy_error']
                        )
    div.append(copyscript)

    return div
