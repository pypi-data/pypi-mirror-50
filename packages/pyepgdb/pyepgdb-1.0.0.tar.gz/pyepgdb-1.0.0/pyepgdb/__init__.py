"""
Parse epgdb files.
"""

from . import serialisation, compression, structure, values


def parse (f, store=None):
    """Read all programmes from an epgdb file.

:arg typing.BinaryIO f: epgdb file contents
:arg typing.Dict store:
    Used to store temporary data.  Should be empty.  Default: in-memory store

:rtype: typing.Iterator[values.Programme]

"""
    uncompressed_f = compression.parse(f)
    tokens = serialisation.parse(uncompressed_f)
    records = structure.parse(tokens)
    return values.parse(records, store)
