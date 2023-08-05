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
"""This module contains the MangaDex extractor class"""

import os
import re
import json
from multiprocessing.dummy import Pool as ThreadPool

from komidl.status import yn_prompt
from .extractor import Extractor


class MangaDexEX(Extractor):
    """
    An extractor for MangaDex.org
    """
    def __init__(self):
        super().__init__()
        self.name = "MangaDex"
        self.url = "https://www.mangadex.org"
        self._PAGE_PATTERN = r"https?://(?:www\.)?mangadex\.org.*"
        self._CHAPTER_PATTERN = r"https?://(?:www\.)?mangadex\.org/" + \
                                r"chapter/[0-9]+/[0-9]+/?"
        self._MANGA_PATTERN = r"https?://(?:www\.)?mangadex\.org/" + \
                              r"title/[0-9]+/[a-z-]+/?"
        self._POST_API = "https://mangadex.org/api/?id="
        self._IMG_DOMAIN = "https://mangadex.org/data/"

        self._STATUS_DICT = {1: "Ongoing", 2: "Completed", None: "Unknown"}
        self._GENRE_DICT = {1: "4-Koma", 2: "Action", 3: "Adventure",
                            4: "Award Winning", 5: "Comedy", 6: "Cooking",
                            7: "Doujinshi", 8: "Drama", 9: "Ecchi",
                            10: "Fantasy", 11: "Gender Bender", 12: "Harem",
                            13: "Historical", 14: "Horror", 15: "Josei",
                            16: "Martial Arts", 17: "Mecha", 18: "Medical",
                            19: "Music", 20: "Mystery", 21: "Oneshot",
                            22: "Psychological", 23: "Romance",
                            24: "School Life", 25: "Sci-Fi", 26: "Seinen",
                            27: "Shoujo", 28: "Shoujo Ai", 29: "Shounen",
                            30: "Shounen Ai", 31: "Slice of Life", 32: "Smut",
                            33: "Sports", 34: "Supernatural", 35: "Tragedy",
                            36: "Webtoon", 37: "Yaoi", 38: "Yuri",
                            39: "[no chapters]", 40: "Game", 41: "Isekai"}

        self._manga_data = None
        self._chapter_data = None
        self._chapter_data_list = []

    # ===============================================================================
    # State checks
    # ===============================================================================

    def is_gallery(self, url):
        return self._is_chapter(url) or self._is_manga(url)

    def _is_chapter(self, url):
        return bool(re.match(self._CHAPTER_PATTERN, url))

    def _is_manga(self, url):
        return bool(re.match(self._MANGA_PATTERN, url))

    @staticmethod
    def _is_multilang(m_data):
        """Return number of different languages for all chapters in m_data"""
        lang_list = {m_data["chapter"][ch_id]["lang_code"]
                     for ch_id in m_data["chapter"].keys()}

        return bool(len(lang_list) > 1)

    # ===============================================================================
    # State modifiers
    # ===============================================================================

    def reset(self):
        """Clear all instance variables"""
        self._manga_data = None
        self._chapter_data = None
        self._chapter_data_list = []

    def _retrieve_chapter_data(self, url, chapter_id=None):
        # Add a sleep? Maybe
        """Get the data for a manga chapter and store in a class variable"""
        if not self._chapter_data or not url:
            if not chapter_id:
                chapter_id = self._get_data_id(url)
            data_url = self._POST_API + chapter_id + "&type=chapter"
            response = self._session.get(data_url, verify=False)
            response.raise_for_status()
            self._chapter_data = json.loads(response.content.decode("utf-8"))
        return self._chapter_data

    def _retrieve_manga_data(self, url, manga_id=None):
        """Get the data for a manga and store in a class variable"""
        if not self._manga_data:
            if not manga_id:
                manga_id = self._get_data_id(url)
            data_url = self._POST_API + str(manga_id) + "&type=manga"
            response = self._session.get(data_url, verify=False)
            response.raise_for_status()
            self._manga_data = json.loads(response.content.decode("utf-8"))
        return self._manga_data

    def _retrieve_cdl(self, m_data, args):
        """Retrieve chapter data list"""
        if not self._chapter_data_list:
            pool = ThreadPool(args.thread_size)
            url_list = [(None, ch_id) for ch_id in m_data["chapter"].keys()
                        if m_data["chapter"][ch_id]["lang_code"] in args.lang]
            # If the preferred language is not found
            if not url_list:
                if self._is_multilang(m_data):
                    # If there are multiple languages, then raise an exception
                    raise ValueError(f"Preferred language ({args.lang[0]}) " +
                                     "not found")
                # Otherwise, prompt for download in found language
                print(f"Warning: Preferred language ({args.lang[-1]}) " +
                      "not found")
                dl = yn_prompt("Download gallery in only available language?",
                               skip=args.yes)
                if not dl:
                    raise ValueError(f"Preferred language ({args.lang[0]}) " +
                                     "not found")

                url_list = [(None, ch_id) for ch_id in m_data['chapter']]

            self._chapter_data_list = pool.starmap(self._retrieve_chapter_data,
                                                   url_list)
        return self._chapter_data_list

    # ===============================================================================
    # Getters
    # ===============================================================================

    @staticmethod
    def _get_data_id(url):
        """Get the ID of the for data GET request"""
        return url.split("/")[-3] if url[-1] == "/" else url.split("/")[-2]

    @staticmethod
    def _get_size_data(c_data):
        """From a chapter data, retrieve size"""
        return int(len(c_data["page_array"]))

    @staticmethod
    def _get_title(m_data):
        """Get title of manga from manga_data"""
        return m_data["manga"]["title"]

    @staticmethod
    def _get_artist(m_data):
        return m_data["manga"]["artist"]

    @staticmethod
    def _get_author(m_data):
        return m_data["manga"]["author"]

    def get_size(self, url, soup, args):
        """Get the number of images to download"""
        size = 0
        if self._is_manga(url):
            m_data = self._retrieve_manga_data(url)
            chapter_data_list = self._retrieve_cdl(m_data, args)
            for chapter in chapter_data_list:
                size += self._get_size_data(chapter)
        elif self._is_chapter(url):
            if not self._chapter_data:
                self._retrieve_chapter_data(url)
            size = self._get_size_data(self._chapter_data)
        return int(size)

    def _get_chapter_urls(self, c_data, ch_path=""):
        """Same output as get_gallery_urls, but for a single chapter"""
        url_list = []
        size = self._get_size_data(c_data)
        size_len = len(str(abs(size)))
        for img_num, sub_url in enumerate(c_data["page_array"]):
            img_type = sub_url.split(".")[-1]
            img_name = f"{str(img_num+1).zfill(size_len)}.{img_type}"
            filename = os.path.join(ch_path, img_name)
            if c_data["server"] == "/data/":
                img_url = f"{self._IMG_DOMAIN + c_data['hash']}/{sub_url}"
            else:
                img_url = f"{c_data['server'] + c_data['hash']}/{sub_url}"
            url_list.append([filename, img_url])
        return url_list

    def _get_manga_urls(self, url, args):
        """Same output as get_gallery_urls, but for all chapters of a manga"""
        url_list = []
        m_data = self._retrieve_manga_data(url)
        # Download each chapter's data from the URL
        ch_data_list = self._retrieve_cdl(m_data, args)
        for ch in ch_data_list:
            num = ch["chapter"]
            ch_path = "Chapter " + num.zfill(4)
            url_list += self._get_chapter_urls(ch, ch_path)
        return url_list

    def get_gallery_urls(self, url, soup, args):
        url_list = []
        if self._is_chapter(url):
            if not self._chapter_data:
                self._retrieve_chapter_data(url)
            url_list = self._get_chapter_urls(self._chapter_data)
        elif self._is_manga(url):
            url_list = self._get_manga_urls(url, args)
        return url_list

    def get_tags(self, url, soup, args):
        tags = {"URL": url}
        # Ensure that manga_data is set
        if self._is_chapter(url):
            if not self._chapter_data:
                self._retrieve_chapter_data(url)
            c_data = self._chapter_data
            m_data = self._retrieve_manga_data(url,
                                               manga_id=c_data["manga_id"])
        else:
            # is_manga
            m_data = self._retrieve_manga_data(url)
            c_data = None
            # Retrieve chapter data for _get_langs to work
            self._retrieve_cdl(m_data, args)
        # Start scraping tags
        tags["Title"] = self._get_title(m_data)
        tags["Languages"] = self._get_langs()
        tags["Artists"] = self._get_artist(m_data)
        tags["Authors"] = self._get_author(m_data)
        tags["Chapters"] = self._get_chapters(url, m_data, c_data)
        tags["Category"] = self._get_categories(m_data)
        tags["Status"] = self._get_status(m_data)
        return tags

    def _get_langs(self):
        if self._chapter_data:
            return self._chapter_data["lang_name"]
        return self._chapter_data_list[0]["lang_name"]

    def _get_chapters(self, url, m_data, c_data):
        chapters = ""
        if self._is_chapter(url):
            chapters = c_data['chapter'].zfill(4)
        elif self._is_manga(url):
            last_chapter = sorted(m_data['chapter'].keys(), key=int)[-1]
            end = m_data['chapter'][last_chapter]['chapter'].zfill(4)
            chapters = "0001-" + end
        return chapters

    def _get_categories(self, m_data):
        return [self._GENRE_DICT[genre] for genre in m_data["manga"]["genres"]]

    def _get_status(self, m_data):
        return self._STATUS_DICT[m_data["manga"]["status"]]
