
from setuptools import find_packages, setup

readme = open('README.md').read()

with open('docs/history.rst') as history_file:
    history = history_file.read()

requirements = [
    "requests>=2.11.1",
    "beautifulsoup4>=4.6.3",
    "ricecooker>=0.6.31",
    "le_utils>=0.1.19",
    "cssutils>=1.0.2",
    "google-api-python-client>=1.7.9",
    "google-auth-oauthlib>=0.4.0",
    "oauthlib>=3.0.1",
    "requests-oauthlib>=1.2.0",
    "youtube_dl>=2019.7.2",
]


setup(
    name="webmixer",
    packages = find_packages(),
    version="0.0.0",
    description="Library for scraping urls and downloading them as files",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    license="MIT",
    url="https://github.com/learningequality/webmixer",
    download_url="https://github.com/learningequality/webmixer/releases",
    keywords="scrapers webmixer web-mixer mixer scraper",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    author="Learning Equality",
    author_email='dev@learningequality.org',
)
