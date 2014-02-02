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
TLC5947 LED driver.
"""

import ctypes as ct

class Driver(object):
    """
    TLC5947 LED driver.
    """
    BITS_PER_VALUE = 12
    N_LEDS = 24
    MAX_VALUE = 2 ** BITS_PER_VALUE - 1

    def __init__(self):
        n = self._n_leds = self.N_LEDS # * n_drivers
        self._values = [0] * n
        self._lib = ct.CDLL('libbcm2835.so')

        self._n_bytes = int(n * self.BITS_PER_VALUE / 8)
        self._t_array = ct.c_char * self._n_bytes

        self._lib.bcm2835_init();
        self._lib.bcm2835_spi_begin();
        self._lib.bcm2835_spi_chipSelect(0);
        self._lib.bcm2835_spi_setDataMode(0);
        self._lib.bcm2835_spi_setClockDivider(8192)


    def set_led_all(self, v):
        self._values = [int(v * self.MAX_VALUE)] * self._n_leds


    def set_led(self, led, v):
        self._values[led - 1] = int(v * self.MAX_VALUE)


    def write(self):
        tx = self._convert(self._values)
        self._lib.bcm2835_spi_writenb(tx, self._n_bytes);


    def _convert(self, values):
        data = []
        for i in range(23, 0, -2):
            data.append((values[i] >> 4))
            data.append(((values[i] & 0x0f) << 4) | (values[i - 1] >> 8))
            data.append(values[i - 1] & 0xff)
        #from binascii import unhexlify
        #data = unhexlify(''.join(reversed(['{:03x}'.format(v) for v in (values)])))
        return self._t_array(*data)


    def __del__(self):
        self._lib.bcm2835_spi_end();
        self._lib.bcm2835_close();


# vim: sw=4:et:ai
