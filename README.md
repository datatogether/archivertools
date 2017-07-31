# archivertools
This is a package of tools to be used for scraping websites via morph.io into the Data Together pipeline

## Installation
```
pip install archivertools
```

## Usage
The Archiver class provides all of the functionality
TODO: Fill in details

### Initialization:
```python
from archivertools import Archiver

url = 'http://example.org'
UUID = '0000'
archiver = Archiver(url,UUID)
```

### Saving child urls
For urls on the current page that should be ingested by the Data Together crawler
```python
archiver.addURL(url)
```

### Saving files/data
Add a local file to be uploaded to Data Together pipeline. Automatically computes hash

```python
comments='information about the file, such as encoding, metadata, etc' #optional
archiver.addFile(filename,comments)
```
