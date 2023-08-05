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
"""This module contains the Hentai2Read extractor class"""

import os
import re

from .extractor import Extractor


class Hentai2ReadEX(Extractor):
    """
    An extractor for Hentai2Read.com

    The image URLs come from a JavaScript variable embedded in the first page
    of the gallery (gData). Another quirk is that galleries on this site are
    spread throughout multiple pages.
    """
    def __init__(self):
        super().__init__()
        self.name = "Hentai2Read"
        self.url = "https://www.hentai2read.com"
        self._PAGE_PATTERN = r"https?://(?:www\.)?hentai2read\.com.*"
        self._GALLERY_PATTERN = r"https?://(?:www\.)?hentai2read\.com/[^/]*"
        self._IMG_DOMAIN = "https://static.hentaicdn.com/hentai"

    # =========================================================================
    # Getters
    # =========================================================================

    @staticmethod
    def _get_title(soup):
        title = soup.title.string
        return title.split("(")[0].strip()

    @staticmethod
    def _get_gallery_size(datavar):
        """Returns the total number of images in gallery"""
        for line in datavar:
            if "images" in line:
                return len(line.split(","))-1
        return None

    def _get_datavar(self, url):
        """Returns a list of all items in the gData variable

        gData is a variable in the site's JavaScript and is retrieved from the
        gallery page. It is useful for finding the gallery size and getting
        the image URLs.
        """
        # Download the first gallery page
        url = os.path.join(url, "1")
        soup = self._get_soup(url)
        # Get all instances of <script>
        scripts = soup.find_all("script")
        # Look for the tags that contain content
        #   (assume var gData is the first inst.)
        data = [tag for tag in scripts if len(tag.contents) > 0][0]
        # Strip the content, then split and strip each line to make a list
        return [line.strip() for line in data.contents[0].strip().splitlines()]

    def get_size(self, url, soup, args):
        datavar = self._get_datavar(url)
        return self._get_gallery_size(datavar)

    def get_gallery_urls(self, url, soup, args):
        datavar = self._get_datavar(url)

        url_list = []
        size = self._get_gallery_size(datavar)
        size_len = len(str(abs(size)))
        for line in datavar:
            if "images" in line:
                data_array = line.split(" ")[2]
                url_array = data_array.split(",")[:-1]

        for item in url_array:
            url = self._build_url(item)
            filename = self._build_filename(url, size_len)
            url_list.append([filename, url])
        return url_list

    def get_tags(self, url, soup, args):
        soup_tags = {"Title": self._get_title(soup), "URL": url}
        tags = soup.find_all("li", {"class": "text-primary"})
        for tag in tags:
            if tag.b and tag.find_all("a"):
                key = tag.b.string
                key += "s" if key[-1] != "s" else key
                items = self._clean_tags(tag)
                soup_tags[key] = items
        return soup_tags

    # =========================================================================
    # Misc. functions
    # =========================================================================

    def _build_url(self, item):
        """Return a URL for an item

        Removes any quotes, brackets, and backslashes.
        """
        image = re.sub(r'[\\"\[\]]', "", item)
        return self._IMG_DOMAIN + image

    @staticmethod
    def _build_filename(url, len_size):
        """Return a filename based on the image's URL and gallery size"""
        file_ = url.split("/")[-1]
        ext = file_.split(".")[-1]
        name = file_.split(".")[0][-len_size:]
        return f"{name}.{ext}"

    @staticmethod
    def _clean_tags(tags):
        """
        Build list from tags for the dictionary and format all entries
        """
        items = [item.string for item in tags.find_all("a")]
        # Remove empty "-" placeholder used by site
        items = ["" if item == "-" else item for item in items]
        # Remove newline char
        items = [re.sub(r"\n", "", item) for item in items]
        # Remove bracket content
        items = [item.split("(")[0].strip()
                 if "(" in item else item for item in items]
        return items
