import collections


class TokenPathIndex:
    def __init__ (self, index):
        self.index = index

    def __str__ (self):
        return str(self.index)

    def __repr__ (self):
        return '<TokenPathIndex({})>'.format(self.index)

    def __eq__ (self, other):
        return isinstance(other, TokenPathIndex) and other.index == self.index

    def __hash__ (self):
        return hash(self.index)


class _Token:
    def __init__ (self, path, value):
        self.path = path
        self.value = value

    def __str__ (self):
        path = '/'.join(str(part) for part in self.path)
        return '{}({}: {})'.format(
            type(self).__name__, repr(path), repr(self.value))

    __repr__ = __str__

    def with_name (self, name):
        return Token((name,) + self.path, self.value)

    def wrap_name (self, name):
        return self.with_name(name) if self.path else self


class _UnnamedToken (_Token):
    def __init__ (self, value):
        _Token.__init__(self, (), value)


class Token (_Token):
    def __init__ (self, path, value):
        _Token.__init__(self, path, value)


class RestorableIterator:
    def __init__ (self, source):
        self._source = source
        self._extras = collections.deque()

    def __iter__ (self):
        return self

    def __next__ (self):
        if self._extras:
            return self._extras.pop()
        else:
            return next(self._source)

    def add (self, item):
        self._extras.append(item)


def _build_record (tokens, transform, depth):
    record = None
    base_path = None

    for token in tokens:
        this_base_path = token.path[:depth]
        if (len(token.path) <= depth or
            (base_path is not None and this_base_path != base_path)
        ):
            tokens.add(token)
            break
        base_path = this_base_path

        if isinstance(token.path[depth], TokenPathIndex):
            if record is None:
                record = []
            if len(token.path) == depth + 1:
                record.append(token.value)
            else:
                tokens.add(token)
                record.append(_build_record(tokens, transform, depth + 1))
        else:
            if record is None:
                record = {}
            if len(token.path) == depth + 1:
                record[token.path[depth]] = token.value
            else:
                tokens.add(token)
                record[token.path[depth]] = (
                    _build_record(tokens, transform, depth + 1))

    return transform(record)


def build_record (tokens, transform=lambda record: record, depth=0):
    return _build_record(RestorableIterator(tokens), transform, depth)
