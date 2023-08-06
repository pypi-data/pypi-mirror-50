from . import _bytedata as bytedata


def _group_tokens (tokens):
    """Group tokens from `serialisation.parse` into records.

Drops tokens that aren't in records.  Returns an iterator of iterators of
tokens.

"""
    restorable_tokens = bytedata.result.RestorableIterator(tokens)
    finished = False

    def iter_group ():
        current_path = None
        for token in restorable_tokens:
            path_base = token.path[:1]
            if path_base != current_path:
                # should be in the next group - put it back on the iterator
                if current_path is not None:
                    restorable_tokens.add(token)
                    return
                current_path = path_base
            # record index / 'record' / field index / field property
            if len(token.path) >= 4 and token.path[1] == 'record':
                yield token

        nonlocal finished
        finished = True

    while not finished:
        yield iter_group()


def _transform_record (record):
    """Transform a record from a list of fields to a dict.

Doesn't handle nested records.

"""
    if isinstance(record, list):
        # value can only be missing if it was an empty sequence of tokens,
        # which should have become a list, which we should transform into a dict
        return {field['name']: field.get('value', {}) for field in record}
    else:
        return record


def parse (tokens):
    """Group parsed epgdb file tokens into records.

:arg typing.Iterator tokens: Result of :func:`pyepgdb.serialisation.parse`

:return:
    Records as defined in the epgdb file.  Values are :class:`int`,
    :class:`str`, :class:`bytes` or nested records
:rtype: typing.Iterator[typing.Dict]

"""
    for record_tokens in _group_tokens(tokens):
        yield bytedata.result.build_record(record_tokens, _transform_record, 2)
