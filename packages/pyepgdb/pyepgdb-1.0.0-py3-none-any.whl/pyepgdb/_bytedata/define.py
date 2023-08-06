from . import result, util


class _Part:
    def __init__ (self, read, save=set()):
        self.read = read
        self.save = set(save)


class Definition:
    def __init__ (self, parts):
        self._parts = tuple(parts)

    def __len__ (self):
        return len(self._parts)

    def __iter__ (self):
        return iter(self._parts)

    def __getitem__ (self, i):
        return self._parts[i]

    def __add__ (self, other):
        if other == 0 or (hasattr(other, '__len__') and len(other) == 0):
            return self
        elif not isinstance(other, Definition):
            raise TypeError('cannot add Definition to {}'.format(other))
        else:
            return Definition(self._parts + other._parts)

    def __radd__ (self, other):
        if other == 0 or (hasattr(other, '__len__') and len(other) == 0):
            return self
        else:
            raise TypeError('cannot add Definition to {}'.format(other))

    def __iadd__ (self, other):
        self._parts = (self + other)._parts
        return self

    @property
    def save (self):
        return set().union(*(p.save for p in self))

    def read (self, sr, saved_outer=None):
        saved = {} if saved_outer is None else saved_outer

        for part in self:
            try:
                for token in part.read(saved, sr):
                    if isinstance(token, result.Token):
                        if token.path in self.save:
                            saved[token.path] = token.value
                        yield token
            except util.WrappedError:
                raise
            except Exception as e:
                raise util.wrap_exc(sr, sr.pos, e)


empty = Definition(())


def _define (save=set()):
    return lambda read: Definition((_Part(read, save),))


def named (name, defn):
    @_define(defn.save)
    def read (saved, sr):
        for part in defn:
            for token in part.read(saved, sr):
                yield token.with_name(name)
    return read


def _const (val_fn, save=set()):
    @_define(save)
    def read (saved, sr):
        val = val_fn(saved)
        got = sr.read_exactly(len(val))
        if got != val:
            raise util._FormatError(
                'expected to read {}, found {}'.format(val, got))
        return iter(())
    return read


def const (val_def):
    if isinstance(val_def, bytes):
        return _const(lambda saved: val_def)
    else:
        return _const(lambda saved: saved[val_def], {val_def})


def const_null (length_def):
    if isinstance(length_def, int):
        val = b'\x00' * length_def
        return _const(lambda saved: val)
    else:
        return _const(lambda saved: b'\x00' * saved[length_def], {length_def})


def parse (length_def, parser):
    is_name = not isinstance(length_def, int)

    @_define({length_def} if is_name else set())
    def read (saved, sr):
        length = saved[length_def] if is_name else length_def
        yield result._UnnamedToken(parser(sr.read_exactly(length)))

    return read


def skip (length_def, check=False):
    is_name = not isinstance(length_def, int)

    @_define({length_def} if is_name else set())
    def read (saved, sr):
        length = saved[length_def] if is_name else length_def
        if check:
            sr.read_exactly(length)
        else:
            sr.skip(length)
        return iter(())

    return read


def _repeat(get_iter, defn, save=set(), ignore_eof=False):
    @_define(save)
    def read (saved, sr):
        for i, _ in enumerate(get_iter(saved, sr)):
            try:
                for token in defn.read(sr):
                    yield token.wrap_name(result.TokenPathIndex(i))
            except util.WrappedError as e:
                if isinstance(e.exc, EOFError) and ignore_eof:
                    break
                else:
                    raise
    return read


def repeat (length_def, defn):
    if isinstance(length_def, int):
        get_iter = lambda saved, sr: range(length_def)
        save = set()
    else:
        get_iter = lambda saved, sr: range(saved[length_def])
        save = {length_def}
    return _repeat(get_iter, defn, save=save)


def repeat_size (size_def, defn):
    is_name = not isinstance(size_def, int)

    def get_iter (saved, sr):
        initial_pos = None
        while True:
            pos = sr.pos
            size = saved[size_def] if is_name else size_def
            if initial_pos is None:
                initial_pos = pos
            if pos < initial_pos + size:
                yield None
            elif pos == initial_pos + size:
                break
            else:
                raise util._FormatError(
                    'expected a repeat to end after exactly {} bytes; ' \
                    'ended after {}'.format(size, pos - initial_pos))

    return _repeat(get_iter, defn, save={size_def} if is_name else set())


def repeat_until_eof (defn):
    def get_iter (saved, sr):
        while True:
            yield None

    return _repeat(get_iter, defn, ignore_eof=True)


def dispatch (key_name, defns):
    @_define({key_name} | set.union(*(defn.save for defn in defns.values())))
    def read (saved, sr):
        return defns[saved[key_name]].read(sr, saved)

    return read
