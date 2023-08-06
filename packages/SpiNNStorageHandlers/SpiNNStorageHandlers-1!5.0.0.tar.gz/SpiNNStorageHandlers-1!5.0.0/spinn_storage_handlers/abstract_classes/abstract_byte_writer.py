# Copyright (c) 2017 The University of Manchester
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

from six import add_metaclass
from spinn_utilities.abstract_base import AbstractBase, abstractmethod


@add_metaclass(AbstractBase)
class AbstractByteWriter(object):
    """ An abstract writer of bytes.

    .. note::
        Due to endianness concerns, the methods of this writer should be used\
        directly for the appropriate data type being written; e.g. an int\
        should be written using write_int rather than calling write_byte 4\
        times with the bytes of the int, unless a specific endianness is being\
        achieved.
    """

    __slots__ = []

    @abstractmethod
    def write_byte(self, byte_value):
        """ Writes the lowest order byte of the given value.

        :param byte_value: The byte to write
        :type byte_value: int
        :return: Nothing is returned
        :rtype: None
        :raise IOError: If there is an error writing to the stream
        """

    def write_bytes(self, byte_iterable):
        """ Writes a set of bytes.

        :param byte_iterable: The bytes to write
        :type byte_iterable: bytes or bytearray or iterable(bytes or bytearray)
        :return: Nothing is returned
        :rtype: None
        :raise IOError: If there is an error writing to the stream
        """

    @abstractmethod
    def write_short(self, short_value):
        """ Writes the two lowest order bytes of the given value.

        :param short_value: The short to write
        :type short_value: int
        :return: Nothing is returned
        :rtype: None
        :raise IOError: If there is an error writing to the stream
        """

    @abstractmethod
    def write_int(self, int_value):
        """ Writes a four byte value.

        :param int_value: The integer to write
        :type int_value: int
        :return: Nothing is returned
        :rtype: None
        :raise IOError: If there is an error writing to the stream
        """

    @abstractmethod
    def write_long(self, long_value):
        """ Writes an eight byte value.

        :param long_value: The 64-bit int to write
        :type long_value: int
        :return: Nothing is returned
        :rtype: None
        :raise IOError: If there is an error writing to the stream
        """

    @abstractmethod
    def get_n_bytes_written(self):
        """ Determines how many bytes have been written in total.

        :return: The number of bytes written
        :rtype: int
        :raise None: Does not raise exceptions
        """
