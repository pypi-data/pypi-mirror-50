import itertools


def validate (type_, allow_none=False, default=None):
    """Create a validator for a field in an epgdb record.

type_: Class to expect the value to be an instance of
allow_none: Whether the value should pass validation if it's `None`
default: Value to use if `None` is allowed and the value is `None`

Returns a function which accepts the value and returns the value to use or
throws `ValueError`.

"""
    def validate_fn (value):
        if value is None:
            if allow_none:
                return default
            else:
                raise ValueError('field is missing')
        if not isinstance(value, type_):
            raise ValueError('expected: {}; got: {}'.format(type_, repr(value)))
        return value

    return validate_fn


def validate_map (validate_fn, allow_none=False, default=None):
    """Create a validator for a 'map'-type field in an epgdb record.

Verifies that the value is a dict with string keys.

validate_fn:
    Function used to validate all individual values in the map (like the
    function returned by `validate`)
allow_none: whether the map value should pass validation if it's `None`
default: map value to use if `None` is allowed and the map value is `None`

Returns a function which accepts the map value and returns the map value to use
or throws `ValueError`.

"""
    validate_outer = validate(dict, allow_none, default)

    def validate_map_fn (value):
        valid_value = validate_outer(value)
        deep_valid_value = {}
        for key, inner_value in valid_value.items():
            try:
                deep_valid_value[key] = validate_fn(inner_value)
            except ValueError as e:
                raise ValueError({'key': key}, *e.args)
        return deep_valid_value

    return validate_map_fn


def read_value (fields, name, validate_fn):
    """Retrieve a value from an epgdb record and validate it.

fields: The record dict
name: The field name
validate_fn:
    Function used to validate the value (like the function returned by
    `validate`)

Returns the value to use or throws `ValueError`.

"""
    value = fields.get(name)
    try:
        return validate_fn(value)
    except ValueError as e:
        raise ValueError('found item with unexpected value',
                         {'field': name, 'fields': fields},
                         *e.args)


def localise (lang, strings):
    """Choose a language variant for an epgdb string value.

Some strings stored in epgdb records have values for multiple languages.  This
function extracts the value for the preferred language, or any value, or an
empty string.

lang: ID string for the preferred language
strings:
    The field value; should be a map-type field with string values (see
    `validate_map`)

"""
    return strings.get(lang, next(itertools.chain(strings.values(), ('',))))

