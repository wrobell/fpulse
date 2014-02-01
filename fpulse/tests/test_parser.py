#
# FPulse - LED pulsing application.
#
# Copyright (C) 2014 by Artur Wroblewski <wrobell@pld-linux.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
FPulse parser tests.
"""

from fpulse.parser import str2time, clean_file, parse_file

import unittest

class TimeParserTestCase(unittest.TestCase):
    """
    Time parsing tests.
    """
    def test_parse_time_float(self):
        """
        Test parsing time (float).
        """
        t = str2time('0.2')
        self.assertEquals(0.2, t)


    def test_parse_time_int(self):
        """
        Test parsing time (integer).
        """
        t = str2time('2')
        self.assertEquals(2, t)


    def test_parse_time_empty(self):
        """
        Test parsing time (empty).
        """
        t = str2time('')
        self.assertEquals(1, t)



class FileParsingTestCase(unittest.TestCase):
    """
    File parsing tests.
    """
    def test_cleaning_file(self):
        """
        Test cleaning file
        """
        lines = [' ', '', ' # ', '1', '2',]
        result = list(clean_file(lines))
        self.assertEquals(['1', '2'], result)

    
    def test_parsing_file(self):
        """
        Test parsing FPulse file
        """
        lines = [
            '0: 1 0',
            '2: 1/2 0 1',
            '4: 1 0 1 0 1/3.5',
            '5: 1/0.5 0/0.5',
        ]

        leds, pulses = parse_file(lines)
        self.assertEquals([0, 2, 4, 5], leds)
        self.assertEquals(4, len(pulses))

        p1, p2, p3, p4 = pulses

        self.assertEquals([(1, 1), (0, 1)], p1)
        self.assertEquals([(1, 2), (0, 1), (1, 1)], p2)
        self.assertEquals([(1, 1), (0, 1), (1, 1), (0, 1), (1, 3.5)], p3)
        self.assertEquals([(1, 0.5), (0, 0.5)], p4)


# vim: sw=4:et:ai
