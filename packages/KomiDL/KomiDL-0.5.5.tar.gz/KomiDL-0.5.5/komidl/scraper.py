# KomiDL - A gallery downloader
# Copyright (C) 2019 DNSheng
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""This module contains the Scraper class"""

import os
import sys
import imghdr
import shutil
from multiprocessing.dummy import Lock
from multiprocessing.dummy import Pool as ThreadPool

import requests
from bs4 import BeautifulSoup

import komidl.status as status
import komidl.constants as constants
from komidl.exceptions import ExtractorFailed, InvalidURL


class Scraper:
    """Download all images from a URL with an extractor.

    The Scraper class given a URL and extractor will work to create directories
    and download the images, as well as write tags to files. File downloading
    is multi-processed and thus requires a mutex lock in order to update
    _downloaded (tracks current download progress for the URL) and to print
    the current status to the screen.
    Scraper also has a session object that is shared among methods, and
    must be used for all web requests.
    """
    def __init__(self, extractor=None):
        self.extractor = extractor
        self._lock = Lock()
        self._session = requests.Session()
        self._session.headers = {"User-Agent": constants.USER_AGENT,
                                 "Accept-encoding": "gzip, deflate"}
        requests.packages.urllib3.disable_warnings()
        self._gallery_size = 0
        self._downloaded = 0

    @staticmethod
    def _soup_request(session: requests.Session, url: str):
        """Returns a BS4 soup from the URL's response

        The request is done using the session.
        """
        request = session.get(url, verify=False)
        request.raise_for_status()
        content = request.content
        return BeautifulSoup(content, "html.parser")

    def reset(self) -> None:
        """Resets the state of the Scraper after use"""
        # Reset gallery size
        self._gallery_size = 0
        # Rebuild lock if dereferenced after InvalidURL exception
        if not self._lock:
            self._lock = Lock()

    @staticmethod
    def _get_extension(url: str):
        """Returns the path and extension of a URL.

        Acts exactly like os.path.splitext(), but without the '.' char in
        the extension.
        """
        path, ext = os.path.splitext(url)
        return path, ext[1:]

    @staticmethod
    def _write_image(img: str, dest: str) -> None:
        """Saves the response of an image request to the dest path."""
        with open(dest, "wb") as file_:
            for chunk in img.iter_content(chunk_size=1024):
                file_.write(chunk)

    def _retry_download_image(self, filename: str, url: str) -> None:
        """Retries downloading an image by using alternate extensions/formats

        Alternate image formats are defined in constants.COMMON_FORMATS.

        Raises an ExtractorFailed exception if all attempts using alternate
        image formats have been exhausted.
        """
        current_ext = self._get_extension(url)
        other_exts = (ext for ext in constants.COMMON_FORMATS
                      if ext != current_ext)
        # Exhaustively try other image formats
        for ext in other_exts:
            new_url = self._change_extension(url, ext)
            response = self._session.get(new_url, stream=True, verify=False)
            if response.status_code == 200:
                self._write_image(response, filename)
                break
        else:
            raise ExtractorFailed(f"Extractor returned an invalid URL: {url}")

    def _download_image(self, filename: str, url: str) -> None:
        """Downloads an image from the URL and saves it to filename.

        Failure to download an image (HTTP 404) may be caused by a wrong
        extension from the extractor. On failure, various other extensions are
        exhaustively tried. If the image can't be downloaded, then the gallery
        should be failed as well.

        Downloading an image updates the status bar, and thus the mutex lock
        is acquired before incrementing and drawing.

        In case the 'URL' or 'filename' argument was incorrect, after a
        successful download the magic bytes of the image is checked and the
        image's file extension may be modified.

        Returns the full path of the downloaded image
        """
        img = self._session.get(url, stream=True, verify=False)
        if img.status_code == 200:
            self._write_image(img, filename)
        elif img.status_code == 404:
            self._retry_download_image(filename, url)
        else:
            raise InvalidURL(f"Server error encountered at: {url}")

        self._lock.acquire()
        self._downloaded += 1
        status.progress_draw(constants.STATUSBAR_LEN, self._downloaded,
                             self._gallery_size)
        self._lock.release()

        return self._fix_extension(filename)

    @staticmethod
    def _fix_extension(image: str) -> str:
        """Renames the image's file extension based on the magic bytes found.

        If magic bytes could not be found, the image's path is not modified.

        Returns image's path with true file extension
        """
        cur_ext = Scraper._get_extension(image)
        actual_ext = imghdr.what(image)
        if actual_ext is not None:
            if cur_ext != actual_ext:
                new_image = Scraper._change_extension(image, actual_ext)
                os.rename(image, new_image)
                return new_image
        return image

    @staticmethod
    def _change_extension(url: str, ext: str) -> str:
        """Replaces the URL's file extension."""
        base_url, _ = os.path.splitext(url)
        return f"{base_url}.{ext}"

    @staticmethod
    def _create_dir(title: str, root_dir: str, overwrite=False) -> str:
        """Creates a directory to hold all downloaded files.

        The directory is created in the root directory, which is defined by
        the --directory argument (by default it is where the user ran the
        script).
        If the root directory does not exists, an exception is raised.
        If 'overwrite' is set, then any existing folder is automatically
        overwritten. Otherwise, a prompt will appear to give the user
        the option to overwrite or create the directory with a new name.

        Returns the full path of the newly created directory.
        """
        root_dir = os.path.abspath(root_dir)
        dest = os.path.join(root_dir, title)

        try:
            os.mkdir(dest)
        except FileExistsError:
            if not overwrite:
                prompt_msg = f"{dest} already exists. Overwrite?"
                overwrite = status.yn_prompt(prompt_msg)
            if overwrite:
                shutil.rmtree(dest)
            else:
                duplicates = sum(1 for dir_ in os.listdir(root_dir)
                                 if title in dir_)
                dest = f"{dest} ({duplicates})"
            os.mkdir(dest)

        return dest

    @staticmethod
    def _append_path(path: str, gallery_urls):
        """Appends the path to all image paths in gallery_urls."""
        for img, url in gallery_urls:
            yield os.path.join(path, img), url

    @staticmethod
    def _create_subdirs(path, gallery_urls) -> None:
        """Create all sub-directories from paths in gallery_urls."""
        img_urls = Scraper._append_path(path, gallery_urls)
        img_paths = (os.path.split(img) for img, _ in img_urls)
        for sub_dir, _ in img_paths:
            os.makedirs(sub_dir, exist_ok=True)

    def scrape(self, url: str, args) -> str:
        """Scrapes an image gallery at the URL.

        Using the extractor set within the object, if the URL given is a
        gallery then it is used to scrape.

        Raises an InvalidURL exception if the given URL or scraped image URL
        could not be requested.

        Raises an ExtractorFailed exception if an error was encountered within
        the extractor.

        Raises a ValueError exception if any argument values are incorrect.

        Returns the full path of the directory containing all scraped images.
        """
        self._downloaded = 0

        soup = self._soup_request(self._session, url)

        if not self.extractor.is_gallery(url):
            raise InvalidURL(f"'{url}' is not a valid image gallery for the "
                             f"'{self.extractor.name}' extractor")
        try:
            directory = self.scrape_gallery(soup, url, args)
        finally:
            self.extractor.reset()

        return directory

    def _fail(self, path=None) -> None:
        """Print a failure message and delete all loose files.

        The mutex lock for Scraper is destroyed to prevent further writing by
        the downloading sub-processes.
        """
        self._lock.acquire()
        status.progress_fail(constants.STATUSBAR_LEN, self._downloaded,
                             self._gallery_size)
        self._lock = None
        if path is not None:
            shutil.rmtree(path)

    def _download_images(self, path, urls, thread_size: int) -> None:
        """Download images from the urls to the path"""
        img_urls = self._append_path(path, urls)
        pool = ThreadPool(thread_size)
        try:
            pool.starmap(self._download_image, img_urls)
        finally:
            pool.close()
            pool.join()

    def scrape_gallery(self, soup, url, args) -> str:
        """Scrape a URL and download all images.

        Tags are written to a file if the --tags option is selected.

        In the process, the directory to hold all scraped info is created.
        """
        # Gather info for progress bar img downloading, create dest directory
        tags = self.extractor.get_tags(url, soup, args)
        title = self._build_title(tags)
        path = self._create_dir(title, args.directory, overwrite=args.yes)
        _, dirname = os.path.split(path)
        self._gallery_size = self.extractor.get_size(url, soup, args)

        # Start scraping process
        status.progress_start(dirname)
        try:
            gallery_urls = self.extractor.get_gallery_urls(url, soup, args)
            # Create the sub-directories if needed
            self._create_subdirs(path, gallery_urls)
            # Start downloading images
            self._download_images(path, gallery_urls, args.thread_size)
        except (ExtractorFailed, InvalidURL, KeyboardInterrupt) as e:
            self._fail(path=path)
            raise e
        # Write tags
        if args.tags:
            self._write_tags(tags, path)
        status.progress_finish(constants.STATUSBAR_LEN)

        return path

    @staticmethod
    def _build_title(tags: dict) -> str:
        """Build a name for the directory containing downloaded images"""
        def langs_tostr(langs: str) -> str:
            """Return language as an ISO 639-1 abbreviation"""
            # Get the first language if the value is a list
            if isinstance(langs, list):
                language, *_ = langs
            else:
                language = langs
            return constants.LANG_TO_ISO[language.title()]

        def build_credit_tag(tags: dict) -> str:
            """Credit the author/artist/group of the gallery for the title

            Priority of: Authors -> Artists -> Groups -> UNKNOWN
            """
            credit = tags.get('Authors',
                              tags.get('Artists',
                                       tags.get('Groups',
                                                'Unknown')))
            if isinstance(credit, list):
                return "x".join(name.upper() for name in credit)
            return credit.upper()

        title = tags.get('Title', 'UNTITLED')
        language = langs_tostr(tags['Languages'])
        credit = build_credit_tag(tags)
        chapters = tags.get('Chapters')
        chapter_tag = f"[{chapters}] " if chapters else " "
        return f"[{credit}][{language}]{chapter_tag}{title}"

    @staticmethod
    def _write_tags(tags, path):
        """Writes tags to a text file path"""
        info_str = Scraper._tags_tostr(tags)
        info_file = os.path.join(path, "info.txt")
        with open(info_file, "w") as file_:
            file_.write(info_str)

    @staticmethod
    def _tags_tostr(tags):
        """Returns tags as a string of format: 'KEY:ITEM,ITEM,ITEM'"""
        valid_keys = [key for key in tags if tags[key]]
        item_strs = (','.join(tags[key]) if isinstance(tags[key], list)
                     else tags[key] for key in valid_keys)
        tag_strs = (f"{key}:{item_str}\n"
                    for key, item_str in zip(valid_keys, item_strs))
        return "".join(tag_strs)
