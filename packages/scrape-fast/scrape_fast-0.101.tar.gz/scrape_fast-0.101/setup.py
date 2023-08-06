from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='scrape_fast',
    version='0.101',
    description='Common web scraping functions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Druidmaciek/scrape_fast',
    author='Maciej Janowski',
    author_email='maciekjanowski@icloud.com',
    packages=['scrape_fast', 'scrape_fast.browser',
              'scrape_fast.parser', 'scrape_fast.proxies',
              'scrape_fast.simple'],
    include_package_data=True,
    install_requires=[
        'requirements',
        'selenium',
        'bs4'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='development web scraping crawling data',
    python_requires='>=3.6',
    project_urls={
        'Bug Reports': 'https://github.com/Druidmaciek/scrape_fast/issues',
        'Funding': 'https://paypal.me/druidmaciek',
        #'Say Thanks!': None,
        'Source': 'https://github.com/Druidmaciek/scrape_fast'
    },
)

__author__ = "Maciej Janowski"
