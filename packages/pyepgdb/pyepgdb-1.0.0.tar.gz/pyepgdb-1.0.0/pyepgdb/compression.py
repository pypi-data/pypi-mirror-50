import gzip


def parse (f):
    """Decompress an epgdb file.

:arg typing.BinaryIO f: epgdb file contents

:return: Uncompressed epgdb file contents
:rtype: typing.BinaryIO

"""
    # skip epgdb-specific header
    f.read(12)
    return gzip.GzipFile(fileobj=f)
