# archivertools
This is a package of tools to be used for scraping websites via morph.io into the Data Together pipeline

## Installation
Tested with Python 2.7, 3.6

Install via pip
```
pip install archivertools
```


## Usage
In order to authenticate to the Data Together servers, make sure the environment variable `MORPH_DT_API_KEY` is set. To do this in morph.io, see [the morph documentation on secret values](https://morph.io/documentation/secret_values#reading-python).

For testing on your local system, you can set an environment variable within python using the `os` package
```python
import os

os.environment['MORPH_DT_API_KEY'] = 'the_text_of_your_dt_api_key'
```

The Archiver class provides the interface for saving data that will be ingested onto Data Together. All of the data and files are stored in a local sqlite database called `data.sqlite`. It is important that you call the `Archiver.commit()` function at the end of your run to ensure that the data is ingested.

### Initialization:
```python
from archivertools import Archiver

url = 'http://example.org'
UUID = '0000'
a = Archiver(url,UUID)
```

### Saving child urls
For urls on the current page that will be ingested by the Data Together crawler. The 
```python
url = 'http://example.org/links'
a.addURL(url)
```

### Saving files
Add a local file to be uploaded to Data Together pipeline. Automatically computes hash

```python
filename='example_file.csv'
comments='information about the file, such as encoding, metadata, etc' # optional
a.addFile(filename,comments)
```

### Committing
Run this function at the end of your scraper to let Data Together know that your scraper has finished running. It will authenticate with Data Together and begin the upload process
```python
a.commit()
```

