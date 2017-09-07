from setuptools import setup
import os
def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        result = f.read()
    return result

setup(name = 'archivertools',
        version = '0.0.2.dev1',
        description = 'tools for use with Data Together morph.io archival scraping work',
        url = 'https://github.com/datatogether/archivertools',
        author = 'Jeffrey Liu',
        author_email = 'email.jeffrey.liu@gmail.com',
        license = 'GNU AGPL v3',
        packages = ['archivertools'],
        install_requires =read('requirements.txt').splitlines()
        )

