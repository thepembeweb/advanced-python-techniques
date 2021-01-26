"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.
"""
from helpers import cd_to_datetime, datetime_to_str
from json import JSONEncoder
import datetime

class NearEarthObject(JSONEncoder):
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # Assignment of information from the arguments passed to the constructor
        self.designation = info.get('pdes', None)
        self.name = info.get('name') if info.get('name', None) and self.is_blank(info.get('name')) else None
        self.diameter = float(info.get('diameter')) if info.get('diameter', None) and self.is_blank(
            info.get('diameter')) else float('nan')
        self.hazardous = True if info.get('pha', None) and info.get('pha') in ('Y', 'y') else False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    def is_blank(self, object):
        return bool(object and object.strip())

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f'{self.designation} ({self.name})' if self.name else f'{self.designation}'

    def __str__(self):
        """Return `str(self)`."""
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and " \
               f"is {'' if self.hazardous else 'not '} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f'NearEarthObject(designation={self.designation!r}, name={self.name!r}, ' \
               f'diameter={self.diameter:.3f}, hazardous={self.hazardous!r})'

    def serialize(self):
        """Return serialized attributes for writing to file."""
        return {
            'designation': self.designation,
            'name': self.name if (self.name and self.is_blank(self.name)) else '',
            'diameter_km': self.diameter,
            'potentially_hazardous': self.hazardous,
        }


class CloseApproach(JSONEncoder):
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = info.get('des', '')
        self.distance = float(info.get('dist', 0.0))
        self.time = cd_to_datetime(info.get('cd')) if info.get('cd', None) else None
        self.velocity = float(info.get('v_rel', 0.0))

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f"On {self.time_str}, '{self.neo.fullname}' approaches Earth at a distance " \
               f"of {self.distance:.2f}au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def serialize(self):
        """Return serialized attributes for writing to file."""
        return {
            'datetime_utc': self.time_str,
            'distance_au': self.distance or float('nan'),
            'velocity_km_s': self.velocity or float('nan'),
        }

