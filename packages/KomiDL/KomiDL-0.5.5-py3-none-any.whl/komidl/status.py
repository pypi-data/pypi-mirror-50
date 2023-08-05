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
"""This module contains functions for drawing status messages"""

import sys


def _get_bars(bar_size: int, current: int, total: int) -> int:
    """Calculate the number of bars to display in the progress bar.

    Parameters
    ----------
    bar_size:   Total # of bars to be displayed
    current:    Current units
    total:      Total units required

    Returns
    -------
    The number of bars to display in the progress bar
    """
    return int((current*bar_size)/float(total))


def _get_percent(current: int, total: int) -> int:
    """Calculate the percentage of 'current' from 'total'.

    Parameters
    ----------
    current:    Current units
    total:      Total units required

    Returns
    -------
    The percentage of pages downloaded
    """
    return int(current*100/float(total))


def _progress_bar(string: str) -> None:
    """Print the progress bar message in-place"""
    sys.stdout.write("\r")
    sys.stdout.write(string)
    sys.stdout.flush()


def progress_start(title: str) -> None:
    """Print the starting download message.

    Parameters
    ----------
    title:      The title of the gallery that will be downloaded
    """
    sys.stdout.write(f"Downloading: {title}\n")


def progress_draw(bar_size: int, current: int, total: int) -> None:
    """Draw a progress bar.

    Parameters
    ----------
    bar_size:   Total # of bars to be displayed
    current:    Current units
    total:      Total units required
    """
    bars = _get_bars(bar_size, current, total)
    bar_str = '='*bars
    percent = _get_percent(current, total)
    _progress_bar(f"Progress:    [{bar_str:<{bar_size}}]{percent:>4}%")


def progress_fail(bar_size: int, current: int, total: int) -> None:
    """Draw a progress bar failing at a certain point.

    Parameters
    ----------
    bar_size:   Total # of bars to be displayed
    current:    Current units
    total:      Total units required
    """
    bars = _get_bars(bar_size, current, total)
    bar_str = '='*bars
    percent = _get_percent(current, total)
    _progress_bar(f"FAILED:      [{bar_str:<{bar_size}}]{percent:>4}%")


def progress_stop(bar_size: int, current: int, total: int) -> None:
    """Draw a progress bar stopped at a certain point.

    Parameters
    ----------
    bar_size:   Total # of bars to be displayed
    current:    Current units
    total:      Total units required
    """
    bars = _get_bars(bar_size, current, total)
    bar_str = '='*bars
    percent = _get_percent(current, total)
    _progress_bar(f"STOPPED:      [{bar_str:<{bar_size}}]{percent:>4}%")


def progress_finish(bar_size: int) -> None:
    """Draw a complete progress bar appended by a newline."""
    bar_str = '='*bar_size
    _progress_bar(f"Complete:    [{bar_str:<{bar_size}}]{100:>4}%")
    sys.stdout.write("\n")


def yn_prompt(prompt_msg: str, skip=False) -> bool:
    """Print a message with yes/no prompt and return user input.

    Parameters
    ----------
    prompt_msg : str
        A message/question to accompany the yes/no prompt

    Returns
    -------
    bool
        True if user entered yes, false if otherwise
    """
    if skip:
        return skip

    prompt_msg += " [y/N] "
    response = input(prompt_msg)
    return response.lower() == "y"
