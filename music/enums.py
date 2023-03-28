"""
The enums used in this project. They define different kinds of instruments and vocals.
"""

from enum import Enum


class Instrument(Enum):

    LEAD_GUITAR = 'lead guitar'
    RHYTHM_GUITAR = 'rhythm guitar'
    BASS = 'bass'
    DRUMS = 'drums'
    KEYBOARD = 'keyboards'
    VOCALS = 'vocals'


class Vocals(Enum):

    LEAD_VOCALS = 'lead vocals'
    BACKGROUND_VOCALS = 'background vocals'
