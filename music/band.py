"""The class representing the concept of a music group/band.
It includes a list of Musician objects (band members) and the date when the band started performing together.

The corresponding exception classes are included as well.
File I/O and JSON encoding/decoding of Band objects are demonstrated too.
"""


#%%
# Setup / Data

import pickle
from datetime import date, datetime, time
import json
import sys

from music.musician_module import Musician
from util.utility import format_date, get_project_dir, get_data_dir

from testdata.musicians import *


#%%
class Band():
    """The class describing the concept of a music group/band.
    It includes a list of Musician objects (band members)
    and the dates when the band started/stopped performing together.
    """

    # Class variables: like static fields in Java; typically defined and initialized before __init__()
    # Insert a class variable (static field), such as genres, date_pattern,...

    genres = ['rock', 'blues', 'alternative', ]

    def __init__(self, name, *members, start=date.today(), end=date.today()):
        # Code to check if the band name is specified correctly (possibly raises BandNameError)

        band_name_error = not isinstance(name, str) or (len(name) < 2)
        if band_name_error:
            raise BandNameError(name)

        self.name = name
        self.members = members
        self.start = start
        self.end = end

        # self.__i = 0                                  # introduce and initialize iterator counter, self.__i

    def __str__(self):
        n = f'{self.name}'
        n += ': ' if self.members else ' '
        m = ', '.join([str(m) for m in self.members]) if self.members else ''
        s = str(self.start.year)
        e = str(self.end.year)
        return f'{n}{m} ({s}-{e})'

    def __eq__(self, other):
        # Musician objects are unhashable, so comparing the members tuples from self and other directly does not work;
        # see https://stackoverflow.com/a/14721133/1899061, https://stackoverflow.com/a/17236824/1899061
        # return self == other if isinstance(other, Band) else False    # No! Musician objects are unhashable!
        # However, this works:
        # return self.__dict__ == other.__dict__ if isinstance(other, Band) else False

        # # members must be compared 'both ways', because the two tuples can be of different length
        # m_diff_1 = [x for x in self.members if x not in other.members]
        # m_diff_2 = [x for x in other.members if x not in self.members]
        # m = len(m_diff_1) == len(m_diff_2) == 0

        # members must be compared 'both ways', because the two tuples can be of different length

        t = isinstance(other, Band)
        n = self.name == other.name
        m = all([x in self.members for x in other.members]) and all([x in other.members for x in self.members])
        s = self.start.year == other.start.year
        e = self.end.year == other.end.year

        return t and n and m and s and e

    @staticmethod
    def is_date_valid(d):
        """It is assumed that a band does not perform together since more than ~60 years ago.
        So, the valid date to denote the start of a band's career is between Jan 01, 1960, and today.
        """

        return date(1960, 1, 1) <= d <= date.today() if isinstance(d, date) else False

    def __iter__(self):
        """Once __iter__() and __next__() are implemented in a class,
        we can create an iterator object by calling the iter() built-in function on an object of the class,
        and then call the next() built-in function on that object.
        It is often sufficient to just return self in __iter__(),
        if the iterator counter such as self.__i is introduced and initialized in __init__().
        Alternatively, the iterator counter (self.__i) is introduced and initialized here.
        """

        self.__i = 0
        return self               # sufficient if the iterator counter is introduced and initialized in __init__()

    def __next__(self):
        if self.__i <= len(self.members):
            m = self.members[self.__i]
            self.__i += 1
            return m
        else:
            raise StopIteration


#%%
# Check class variables
print(Band.genres)

#%%
# Test the basic methods (__init__(), __str__(),...)
the_beatles = Band('The Beatles', *[johnLennon, paulMcCartney, georgeHarrison, ringoStarr],
                   start=date(1962, 10, 5), end=date(1970, 4, 11))
print(the_beatles)
print(the_beatles == Band('The Beatles', *[johnLennon, paulMcCartney, georgeHarrison, ringoStarr],
                          start=date(1962, 10, 5), end=date(1970, 4, 11)))
print(the_beatles.genres)

#%%
# Test the date validator (@staticmethod is_date_valid(<date>))
print(Band.is_date_valid(date(1950, 4, 2)))

#%%
# Test the iterator
m_iterator = iter(the_beatles)
# print(type(m_iterator))
while True:
    try:
        m = next(the_beatles)
        print(m)
    except:
        break
print('Done')
# m = next(the_beatles)             # No! The iterator is exhausted
m_iterator = iter(the_beatles)
print(next(the_beatles))

#%%
def next_member(band):
    """Generator that shows members of a band, one at a time.
    yield produces a generator object, on which we call the next() built-in function.
    A great tutorial on generators: https://realpython.com/introduction-to-python-generators/.
    """

    for m in band.members:
        input('Next: ')
        yield m
        print('Yeah!')


#%%
# Test next_member(band)

m_gen = next_member(the_beatles)
print(type(m_gen))
while True:
    try:
        print(next(m_gen))
    except:
        break
print('Done')


#%%
# Demonstrate generator expressions
ge = (i**2 for i in range(5))
print(type(ge))
print(next(ge))
print(next(ge))
print(next(ge))
print(next(ge))
print(next(ge))
# print(next(ge))                   # No! The generator is exhausted!


#%%
class BandEncoder(json.JSONEncoder):
    """JSON encoder for Band objects (cls= parameter in json.dumps()).
    """

    def default(self, band):
        # recommendation: always use double quotes with JSON

        pass


#%%
def band_py_to_json(band):
    """JSON encoder for Band objects (default= parameter in json.dumps()).
    """


#%%
def band_json_to_py(band_json):
    """JSON decoder for Band objects (object_hook= parameter in json.loads()).
    """


#%%
# Demonstrate JSON encoding/decoding of Band objects

# Using the json_tricks module from the json-tricks external package (https://github.com/mverleg/pyjson_tricks).
# From the package documentation:
# The JSON string resulting from applying the json_tricks.dumps() function stores the module and class name.
# The class must be importable from the same module when decoding (and should not have changed).
# If it isn't, you have to manually provide a dictionary to cls_lookup_map when loading
# in which the class name can be looked up. Note that if the class is imported, then globals() is such a dictionary
# (so try loads(json, cls_lookup_map=glboals())).
# Also note that if the class is defined in the 'top' script (that you're calling directly),
# then this isn't a module and the import part cannot be extracted. Only the class name will be stored;
# it can then only be deserialized in the same script, or if you provide cls_lookup_map.
# That's why the following warning appears when serializing Band objects in this script:
# UserWarning: class <class '__main__.Band'> seems to have been defined in the main file;
# unfortunately this means that it's module/import path is unknown,
# so you might have to provide cls_lookup_map when decoding.

# Single object
from json_tricks import loads, dumps
theBeatles = Band('The Beatles', *[johnLennon, paulMcCartney, georgeHarrison, ringoStarr],
                  start=date(1957, 7, 6), end=date(1970, 4, 10))
theBeatles_json = dumps(theBeatles, indent=4)
print(theBeatles == loads(theBeatles_json))

# List of objects

theBeatles = Band('The Beatles', *[johnLennon, paulMcCartney, georgeHarrison, ringoStarr],
                  start=date(1957, 7, 6), end=date(1970, 4, 10))
theRollingStones = Band('The Rolling Stones', *[mickJagger, keithRichards, ronWood, charlieWatts],
                        start=date(1962, 7, 12))
pinkFloyd = Band('Pink Floyd', *[sydBarrett, davidGilmour, rogerWaters, nickMason, rickWright])

bands = [theBeatles, theRollingStones, pinkFloyd]
bands_json = dumps(bands, indent=4)
print(bands == loads(bands_json))


#%%
class BandError(Exception):
    """Base class for exceptions in this module.
    """

    pass


#%%
class BandNameError(BandError):
    """Exception raised when the name of a band is specified incorrectly.
    """

    def __init__(self, name):
        Exception.__init__(self, f'BandNameError: \'{name}\' is not a valid band name')
        self.name = name


#%%
# Demonstrate exceptions

#%%
# Catching exceptions - try-except block
# If an exception is caught as e, then e.args[0] is the type of exception (relevant for exception handling).
# To write error messages to the exception console, use sys.stderr.write(f'...').

# print(', '.join([m.name for m in the_beatles.members]))
try:
    for i in range(5):
        print(the_beatles.members[i].name)
except Exception as e:
    # print(e)
    # print(e.args)
    # print(e.args[0])
    # sys.stderr.write(e.args[0])
    sys.stderr.write(f'\n{type(e).__name__}: {e.args[0]}\n\n')

#%%
# Catching multiple exceptions and the 'finally' clause
try:
    for i in range(5):
        print(the_beatles.members[i].name)
        # print(the_beatles / 4)
except IndexError as e:
    sys.stderr.write(f'\n{type(e).__name__}: {e.args[0]}\n\n')
except Exception as e:
    # print(e)
    # print(e.args)
    # print(e.args[0])
    # sys.stderr.write(e.args[0])
    sys.stderr.write(f'\n{type(e).__name__}: {e.args[0]}\n\n')
finally:
    print('Caught an exception. Stopped any further processing.')

#%%
# Using the 'else' clause (must be after all 'except' clauses)
try:
    for i in range(4):
        print(the_beatles.members[i].name)
        # print(the_beatles / 4)
except IndexError as e:
    sys.stderr.write(f'\n{type(e).__name__}: {e.args[0]}\n\n')
else:
    print('Done.')

#%%
# Catching 'any' exception - empty 'except' clause
try:
    for i in range(5):
        print(the_beatles.members[i].name)
        # print(the_beatles / 4)
except:
    sys.stderr.write('\nCaught an exception. Stopped any further processing.\n\n')

#%%
# Catching user-defined exceptions
try:
    b = Band('a', *[johnLennon, paulMcCartney, georgeHarrison, ringoStarr],
             start=date(1957, 7, 6), end=date(1970, 4, 11))
except BandNameError as e:
    # sys.stderr.write(f'\n{type(e).__name__}: {e.args[0]}')
    sys.stderr.write(f'\n{e.args[0]}\n\n')

#%%
# Demonstrate working with files

theBeatles = Band('The Beatles', *[johnLennon, paulMcCartney, georgeHarrison, ringoStarr],
                  start=date(1957, 7, 6), end=date(1970, 4, 10))
theRollingStones = Band('The Rolling Stones', *[mickJagger, keithRichards, ronWood, charlieWatts],
                        start=date(1962, 7, 12))
pinkFloyd = Band('Pink Floyd', *[sydBarrett, davidGilmour, rogerWaters, nickMason, rickWright])

#%%
# Writing to a text file - <outfile>.write(str(<obj>), <outfile>.writelines([str(<obj>)+'\n' for <obj> in <objs>])
bands = [theBeatles, theRollingStones, pinkFloyd]
file = get_project_dir() / 'data/bands.txt'
with open(file, 'w') as f:
    # for band in bands:
    #     f.write(str(band) + '\n')
    f.writelines([str(b) + '\n' for b in bands])
print('Done')

#%%
# Demonstrate reading from a text file - <infile>.readline(), <infile>.readlines()
bands = [theBeatles, theRollingStones, pinkFloyd]
file = get_project_dir() / 'data/bands.txt'
with open(file, 'r') as f:
    # lines = f.read().rstrip()
    # lines = f.read().splitlines()
    lines = ''
    while True:
        line = f.readline()
        if line:
            lines += line
        else:
            break
print(lines)

#%%
# Demonstrate writing to a binary file - pickle.dump(<obj>, <outfile>)
bands = [theBeatles, theRollingStones, pinkFloyd]
file = get_project_dir() / 'data/bands'
with open(file, 'wb') as f:
    pickle.dump(bands, f)
print('Done')

#%%
# Demonstrate reading from a binary file - pickle.load(<infile>)
bands = [theBeatles, theRollingStones, pinkFloyd]
file = get_project_dir() / 'data/bands'
with open(file, 'rb') as f:
    bands1 = pickle.load(f)
print('Done')
print(bands == bands1)


