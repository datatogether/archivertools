from setuptools import setup

setup(name = 'archivertools',
        version = '0.0.1.dev1',
        description = 'tools for use with Data Together morph.io archival scraping work',
        url = 'https://github.com/datatogether/archivertools',
        author = 'Jeffrey Liu',
        author_email = 'email.jeffrey.liu@gmail.com',
        license = 'GNU AGPL v3',
        packages = ['archivertools'],
        install_requires = ['scraperwiki',
            'requests'])

