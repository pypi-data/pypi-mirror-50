![alt_text](docs/images/komidl_img.png)


## Description

KomiDL (コミDL) is a command-line program that can download images and series
from web galleries.

Inspired by [youtube-dl](https://youtube-dl.org/), KomiDL is able to download
images from any supported website URL. It also supports tag extraction and
can export files downloaded to formats such as archives (zip, tar, gztar,
bztar) or PDF.

Custom extractors can be written by implementing the abstract Extractor class
and registering it to extractors.py.

As the program is currently in early stages of development, bugs are likely
to occur. Use the program at your own risk.

## Requirements

+ python 3.6+
+ requests
+ BeautifulSoup
+ Pillow

## Installation

As the program is currently in early stages of development, it is
recommended that you download and install the latest version from the git
repository's MASTER branch.

Go to the folder containing setup.py and run the following command:

```sh
python setup.py install
```

## Usage

![alt_text](docs/images/usage.gif)

Get help by running:

```sh
komidl -h
```

## Testing

Go to the folder containing setup.py and run the following command:

```sh
python setup.py test
```

## License
Copyright (c) 2019 DNSheng

Licensed under the [GNU GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).

See LICENSE for the full details.
