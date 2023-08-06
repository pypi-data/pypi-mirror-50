import struct
import sys


def _until_null (data):
    return data.split(b'\x00')[0]


identity = lambda data: data


def int_ (endian=None, signed=False):
    endian_spec = {None: '@', 'little': '<', 'big': '>'}[endian]
    off_size_endian_spec = sys.byteorder if endian is None else endian
    size_specs = {
        1: {False: 'B', True: 'b'},
        2: {False: 'H', True: 'h'},
        4: {False: 'I', True: 'i'},
        8: {False: 'Q', True: 'q'},
    }

    def parse (data):
        if len(data) in size_specs:
            size_spec = size_specs[len(data)][signed]
            return struct.unpack(endian_spec + size_spec, data)[0]
        else:
            return int.from_bytes(data, byteorder=off_size_endian_spec)

    return parse


def str_ (enc):
    def parse (data):
        return data.decode(enc)
    return parse


def null_str (enc):
    def parse (data):
        return str_(enc)(_until_null(data))
    return parse


def binary (data):
    return data
