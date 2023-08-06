"""
    toomanyobjs - a simple object instance sharing and storage library

    Copyright (C) 2019  Kevin Froman
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import shelve
import pickle
from typing import NewType

from . import toomany

TooMany = toomany.TooMany
NewType("TooMany", object)

def import_raw(too_many: bytes) -> TooMany:
    return pickle.loads(too_many)

def get(cache_name: str) -> TooMany:
    """Return a stored TooMany object"""

    with shelve.open(cache_name) as shelf:
        return shelf["toomany"]

def store(cache_name: str, data: TooMany, write_out: bool = False):
    """Store a TooMany object"""

    if write_out:
        return pickle.dumps(data)

    with shelve.open(cache_name) as shelf:
        shelf["toomany"] = data

    return b""
