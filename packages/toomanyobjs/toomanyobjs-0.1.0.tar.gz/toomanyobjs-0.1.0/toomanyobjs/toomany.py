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

class TooMany:
    """Stores arbitrary class instances (like a singleton) and lets you get them back"""

    def __init__(self):
        """Initialize the objects and the associated metadata"""
        self.objects = {}

    def add(self, inst, overwrite=False):
        """Add a class instance.
        Set overwrite to True if you want to overwrite any existing instances"""
        try:
            self.objects[inst.__class__] # Check if a class has an instance
        except KeyError:
            self.objects[inst.__class__] = inst # If it doesn't exist, add it
        else:
            if overwrite:
                self.objects[inst] = inst

    def get(self, clss: object, args: tuple = ()):
        """Get a class instance or make a new one of it doesn't exist"""
        try:
            return self.objects[clss] # Try to return existing instance
        except KeyError:
            self.objects[clss] = clss(args)
            return self.objects[clss] # If there is none, make a new one with the specified args
    
    def share_object(self):
        for objs in self.objects:
            objs._TooMany = self