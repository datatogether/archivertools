# archivertools
<!-- Repo Badges for: Github Project, Slack, License-->

[![GitHub](https://img.shields.io/badge/project-Data_Together-487b57.svg?style=flat-square)](http://github.com/datatogether)
[![Slack](https://img.shields.io/badge/slack-Archivers-b44e88.svg?style=flat-square)](https://archivers-slack.herokuapp.com/)
[![License](https://img.shields.io/github/license/datatogether/archivertools.svg)](./LICENSE) 

This is a package of tools to be used for scraping websites via morph.io into the Data Together pipeline.

## License & Copyright

Copyright (C) 2017 Data Together  
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free Software
Foundation, version 3.0.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.

See the [`LICENSE`](./LICENSE) file for details.

## Getting Involved

We would love involvement from more people! If you notice any errors or would like to submit changes, please see our [Contributing Guidelines](./.github/CONTRIBUTING.md). 

We use GitHub issues for [tracking bugs and feature requests](https://github.com/datatogether/archivertools/issues) and Pull Requests (PRs) for [submitting changes](https://github.com/datatogether/archivertools/pulls)

### Getting Started and Style Guides
Refer to these resources to learn more about using Github, best practices for writing Python code, code linters to analyze your code for errors, and writing docstrings which describes what functions do.

- [How to use Git Version Control](https://try.github.io/levels/1/challenges/1)
- [Github's "Hello, World" Guides](https://guides.github.com/activities/hello-world/)
- [PEP8 Python style guide](https://www.python.org/dev/peps/pep-0008/)
- Python linters automatically check your code for style errors:
  - [PEP8 command line](https://pypi.python.org/pypi/pep8)
  - [PEP8 online](http://pep8online.com/)
  - [sublime text PEP8](https://github.com/SublimeLinter/SublimeLinter-pep8)
  - [pycodestyle for Atom](https://github.com/AtomLinter/linter-pycodestyle)
  - [flake8 for vim](https://github.com/nvie/vim-flake8)
  - [flymake and flake8 for emacs](https://www.emacswiki.org/emacs/PythonProgrammingInEmacs#toc18 )
- Function documentation should follow the [Google-style Python docstring format](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
  - [sublime text autodocstring](https://packagecontrol.io/packages/AutoDocstring)

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

os.environ['MORPH_DT_API_KEY'] = 'the_text_of_your_dt_api_key'
```

The Archiver class provides the interface for saving data that will be ingested onto Data Together. All of the data and files are stored in a local sqlite database called `data.sqlite`. It is important that you call the `Archiver.commit()` function at the end of your run to ensure that the data is ingested.

### Initialization
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

