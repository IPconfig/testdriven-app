# purely used to test in shell. delete when everything works

from project.api.util_db import DB, set_array
from project.api.utils import read_plc_memory, map_memory_to_db, plc_db_to_json, layout
from project.api.models import PLCDBSchema, PLCDBSchema2, Plc_db
import snap7.client
import project.api.util_db as util

client = snap7.client.Client()
client.connect('192.168.0.1', 0, 0)

memObj = read_plc_memory(client)

dbo = map_memory_to_db(memObj, client)
memObj["tubes_per_row"] = dbo.tubes_per_row

memory_bytearray = client.db_read(7, 0, 62014)

temp_bytearray = memory_bytearray

def print_this(key, index, _type):
    import re
    import struct
    print("My index is {0} and my type is {1}".format(index, _type))
    if _type == 'BOOL':
        print("I'm a Boolean")
    if _type.startswith('STRING'):
        max_size = re.search('\d+', _type).group(0)
        max_size = int(max_size)
        print("{1} I'm a String, my size is {0}".format(max_size, key))
    if _type.startswith('ARRAY'):
        max_size = re.search('\d+', _type).group(0)
        max_size = int(max_size)
        print("{1} I'm an ARRAY, my size is {0}".format(max_size, key))
test = dbo.tubes_per_row  # [10,10,10,10,10....]
_no = len(test)
max_size = 10
b = bytearray()
zero = bytearray()
merged = bytearray()
# convert list of values to bytes
b = b.join((struct.pack('>h', val) for val in test))
# generate zeroes to fill the empty space in the array
zero = zero.join((struct.pack('>h', 0) for val in range(_no, max_size, 1)))
# create a new byte array consisting of values + zeroes
merged = merged.join([b, zero])
_bytearray = []
_bytearray[index:index + 2] = struct.unpack('2B' * max_size, bytes(merged))
        fmerged = set_array(_bytearray=None, byte_index=None, value=test, max_size=max_size)
        if merged == fmerged:
            print('merged and fmerged are the same')
    if _type.startswith('FARRAY'):
        max_size = re.search('\d+', _type).group(0)
        max_size = int(max_size)
        print("Key:{1} I'm a FARRAY, my size is {0}".format(max_size, key))
    if _type == 'REAL':
        print("I'm a Real")
    if _type == 'DWORD':
        print("I'm a DWORD")
    if _type == 'INT':
        print("I'm a Integer")




def print_this_clean(key, index, _type):
    import re
    import struct
    print("My index is {0} and my type is {1}".format(index, _type))
    if _type == 'BOOL':
        print("I'm a Boolean")
    if _type.startswith('STRING'):
        max_size = re.search('\d+', _type).group(0)
        max_size = int(max_size)
        print("{1} I'm a String, my size is {0}".format(max_size, key))
    if _type.startswith('ARRAY'):
        max_size = re.search('\d+', _type).group(0)
        max_size = int(max_size)
        print("{1} I'm an ARRAY, my size is {0}".format(max_size, key))
        test = dbo.tubes_per_row  # [10,10,10,10,10....]
        result = set_array(_bytearray=None, byte_index=None, value=test, max_size=max_size)
    if _type.startswith('FARRAY'):
        max_size = re.search('\d+', _type).group(0)
        max_size = int(max_size)
        print("Key:{1} I'm a FARRAY, my size is {0}".format(max_size, key))
    if _type == 'REAL':
        print("I'm a Real")
    if _type == 'DWORD':
        print("I'm a DWORD")
    if _type == 'INT':
        print("I'm a Integer")
    return result

def do_something_with_layout(layout):
from project.api.util_db import parse_specification
spec = parse_specification(layout)
data = {}
bytearr = bytearray()
for key in spec:
    data[key] = spec[key]
    index, _type = data[key]
    result = print_this_clean(key, index, _type)  # returns a bytearray based on the type
    bytear.extend(result)  #  add data to the bytearray




# Convert object back to bytearray so we can upload this to the plc
dbo = Plc_db.query.filter_by(plc_id=1).first()
bla = get_memory_object()
# set memory object to values from db
bla["tubes_per_row"] = dbo.tubes_per_row


initial_write = DB(
        tubes_per_row=db["tubes_per_row"],
        tube_ROW=db["tube_ROW"],
        tube_number_in_row=db["tube_number_in_row"],
        tube_state=db["tube_state"],
        tube_state_client=tube_state_client,
        total_tubes=db["total_tubes"],
        counter=db["counter"],
        debounce=db["debounce"],
        total_rows=db["total_rows"],
        coppycounter=db["coppycounter"],
        overviewcoppied=db["overviewcoppied"]
)

test = dbo.tubes_per_row

for elem in test:
    _data = elem.to_bytes(2, byteorder='little')
msg = bytearray(final_read.tubes_per_row)
row = util.DB_Row(msg, layout)
row['tubes_per_row']
