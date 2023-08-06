from . import util as _util, define, parse, result
from .util import FormatError


class StreamReader:
    def __init__ (self, f, name=None):
        self._f = f
        self.name = f.name if name is None else name
        self.pos = 0

    def read (self, n):
        data = self._f.read(n)
        self.pos += len(data)
        return data

    def read_exactly (self, n):
        data = self.read(n)
        if len(data) != n:
            raise EOFError(
                'expected to read {} bytes; only found {}'.format(n, len(data)))
        return data

    def skip (self, n):
        self._f.read(n)
        self.pos += n
