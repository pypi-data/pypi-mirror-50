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
"""This module contains the EHentai extractor class"""

import re
from multiprocessing.dummy import Pool as ThreadPool

from .extractor import Extractor


class EHentaiEX(Extractor):
    """
    An extractor for E-Hentai.org
    """
    def __init__(self):
        super().__init__()
        self.name = "E-Hentai"
        self.url = "https://www.e-hentai.org"
        self._PAGE_PATTERN = r"https?://(?:www\.)?e-hentai\.org.*"
        self._GALLERY_PATTERN = r"https?://(?:www\.)?e-hentai\.org/g/" + \
                                r"[0-9]+/[a-z0-9]+/?"

    # =========================================================================
    # Getters
    # =========================================================================

    @staticmethod
    def _get_title(soup):
        title = soup.title.string
        if "]" in title:
            title = title.split("]")[1]
        if "(" in title:
            if title[0] == "(":
                title = title.split("(")[1].split(")")[1]
            else:
                title = title.split("(")[0]

        delims = ("|", "[")
        for delim in delims:
            if delim in title:
                title = title.split(delim)[0]
        return title.strip()

    @staticmethod
    def _get_id(url):
        return url.split("/")[-3] if url[-1] == "/" else url.split("/")[-2]

    @staticmethod
    def _get_language(soup):
        tags = soup.find_all("td", {"class": "gdt1"})
        lang_tag = [tag for tag in tags if tag.string == "Language:"][0]
        return lang_tag.next_sibling.next_element.strip()

    @staticmethod
    def _get_display_block(soup):
        gpc = soup.find("p", {"class": "gpc"}).string.split("-")[1]
        return gpc.strip().split(" ")[0]

    def _get_sub_urls(self, soup, url):
        """E-Hentai has an intermediate URL to go through before loading the
           image

        Parameters
        ----------
        soup : BS4Soup
            The soup of the original URL gallery
        url : str
            The URL of the gallery

        Returns
        -------
        list
            A list of all intermediate URLs
        """
        sub_urls = []
        block = self._get_display_block(soup)
        size = self.get_size(url, soup, None)
        # Ceiling divide size/block
        pages = -(-size // int(block))
        for page in range(0, pages):
            page_url = f"{url}?p={page}"
            soup = self._get_soup(page_url)
            a_tags = soup.find_all("a")
            gallery_id = self._get_id(url)
            sub_tags = [link.get("href") for link in a_tags
                        if link.get("href") and gallery_id in link.get("href")]
            sub_urls += [url for url in sub_tags
                         if re.match(f".*{gallery_id}-[0-9]+$", url)]
        return sub_urls

    def _retrieve_img_url(self, url):
        """From the sub URL, get the image URL

        This is called by the pool starmap

        Returns
        -------
        str
            The image URL
        """
        soup = self._get_soup(url)
        return soup.find("img", {"id": "img"})["src"]

    def _get_img_urls(self, soup, url, args):
        sub_urls = self._get_sub_urls(soup, url)
        pool = ThreadPool(args.thread_size)
        img_urls = pool.map(self._retrieve_img_url, sub_urls)
        return img_urls

    def get_size(self, url, soup, args):
        tags = soup.find_all("td", {"class": "gdt2"})
        tags = [item.string for item in tags]
        pages = [item for item in tags
                 if item is not None and "pages" in item][0]
        return int(pages.split(" ")[0])

    def get_gallery_urls(self, url, soup, args):
        url_list = []
        size = self.get_size(url, soup, args)
        size_len = len(str(abs(size)))
        img_urls = self._get_img_urls(soup, url, args)
        for img_num in range(1, size+1):
            img_type = img_urls[img_num-1].split(".")[-1]
            base_name = str(img_num).zfill(size_len)
            filename = f"{base_name}.{img_type}"
            url_list.append([filename, img_urls[img_num-1]])
        return url_list

    def get_tags(self, url, soup, args):
        soup_tags = {"Title": self._get_title(soup),
                     "Languages": self._get_language(soup),
                     "Artists": [],
                     "Groups": [],
                     "URL": url}
        key_tags = soup.find_all("td", {"class": "tc"})
        for key in key_tags:
            key_name = key.string.title()[:-1]
            if key_name == "Languages":
                continue
            if key_name == "Artist":
                key_name += "s"
            items = key.next_element.next_element.find_all("a")
            tag_list = self._clean_tags(items)
            soup_tags[key_name] = tag_list
        return soup_tags

    # =========================================================================
    # Misc. functions
    # =========================================================================

    @staticmethod
    def _clean_tags(items):
        """Capitalize every word"""
        return [item.string.title() for item in items]
