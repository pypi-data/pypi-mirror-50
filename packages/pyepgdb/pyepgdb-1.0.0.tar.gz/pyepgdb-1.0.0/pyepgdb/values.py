from .network import _util as networkutil

# temporary store key prefixes
_EPISODE_KEY = 'e:'
_BROADCAST_KEY = 'b:'
# epgdb file section names
_EPISODES_SECTION = 'episodes'
_BROADCASTS_SECTION = 'broadcasts'


class _Episode:
    """A produced episode or film, not associated with how it's broadcast.

fields: epgdb record

"""

    def __init__ (self, fields):
        # unique identifier
        self.id_ = networkutil.read_value(
            fields, 'uri', networkutil.validate(str))
        self.fields = fields


class _Broadcast:
    """A specific broadcast of an episode.

fields: epgdb record

"""

    def __init__ (self, fields):
        # links up with _Episode.id
        self.episode_id = networkutil.read_value(
            fields, 'episode', networkutil.validate(str))
        self.fields = fields


class Programme:
    """A produced episode or film, associated with a specific broadcast of it.

:arg typing.Dict episode:
    Record from the epgdb file describing the actual content of the episode or
    film.
:arg typing.Dict broadcast:
    Record from the epgdb file describing a specific broadcast of the episode or
    film.

"""

    def __init__ (self, episode, broadcast):
        self.episode = episode
        """Record for the actual episode content."""

        self.broadcast = broadcast
        """Record for the specific episode broadcast."""


def parse (items, store=None):
    """Restructure parsed epgdb records into programme objects.

:arg typing.Iterator records: Result of :func:`pyepgdb.structure.parse`
:arg typing.Dict store:
    Used to store temporary data.  Should be empty.  Default: in-memory store

:rtype: typing.Iterator[values.Programme]

"""
    if store is None:
        store = {}
    section = None

    for item in items:
        if not isinstance(item, dict):
            pass
        elif '__section__' in item:
            section = item['__section__']
            pass
        elif section == _EPISODES_SECTION:
            episode = _Episode(item)
            # always need to store an episode, since there might be another
            # broadcast for it
            store[_EPISODE_KEY + episode.id_] = episode
        elif section == _BROADCASTS_SECTION:
            broadcast = _Broadcast(item)
            episode = store.get(_EPISODE_KEY + broadcast.episode_id)
            # only need to store a broadcast if we don't have the episode yet
            if episode is None:
                store[_BROADCAST_KEY] = broadcast
            else:
                yield Programme(episode.fields, broadcast.fields)

    # handle broadcasts we found before their episodes
    for store_key, broadcast in store.items():
        if store_key.startswith(_BROADCAST_KEY):
            episode = store[_EPISODE_KEY + broadcast.episode_id]
            yield Programme(episode.fields, broadcast.fields)
