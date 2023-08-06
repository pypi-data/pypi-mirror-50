from . import _bytedata as bytedata
from ._bytedata import define as d, parse as p

_p_uint = p.int_('big')
_p_str = p.str_('utf8')

# a single name-value pair in a record
_defn_field = sum([
    d.named('type', d.parse(1, _p_uint)),
    d.named('name size', d.parse(1, _p_uint)),
    d.named('value size', d.parse(4, _p_uint)),
    d.named('name', d.parse(('name size',), _p_str)),
])

# the value part of a field; can be a nested record
_defns_value = {
    1: d.repeat_size(('value size',), _defn_field),
    2: d.parse(('value size',), p.int_('little')),
    3: d.parse(('value size',), _p_str),
    5: d.parse(('value size',), p.binary),
}

# field and value definitions are mutually recursive, so we must modify one to
# refer to the other
_defn_field += d.dispatch(('type',), {
    type_: d.named('value', defn)
    for type_, defn in _defns_value.items()
})

# the file is sectioned, with each section containing arbitrary records
_defn_file = d.repeat_until_eof(sum([
    d.named('size', d.parse(4, _p_uint)),
    d.named('record', d.repeat_size(('size',), _defn_field)),
]))


def parse (f):
    """Deserialise the data from an uncompressed epgdb file,

:arg typing.BinaryIO f:
    Uncompressed epgdb file contents (see :mod:`pyepgdb.compression`)

:return:
    Iterator over tokens stored in the file, defining a hierarchy of collections
    using sequences of keys/indices.  Intended for consumption by
    :mod:`pyepgdb.structure`

"""
    return _defn_file.read(bytedata.StreamReader(f))
