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
Fake LED driver to print LED brightness values as hex values.
"""

class Driver(object):
    """
    Hex LED driver.
    """

    N_LEDS = 16

    def __init__(self):
        """
        Create the driver.
        """
        self._values = [0]  * self.N_LEDS


    def set_led_all(self, v):
        self._values = [int(v * 15)] * self.N_LEDS


    def set_led(self, led, v):
        self._values[led - 1] = int(v * 15)


    def write(self):
        s = ''.join('{:x}'.format(v) for v in self._values)
        print('\r' + s, end='')


# vim: sw=4:et:ai
