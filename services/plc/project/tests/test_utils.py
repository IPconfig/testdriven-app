from project.tests.base import BaseTestCase
from project.api.utils import (map_bytearray_with_layout, filter_tube_state,
                               map_memory_to_dbo, map_dbo_to_memory)

# create a 2x2 reactor
# [4] [5]
# [3] [2]
_data = bytearray([
    0, 2, 0, 2,                         # tubes per row:        [2, 2]
    0, 1, 0, 1, 0, 2, 0, 2,             # tube Row:             [1, 1]
    0, 1, 0, 2, 0, 1, 0, 2,             # tube_number_in_row:   [1, 2, 1, 2]
    0, 4, 0, 5, 0, 3, 0, 2,             # tube_state:           [4, 5, 3, 2]
    0, 4,                               # total_tubes:          4
    0, 0,                               # counter:              0
    128*0 + 64*0 + 32*0 + 16*0 +
    8*1 + 4*1 + 2*1 + 1*1,              # debounce:             1
    0, 2,                               # total_rows:           2
    0, 0,                               # coppycounter:         0
    0, 0,                               # overviewcoppied:      0
    ])

layout = """

0           tubes_per_row       FARRAY[2]       # number of tubes per row
4           tube_ROW            FARRAY[4]       # element position gives row#
12          tube_number_in_row  FARRAY[4]       # element position gives col#
20          tube_state          ARRAY[4]        # element position gives value
28          total_tubes         INT             # number of total tubes
30          counter             INT             # counter
32.0        debounce            BOOL
33          total_rows          INT             # number of total rows
35          coppycounter        INT
37          overviewcoppied     INT
"""


class TestUtils(BaseTestCase):

    def test_map_bytearray(self):
        db_number = 1
        size = 39
        _bytearray = _data
        memObj = map_bytearray_with_layout(self.client,
                                           db_number, layout, _bytearray, size)
        self.assertEqual(memObj['tubes_per_row'], [2, 2])
        self.assertEqual(memObj['tube_ROW'], [1, 1, 2, 2])
        self.assertEqual(memObj['tube_number_in_row'], [1, 2, 1, 2])
        self.assertEqual(memObj['tube_state'], [4, 5, 3, 2])
        self.assertEqual(memObj['total_tubes'], 4)
        self.assertEqual(memObj['counter'], 0)
        self.assertEqual(memObj['debounce'], True)
        self.assertEqual(memObj['total_rows'], 2)
        self.assertEqual(memObj['coppycounter'], 0)
        self.assertEqual(memObj['overviewcoppied'], 0)

    def test_map_x_to_y(self):
        '''
            test map_memory_to_dbo
            test map_dbo_to_memory
        '''
        db_number = 1
        size = 39
        _bytearray = _data
        memObj = map_bytearray_with_layout(self.client,
                                           db_number, layout, _bytearray, size)
        dbo = map_memory_to_dbo(memObj)
        self.assertEqual(dbo.tubes_per_row, memObj['tubes_per_row'])
        self.assertEqual(dbo.tube_ROW, memObj['tube_ROW'])
        self.assertEqual(dbo.tube_number_in_row, memObj['tube_number_in_row'])
        self.assertEqual(dbo.tube_state, memObj['tube_state'])
        self.assertEqual(dbo.total_tubes, memObj['total_tubes'])
        self.assertEqual(dbo.counter, memObj['counter'])
        self.assertEqual(dbo.debounce, memObj['debounce'])
        self.assertEqual(dbo.total_rows, memObj['total_rows'])
        self.assertEqual(dbo.coppycounter, memObj['coppycounter'])
        self.assertEqual(dbo.overviewcoppied, memObj['overviewcoppied'])

        memory = map_dbo_to_memory(dbo, memObj)
        self.assertEqual(dbo.tubes_per_row, memory['tubes_per_row'])
        self.assertEqual(dbo.tube_ROW, memory['tube_ROW'])
        self.assertEqual(dbo.tube_number_in_row, memory['tube_number_in_row'])
        self.assertEqual(dbo.tube_state, memory['tube_state'])
        self.assertEqual(dbo.total_tubes, memory['total_tubes'])
        self.assertEqual(dbo.counter, memory['counter'])
        self.assertEqual(dbo.debounce, memory['debounce'])
        self.assertEqual(dbo.total_rows, memory['total_rows'])
        self.assertEqual(dbo.coppycounter, memory['coppycounter'])
        self.assertEqual(dbo.overviewcoppied, memory['overviewcoppied'])

    def test_filter_tube_state(self):
        db_number = 1
        size = 39
        _bytearray = _data
        memObj = map_bytearray_with_layout(self.client,
                                           db_number, layout, _bytearray, size)
        res = filter_tube_state(memObj['tubes_per_row'], memObj["tube_state"])
        self.assertEqual(res, [[4, 5], [3, 2]])
