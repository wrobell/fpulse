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
FPulse application main functions.
"""

import itertools
import time

from .parser import parse_file
from .ft import lcmm, flatten

def pulse_time(pulses):
    """
    Find minimal pulse time.
    """
    pulse_times = (p.time % 1 for pt in pulses for p in pt)
    return min(t if t else 1 for t in pulse_times)


def transform_pulses(pulses, p_time):
    """
    Transform sequences of pulses into LED brightness values to be sent at
    a time.

    For example, LED pulses definition

        0: 1/2 0
        2: 1 0/0.5

    results in LED brightness values sent every 0.5s (or multiplication of
    0.5s to minimize device communication)::

        1 1  # 2 * 0.5s
        1 0  # 0.5s
        1 1  # 0.5s, restart LED 2
        0 1
        0 0
    
    """
    # expand each pulse to a sequence of pulse values, so each lasts for
    # minimal pulse time, i.e.
    #
    #    (Pulse(1, 1.5), Pulse(0, 1)) -> (1, 1, 1, 0, 0)
    values = [
        tuple(flatten((p.value,) * round(p.time / p_time) for p in pt))
        for pt in pulses
    ]

    # make each sequence of pulse values to have equal length
    lens = [len(v) for v in values]
    n = lcmm(*lens)
    values = (vt * (n // len(vt)) for vt in values)

    # we have sequence of values for each LED, i.e.
    # 
    #     1: 1 1 0 0 0
    #     2: 1 0 0 1 0
    #
    # transpose sequences to have value of each LED at a time
    # (each sent every minimal pulse time)
    #
    #     1 1
    #     1 0
    #     0 0
    #     0 1
    #     0 0
    #
    values = zip(*values)

    # group the values, to minimize device communication
    groups = itertools.groupby(values)
    values = ((len(list(seq)), key) for key, seq in groups)
    return values


def start(driver, fn):
    """
    Start LED pulsing application.
    """
    f = open(fn)
    leds, pulses = parse_file(f)
    p_time = pulse_time(pulses)
    values = transform_pulses(pulses, p_time)

    for k, led_values in itertools.cycle(values):
        for led, v in zip(leds, led_values):
            driver.set_led(led, v)
        driver.write()
        time.sleep(k * p_time)

# vim: sw=4:et:ai
