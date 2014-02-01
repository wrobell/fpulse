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
FPulse core tests.
"""

from fpulse.parser import Pulse
from fpulse.core import pulse_time, transform_pulses

import unittest

class PulseTransformTestCase(unittest.TestCase):
    """
    Tests of pulse processing functions.
    """
    def test_pulse_time_frac(self):
        """
        Test finding minimal pulse time (fractional)
        """
        pulses = [(Pulse(1, 3), Pulse(1, 4)), (Pulse(1, 2), Pulse(1, 20))]
        pt = pulse_time(pulses)
        self.assertEquals(2, pt)


    def test_pulse_time_frac(self):
        """
        Test finding minimal pulse time (fractional)
        """
        pulses = [(Pulse(1, 3.5), Pulse(1, 1)), (Pulse(1, 2), Pulse(1, 2))]
        pt = pulse_time(pulses)
        self.assertEquals(0.5, pt)


    def test_pulse_transform(self):
        """
        Test pulse transform
        """
        pulses = [
            (Pulse(1, 2), Pulse(0, 1)),
            (Pulse(1, 1), Pulse(0, 0.5)),
        ]
        values = transform_pulses(pulses, 0.5)
        expected = [
            (2, (1, 1)),
            (1, (1, 0)),
            (1, (1, 1)),
            (1, (0, 1)),
            (1, (0, 0))
        ]
        self.assertEquals(expected, list(values))


# vim: sw=4:et:ai
