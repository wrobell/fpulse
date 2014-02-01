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
Common purpose algorithms needed by FPulse.
"""

from functools import reduce

def gcd(a, b):
    """
    Calculate greatest common divisor of `a` and `b`.
    """
    while b:      
        a, b = b, a % b
    return a


def lcm(a, b):
    """
    Calculate least common multiple of `a` and `b`.
    """
    return a * b // gcd(a, b)


def lcmm(*args):
    """
    Calculate least common multiple of all numbers in `args`.
    """
    return reduce(lcm, args)


def flatten(seq):
    """
    Flatten sequence of sequences.
    """
    return (v for item in seq for v in item)


# vim: sw=4:et:ai
