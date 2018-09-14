"""
This module contains utility functions for working with PLC DB objects.
There are functions to work with the raw bytearray data snap7 functions return
In order to work with this data you need to make python able to work with the
PLC bytearray data.

I added the set and get for arrays myself
"""

# TODO: set ARRAY and FARRAY values

# flake8: noqa
try:
    # try with the standard library
    from collections import OrderedDict
except ImportError:
    # fallback to Python 2.6-2.4 back-port
    from ordereddict import OrderedDict


import struct
import logging
from snap7 import six
import re

logger = logging.getLogger(__name__)


def get_bool(_bytearray, byte_index, bool_index):
    """
    Get the boolean value from location in bytearray
    """
    index_value = 1 << bool_index
    byte_value = _bytearray[byte_index]
    current_value = byte_value & index_value
    return current_value == index_value


def set_bool(_bytearray, byte_index, bool_index, value):
    """
    Set boolean value on location in bytearray
    """
    assert value in [0, 1, True, False]
    current_value = get_bool(_bytearray, byte_index, bool_index)
    index_value = 1 << bool_index

    # check if bool already has correct value
    if current_value == value:
        return

    if value:
        # make sure index_v is IN current byte
        _bytearray[byte_index] += index_value
    else:
        # make sure index_v is NOT in current byte
        _bytearray[byte_index] -= index_value


def set_int(bytearray_, byte_index, _int):
    """
    Set value in bytearray to int
    """
    # make sure were dealing with an int
    _int = int(_int)
    _bytes = struct.unpack('2B', struct.pack('>h', _int))
    # print("bytes is: {0}".format(_bytes))
    bytearray_[byte_index:byte_index + 2] = _bytes
    return bytearray_


def get_int(bytearray_, byte_index):
    """
    Get int value from bytearray.

    int are represented in two bytes
    """
    data = bytearray_[byte_index:byte_index + 2]
    data[1] = data[1] & 0xff
    data[0] = data[0] & 0xff
    packed = struct.pack('2B', *data)
    value = struct.unpack('>h', packed)[0]
    # print('packed: {0}'.format, packed)
    # print("value that gets returned: {0}".format, value)
    return value


def set_array(_bytearray, byte_index, value, max_size):
    """
    parse array of integers from bytearray
    int are represented in two bytes

    :params value: array data
    :params max_size: max possible array size
    """

    size = len(value) * 2
    if max_size < size:
        logger.error("Array is too big for the size given in specification")
        logger.error("WRONG SIZED ARRAY ENCOUNTERED")
        size = max_size
    _no = len(value)

    data = bytearray()
    zero = bytearray()
    result = bytearray()
    # convert list of values to bytes
    data = data.join((struct.pack('>h', val) for val in value))
    # generate zeroes to fill the empty space in the array
    zero = zero.join((struct.pack('>h', 0) for val in range(_no, max_size, 1)))
    # create a new byte array consisting of values + zeroes
    result = result.join([data, zero])
    _bytes = struct.unpack('2B' * max_size, bytes(result))
    for i, b in enumerate(_bytes):
        _bytearray[byte_index + i] = b


def get_array(_bytearray, byte_index, max_size):
    """
    parse array of integers from bytearray
    int are represented in two bytes
    """
    size = _bytearray[byte_index + 2]
    if max_size < size:
        logger.error("Array is too big for the size given in specification")
        logger.error("WRONG SIZED ARRAY ENCOUNTERED")
        size = max_size

    data = []
    # _data = [get_int(
    #                 _bytearray, i)
    #                             for i in range(0, max_size * 2, 2)]
    _data = [int.from_bytes(
            _bytearray[i:i + 2], byteorder='big')
                                for i in range(0, max_size * 2, 2)]
    data.extend(_data)
    return data


def get_array_filter(_bytearray, byte_index, max_size):
    """
    parse array of integers from bytearray
    int are represented in two bytes
    """
    size = _bytearray[byte_index + 2]


    if max_size < size:
        logger.error("Array is too big for the size given in specification")
        logger.error("WRONG SIZED ARRAY ENCOUNTERED")
        size = max_size

    data = []
    _data = [get_int(_bytearray, i)
                        for i in range(0, max_size * 2, 2)
                        if get_int(_bytearray, i) != 0]
    data.extend(_data)
    return data


def set_real(_bytearray, byte_index, real):
    """
    Set Real value

    make 4 byte data from real

    """
    real = float(real)
    real = struct.pack('>f', real)
    _bytes = struct.unpack('4B', real)
    for i, b in enumerate(_bytes):
        _bytearray[byte_index + i] = b


def get_real(_bytearray, byte_index):
    """
    Get real value. create float from 4 bytes
    """
    x = _bytearray[byte_index:byte_index + 4]
    real = struct.unpack('>f', struct.pack('4B', *x))[0]
    return real


def set_string(_bytearray, byte_index, value, max_size):
    """
    Set string value

    :params value: string data
    :params max_size: max possible string size
    """
    if six.PY2:
        assert isinstance(value, (str, unicode))
    else:
        assert isinstance(value, str)

    size = len(value)
    # FAIL HARD WHEN trying to write too much data into PLC
    if size > max_size:
        raise ValueError('size %s > max_size %s %s' % (size, max_size, value))
    # set len count on first position
    _bytearray[byte_index + 1] = len(value)

    i = 0
    # fill array which chr integers
    for i, c in enumerate(value):
        _bytearray[byte_index + 2 + i] = ord(c)

    # fill the rest with empty space
    for r in range(i + 1, _bytearray[byte_index]):
        _bytearray[byte_index + 2 + r] = ord(' ')


def get_string(_bytearray, byte_index, max_size):
    """
    parse string from bytearray
    """
    size = _bytearray[byte_index + 1]

    if max_size < size:
        logger.error("the string is to big for the size encountered in specification")
        logger.error("WRONG SIZED STRING ENCOUNTERED")
        size = max_size

    data = map(chr, _bytearray[byte_index + 2:byte_index + 2 + size])
    return "".join(data)


def get_dword(_bytearray, byte_index):
    data = _bytearray[byte_index:byte_index + 4]
    dword = struct.unpack('>I', struct.pack('4B', *data))[0]
    return dword


def set_dword(_bytearray, byte_index, dword):
    dword = int(dword)
    _bytes = struct.unpack('4B', struct.pack('>I', dword))
    for i, b in enumerate(_bytes):
        _bytearray[byte_index + i] = b


def parse_specification(db_specification):
    """
    Create a db specification derived from a
    dataview of a db in which the byte layout
    is specified
    """
    parsed_db_specification = OrderedDict()

    for line in db_specification.split('\n'):
        if line and not line.startswith('#'):
            row = line.split('#')[0]  # remove trailing comment
            index, var_name, _type = row.split()
            parsed_db_specification[var_name] = (index, _type)

    return parsed_db_specification


class DB(object):
    """
    Manage a DB bytearray block given a specification
    of the Layout.

    It is possible to have many repetitive instances of
    a specification this is called a "row".

    probably most usecases there is just one row

    db1[0]['testbool1'] = test
    db1.write()   # puts data in plc
    """
    _bytearray = None      # data from plc
    specification = None   # layout of db rows
    row_size = None        # bytes size of a db row
    layout_offset = None   # at which byte in row specification should
                           # we start reading the data
    db_offset = None       # at which byte in db should we start reading?
                           # first fields could be be status data.
                           # and only the last part could be control data
                           # now you can be sure you will never overwrite
                           # critical parts of db

    def __init__(self, db_number, _bytearray,
                 specification, row_size, size, id_field=None,
                 db_offset=0, layout_offset=0, row_offset=0):

        self.db_number = db_number
        self.size = size
        self.row_size = row_size
        self.id_field = id_field

        self.db_offset = db_offset
        self.layout_offset = layout_offset
        self.row_offset = row_offset

        self._bytearray = _bytearray
        self.specification = specification
        # loop over bytearray. make rowObjects
        # store index of id_field to row objects
        self.index = OrderedDict()
        self.make_rows()

    def make_rows(self):
        id_field = self.id_field
        row_size = self.row_size
        specification = self.specification
        layout_offset = self.layout_offset

        for i in range(self.size):
            # calculate where row in bytearray starts
            db_offset = i * row_size + self.db_offset
            # create a row object
            row = DB_Row(self,
                         specification,
                         row_size=row_size,
                         db_offset=db_offset,
                         layout_offset=layout_offset,
                         row_offset=self.row_offset)

            # store row object
            key = row[id_field] if id_field else i
            if key and key in self.index:
                msg = '%s not unique!' % key
                logger.error(msg)
            self.index[key] = row

    def __getitem__(self, key, default=None):
        return self.index.get(key, default)

    def __iter__(self):
        for key, row in self.index.items():
            yield key, row

    def __len__(self):
        return len(self.index)

    def set_data(self, _bytearray):
        assert(isinstance(_bytearray, bytearray))
        self._bytearray = _bytearray


class DB_Row(object):
    """
    Provide ROW API for DB bytearray
    """
    _bytearray = None      # data of reference to parent DB
    _specification = None  # row specification

    def __init__(self, _bytearray, _specification, row_size=0,
                 db_offset=0, layout_offset=0, row_offset=0):

        self.db_offset = db_offset          # start point of row data in db
        self.layout_offset = layout_offset  # start point of row data in layout
        self.row_size = row_size
        self.row_offset = row_offset        # start of writable part of row

        assert(isinstance(_bytearray, (bytearray, DB)))
        self._bytearray = _bytearray
        self._specification = parse_specification(_specification)

    def get_bytearray(self):
        """
        return bytearray from self or DB parent
        """
        if isinstance(self._bytearray, DB):
            return self._bytearray._bytearray
        return self._bytearray

    def export(self):
        """
        export dictionary with values
        """
        data = {}
        for key in self._specification:
            data[key] = self[key]
        return data

    def __getitem__(self, key):
        """
        Get a specific db field
        """
        assert key in self._specification
        index, _type = self._specification[key]
        return self.get_value(index, _type)

    def __setitem__(self, key, value):
        assert key in self._specification
        index, _type = self._specification[key]
        self.set_value(index, _type, value)

    def __repr__(self):

        string = ""
        for var_name, (index, _type) in self._specification.items():
            string = '%s\n%-20s %-10s' % (string, var_name,
                                          self.get_value(index, _type))
        return string

    def unchanged(self, _bytearray):
        if self.get_bytearray() == _bytearray:
            return True
        return False

    def get_offset(self, byte_index):
        """
        Calculate correct beginning position for a row
        the db_offset = row_size * index
        """
        return int(byte_index) - self.layout_offset + self.db_offset

    def get_value(self, byte_index, _type):
        _bytearray = self.get_bytearray()

        if _type == 'BOOL':
            byte_index, bool_index = byte_index.split('.')
            return get_bool(_bytearray, self.get_offset(byte_index),
                            int(bool_index))

        # remove 4 from byte index since
        # first 4 bytes are used by db
        byte_index = self.get_offset(byte_index)

        if _type.startswith('STRING'):
            max_size = re.search('\d+', _type).group(0)
            max_size = int(max_size)
            return get_string(_bytearray, byte_index, max_size)

        if _type.startswith('ARRAY'):
            max_size = re.search('\d+', _type).group(0)
            max_size = int(max_size)
            return get_array(_bytearray, byte_index, max_size)

        if _type.startswith('FARRAY'):
            max_size = re.search('\d+', _type).group(0)
            max_size = int(max_size)
            return get_array_filter(_bytearray, byte_index, max_size)

        if _type == 'REAL':
            return get_real(_bytearray, byte_index)

        if _type == 'DWORD':
            return get_dword(_bytearray, byte_index)

        if _type == 'INT':
            return get_int(_bytearray, byte_index)

        raise ValueError

    def set_value(self, byte_index, _type, value):
        _bytearray = self.get_bytearray()

        if _type == 'BOOL':
            byte_index, bool_index = byte_index.split('.')
            return set_bool(_bytearray, self.get_offset(byte_index),
                            int(bool_index), value)

        byte_index = self.get_offset(byte_index)

        if _type.startswith('STRING'):
            max_size = re.search('\d+', _type).group(0)
            max_size = int(max_size)
            return set_string(_bytearray, byte_index, value, max_size)

        if _type.startswith('ARRAY'):
            max_size = re.search('\d+', _type).group(0)
            max_size = int(max_size)
            return set_array(_bytearray, byte_index, value, max_size)

        if _type.startswith('FARRAY'):
            max_size = re.search('\d+', _type).group(0)
            max_size = int(max_size)
            return set_array(_bytearray, byte_index, value, max_size)

        if _type == 'REAL':
            return set_real(_bytearray, byte_index, value)

        if _type == 'DWORD':
            return set_dword(_bytearray, byte_index, value)

        if _type == 'INT':
            return set_int(_bytearray, byte_index, value)

        raise ValueError

    def write(self, client):
        """
        Write current data to db in plc
        """
        assert(isinstance(self._bytearray, DB))
        assert(self.row_size >= 0)

        db_nr = self._bytearray.db_number
        offset = self.db_offset
        data = self.get_bytearray()[offset:offset+self.row_size]
        db_offset = self.db_offset

        # indicate start of write only area of row!
        if self.row_offset:
            data = data[self.row_offset:]
            db_offset += self.row_offset

        client.db_write(db_nr, db_offset, data)

    def read(self, client):
        """
        read current data of db row from plc
        """
        assert(isinstance(self._bytearray, DB))
        assert(self.row_size >= 0)
        db_nr = self._bytearray.db_number
        _bytearray = client.db_read(db_nr, self.db_offset, self.row_size)

        data = self.get_bytearray()
        # replace data in bytearray
        for i, b in enumerate(_bytearray):
            data[i + self.db_offset] = b