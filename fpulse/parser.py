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

from collections import namedtuple
import re

Pulse = namedtuple('Pulse', 'value time')
Pulse.__doc__ = """
LED pulse.

LED pulse is LED's brightness for a period of time.

:var value: LED state value (float number between 0 and 1).
:var time: Time in seconds (can be fractional, i.e. 0.5s).
"""

RE_SEQ = re.compile('(?:([01]|0\.[0-9]+)(?:/([0-9]+(?:\.[0-9]+)?))?)(?:\s+|$)')

def str2time(s):
    """
    Convert string to time in seconds.

    Empty string is converted to 1s.

    :param s: String to convert.
    """
    return float(s) if s else 1


def clean_file(f):
    """
    Prepare FPulse input file lines for parsing.

    Each line is
    
    - stripped of leading and trailing whitespace
    - empty and comment lines are removed

    :param f: Text file to clean (or any other iterable of lines).
    """
    lines = (l.strip() for l in f)
    lines = (l for l in lines if l)
    lines = (l for l in lines if l[0] != '#')
    return lines


def parse_file(f):
    """
    Parse file into a list of `Pulse` objects.

    The functions returns tuple of two lists

    - list of LED numbers
    - list of `Pulse` tuples for each LED
    """
    lines = clean_file(f)
    leds = []
    pulses = []
    for line in lines:
        tokens = line.split(':')
        leds.append(int(tokens[0]))
        pulses.append([
            Pulse(float(v[0]), str2time(v[1]))
            for v in RE_SEQ.findall(tokens[1])
        ])

    return leds, pulses


# vim: sw=4:et:ai
