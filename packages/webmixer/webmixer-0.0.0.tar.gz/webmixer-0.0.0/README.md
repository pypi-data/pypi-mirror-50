
# WebMixer

A library for scraping urls

## The Basic Scraper

All `webmixer.scrapers.pages` and `webmixer.scrapers.tags` classes inherit from `webmixer.base.BasicScraper`, which means they all have the following attributes and functions:

### Attributes
* directory (str): Directory to write files to
* color (str): Color for error messages (default: 'rgb(153, 97, 137)')
* locale (str): Language to use when writing error messages (default: 'en')
	* Note: must be listed in `webmixer.messages.MESSAGES`
* default_ext (str): Extension to default to for extracted files

### Functions
#### create_tag(tag)
Args:
* tag (str): tag name to create (e.g. 'p')

Returns a BeautifulSoup tag
Example:
```
image_tag = create_tag('img')
```
___

#### get_filename(link, default_ext=None)

Args:
* link (str): URL that has been scraped
* default_ext (optional str): if the link doesn't have an extension, use this extension'

Returns a filename (str) to use for extracted files
Example:
```
video_filename = get_filename('<url>', default_ext='.mp4')
```
___

#### mark_tag_to_skip(tag)
Mark tag to skip during further scraping operations
Args:
* tag (str): tag to mark

Example:
```
Process img tag here...

mark_tag_to_skip(img)
```
___

#### write_url(link, url=None, default_ext=None, filename=None, directory=None)
Downloads a url and writes it to a zip
Args:
* filepath (str): path to local file
* directory (str): directory to write to zip
* url (optional str): URL used for handling relative URLs
* default_ext (optional str): if the link doesn't have an extension, use this extension
* filename (optional str): name for file to write to zip
* directory (optional str): directory to write file to zip

Returns filepath within zip
Example:
```
write_url('<link>', url='https://domain.com/', default_ext='.mp4', filename='video', directory='media') # 'media/video.mp4'
```
___

#### write_contents(filename, contents, directory=None)
Writes contents to the zip with a given filename
Args:
* filename (str): filename for contents
* contents (bytes): contents to write to zip
* directory (str): directory to write to zip

Returns filepath within zip
Example:
```
write_contents('myfile.pdf', <pdf contents>, directory='docs')  # docs/myfile.pdf
```
___

#### write_file(filepath, directory=None)
Writes a local file to the zip
Args:
* filepath (str): path to local file
* directory (str): directory to write to zip

Returns filepath within zip
Example:
```
write_file('path/to/myfile.mp3', directory='music')  # music/myfile.mp3
```
___


#### create_broken_link_message(link)
Generates a tag with broken link message
Args:
* link (str): link to copy/paste

Returns a div tag with a link to copy/paste into browser
Example:
```
iframe.replaceWith(create_broken_link_message('<url>'))
# iframe -> <div>copy link...</div>
```
___

#### create_copy_link_message(link, partially_scrapable=False)
Generates a tag with 'copy link into browser' message
Args:
* link (str): link to copy/paste
* partially_scrapable (bool): link was mostly scraped, but doesn't include everything from original site

Returns a div tag with a link to copy/paste into browser
Example:
```
iframe.replaceWith(create_copy_link_message('<url>'))
# iframe -> <div>copy link...</div>
```
___

### Exceptions
`webmixer.exceptions` can be useful for handling errors from a variety of sources. If you are scraping a more specialized source, there may be some exceptions that are exclusive to that source. You can then raise the following exceptions to correctly manage that source:

#### BrokenSourceException
Used when the link is completely broken (e.g. site no longer exists)

#### UnscrapableSourceException
Used when the link is working, but cannot be supported on Kolibri (e.g. Flash content)

For instance, the `webmixer.scrapers.pages.gdrive.GoogleDriveScraper` may throw a `FileNotDownloadableError` error. In order to handle this correctly, it will raise an `UnscrapableSourceException`
```
try:
	...
except FileNotDownloadableError as e:
	raise UnscrapableSourceException(e)
```


## Page Scrapers
There are several page scrapers that are available for use in scraping html pages. These will download urls to their respective file types

### Built-in Scrapers
Here is a list of the basic scraper classes, which are also listed under `webmixer.scrapers.pages.base.COMMON_SCRAPERS`:
*  WebVideoScraper
* PDFScraper
* EPubScraper
* ImageScraper
* FlashScraper
* VideoScraper
* AudioScraper


### Using Page Scrapers
When you create a scraper object, you may specify the following:
* url (str): URL that tag can be found at (used to handle relative URLs) __required__
* zipper (optional `ricecooker.utils.html_writer`): Zip to write to
* triaged (optional [str]): List of already parsed URLs

To scrape the page, you may use any of the following writing options:

__to_zip__: Writes a file to self.zipper, which is useful when scraping embedded sources from an html page
Args:
* filename (optional str): name of file to write to
Returns path to file from within zip

Here are the default extensions for each `webmixer.scrapers.pages.base.Scraper`:
| Scraper | Extension |
|--|--|
| HTMLPageScraper  |.html |
|PDFScraper|.pdf|
| EPubScraper | .epub |
| AudioScraper | .mp3 |
| VideoScraper | .mp4 |
| WebVideoScraper | .mp4 |
|ImageScraper| .png |
|FlashScraper| _error_ |

For example:
```
from webmixer.scrapers.base import ImageScraper
image= <BeautifulSoup tag>
image['src'] = ImageScraper('<url>').to_zip()  # Sets 'src' to zipped image filepath
```
___

__to_tag__: Writes file to zip and generates a tag based on what kind of scraper it is. This is useful when you are replacing iframes with native html elements
Args:
* filename (optional str): name of file to write to
Returns tag

Here are the return tag types for each `webmixer.scrapers.pages.base.Scraper`:
| Scraper | Tag |
|--|--|
| HTMLPageScraper  | None|
|PDFScraper|\<embed\>|
| EPubScraper | None |
| AudioScraper | \<audio\> |
| VideoScraper | \<video\> |
| WebVideoScraper | \<video\> |
|ImageScraper|\<img\>|
|FlashScraper|_error_|

For example:
```
from webmixer.scrapers.base import PDFScraper
iframe= <BeautifulSoup tag>
iframe.replaceWith(PDFScraper('<url>').to_tag())  # Replaces iframe with <embed> tag
```

___

__to_file__: Writes to a file. This is useful for downloading URLs as files to your local machine.
Args:
* filename (optional str): name of file to write to
* directory (optional str): directory to write to
* overwrite (bool): overwrite file if it exists
Returns a filepath to the downloaded file

`to_file` uses the `download_file` method to write the file to a `write_to_path`

Here are the return file types for each `webmixer.scrapers.pages.base.Scraper`:
| Scraper | Extension |
|--|--|
| HTMLPageScraper  | .zip - generated by `ricecooker.utils.html_writer` |
|PDFScraper|.pdf |
| EPubScraper | .epub |
| AudioScraper | .mp3 |
| VideoScraper | .mp4 |
| WebVideoScraper | .mp4 |
|ImageScraper|_error - content kind not supported_  |
|FlashScraper|_error_ |

For example:
```
from webmixer.scrapers.base import HTMLPageScraper
new_html_zip_path = HTMLPageScraper('<url>').to_file() # Returns newly scraped html .zip file
```

### Custom Scrapers
Given how diverse the internet is, you may need to implement your own scraper to handle individual sources. You __must__ implement a `test` classmethod in order to use your scraper.

__If you would like to share a custom scraper, please feel free to open a pull request with a new file under `webmixer.scrapers.pages`__

#### Attributes
All scrapers have the following attributes:
* dl_directory (str): Directory to write `to_file` downloaded file to (default: 'downloads')
* directory (str): Directory to write files to
* color (str): Color for error messages (default: 'rgb(153, 97, 137)')
* locale (str): Language to use when writing error messages (default: 'en')
	* Note: must be listed in `webmixer.messages.MESSAGES`
* default_ext (str): Extension to default to for extracted files
* kind (`le_utils.constants.content_kind`): Content kind to write to

`webmixer.scrapers.pages.base.HTMLPageScraper` has these additional attributes:
* partially_scrapable (bool): Not all content can be viewed from within Kolibri (default: False)
* scrape_subpages (bool): Determines whether to scrape any subpages within this page (default: True)
* main_area_selector (optional tuple): Main element selector to replace everything in body tag
* omit_list (optional list): list of selectors to remove from page contents (e.g. [('a', {'class': 'link'})])
* loadjs (bool): Determines whether to load js when loading the page (default: True)
* scrapers ([`webmixer.scrapers.pages.Scraper`]): List of additional scrapers to use on this page
* extra_tags ([`webmixer.scrapers.tags.Tag`]): List of additional tags to scrape

For example, the following code will remove links, scrape Wikipedia pages, and sets all images to 'myimg.png':
```
from webmixer.scrpaers.tags import ImageTag
from webmixer.scrapers.pages.base import HTMLPageScraper
from webmixer.scrapers.pages.wikipedia import WikipediaScraper

class MyCustomTag(ImageTag):
	def process(self):
		self.tag['src'] = self.write_file('myimg.png')

class MyCustomScraper(HTMLPageScraper):
	omit_list = [('a',)]  		   # Remove links
	extra_tags = [MyCustomTag]     # Use MyCustomTag to set images to 'myimg.png'
	scrapers = [WikipediaScraper]  # Scrape any Wikipedia pages

	@classmethod                   # Required test classmethod
	def test(self, url):
		return 'my-domain.com' in url
```

#### Functions
__@classmethod test(url)__: Required method to determine if this is the correct scraper for this URL
Args:
  * url (str): url to test
Returns True if scraper is meant to scrape URL
Example:
```
@classmethod
def test(self, url):
	return 'somedomain' in url
```

___

__preprocess(contents)__: Process contents before main scraping method
Args:
	contents (BeautifulSoup): contents to preprocess
Example:
```
# Delete the first image on the page before scraping all the images
def preprocess(self, contents):
	contents.find('img').decompose()
```
___

__postprocess(contents)__: Process contents after main scraping method
Args:
	contents (BeautifulSoup): contents to postprocess
Example:
```
# Append a link at the end of the <body> tag
def postprocess(self, contents):
	link = self.create_tag('a')
	link.string = 'New Link'
	contents.body.append(link)
```


## Tags
There are several tags that are available for use in scraping html pages. These will handle downloading any referenced files.

### Using Tags
To create a tag, you may specify the following:
* tag (BeautifulSoup.tag): tag to parse __required__
* url (str): url that tag can be found at (used to handle relative URLs) __required__
* attribute (optional str): attribute to find link at (e.g. 'src' or 'data-src')
* scrape_subpages (optional bool): parse linked pages referenced by this tag (default: True)
* extra_scrapers (optional [`webmixer.scrapers.base.BasicScrapers`]): list of scrapers to try to scrape linked pages
* color (optional str): color for injected error messages (default: 'rgb(153, 97, 137)')

To scrape the tag, use the `scrape` method. This will process the tag so that it can be usable from within an html zip. Here is a simple scraping example:
```
from webmixer.scrapers.tags import ImageTag
image_tag = <BeautifulSoup.img tag>
image_scraper = ImageTag(image_tag, '<url>')
image_scraper.scrape()  # image_tag['src'] will point to downloaded image file in zip
```



### Built-in Tags
Here is a list of the available tags, which are also listed under `webmixer.scrapers.tags.COMMON_TAGS`

* ImageTag (img)
* AudioTag (audio)
* VideoTag (video)
* EmbedTag (embed)
* LinkTag (a) _Scrapes linked pages referenced by 'href' attribute_
* IframeTag (iframe) _Scrapes embedded pages referenced byon 'src' attribute_
* StyleTag (style) _Scrapes sheets referenced by 'href' attribute_
* ScriptTag (script) _Scrapes scripts referenced by 'src' attribute_


### Custom Tags
Depending on the source you are trying to scrape, you may need more specific methods for scraping a page. To create a custom tag, you will need to subclass `webmixer.scrapers.tags.BasicScraperTag`

#### Attributes
All tags have the following attributes:
* selector (tuple): BeautifulSoup selector to find tag (e.g. ('a', {'class': 'link'}))
* default_ext (str): Extension to use if link doesn't have an extension
* directory (str): Directory to write tag files to
* attributes (dict): Any attributes to assign to a tag
* default_attribute (str): Attribute that references files (default: 'src')
* scrape_subpages (bool): Determines whether to scrape any linked pages (default: True)
* extra_scrapers ([`webmixer.scrapers.base.BasicScrapers`]): List of additional scrapers to use for scraping linked pages
* color (str): Color for error messages (default: 'rgb(153, 97, 137)')
* locale (str): Language to use when writing error messages (default: 'en')
	* Note: must be listed in `webmixer.messages.MESSAGES`

Example:
```
from webmixer.scrapers.tags import BasicScraperTag

class MyVideoTag(BasicScraperTag):
	selector = ('video', {'class': 'video-class'})  # Select video.video-class
	directory = 'media'								# Files will be written to media folder
	attributes = {									# Videos will have width 100%
		'width': '100%'
	}
```


#### Built-in functions
For more custom scraping logic, you may also override the following methods:

__process()__: Makes the tag usable from within an html zip by downloading any referenced files
Example:
```
class MyVideoTag(BasicScraperTag):
	def process(self):
		# Scrape all of the <source> tags
	    for source in self.tag.find_all('source'):
	        BasicScraperTag(source, self.zipper, self.url).scrape()
```
___

__handle_error()__: Determines how to handle cases where the link is broken
Example:
```
class MyVideoTag(BasicScraperTag):
	def handle_error(self):
		self.tag.decompose()  # Just remove the element if it doesn't work
```
___

__handle_unscrapable()__: Determines how to handle cases where the link is not scrapable
Example:
```
class MyVideoTag(BasicScraperTag):
	def handle_unscrapable(self):
		self.tag.replaceWith(self.create_copy_link_message(self.link))
```


## Helper Functions
### webmixer.utils.guess_scraper
If you would like to determine which scraper to use based on a URL, you can use the `webmixer.utils.guess_scraper` method. This will accept the following arguments:
* url (str): URL to scrape
* scrapers ([`webmixer.scrapers.base.BasicScrapers`]): list of other scrapers to test URL against
* allow_defualt (optional bool): use generic default scraper in case nothing matches (default: False)

_You can also pass in additional arguments to scrapers with `kwargs`_

So a simple usage of `guess_scraper` might be:
```
from webmixer.utils import guess_scraper
scraper = guess_scraper('<url>', scrapers=[MyCustomScraper])
```
