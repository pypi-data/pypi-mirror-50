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

import os
import logging
from six import add_metaclass
from spinn_utilities.abstract_base import AbstractBase, abstractmethod

logger = logging.getLogger(__name__)


@add_metaclass(AbstractBase)
class AbstractBufferedDataStorage(object):
    """ An object that can store and read back buffered data.
    """

    __slots__ = []

    @abstractmethod
    def write(self, data):
        """ Store data in the data storage in the position indicated by\
            the write pointer index.

        :param data: the data to be stored
        :type data: bytearray
        :rtype: None
        """

    @abstractmethod
    def read(self, data_size):
        """ Read data from the data storage from the position indicated by\
            the read pointer index.

        :param data_size: number of bytes to be read
        :type data_size: int
        :return: a bytearray containing the data read
        :rtype: bytearray
        """

    @abstractmethod
    def readinto(self, data):
        """ Read some bytes of data from the underlying storage into a\
            predefined array.  Will block until some bytes are available,\
            but may not fill the array completely.

        :param data: The place where the data is to be stored
        :type data: bytearray
        :return: The number of bytes stored in data
        :rtype: int
        :raise IOError: If an error occurs reading from the underlying storage
        """

    @abstractmethod
    def read_all(self):
        """ Read all the data contained in the data storage starting from\
            position 0 to the end.

        :return: a bytearray containing the data read
        :rtype: bytearray
        """

    @abstractmethod
    def seek_read(self, offset, whence=os.SEEK_SET):
        """ Set the data storage's current read position to the offset.

        :param offset: Position of the read pointer within the buffer
        :type offset: int
        :param whence: One of:
            * `os.SEEK_SET` which means absolute buffer positioning (default)
            * `os.SEEK_CUR` which means seek relative to the current read\
              position
            * `os.SEEK_END` which means seek relative to the buffer's end
        :rtype: None
        """

    @abstractmethod
    def seek_write(self, offset, whence=os.SEEK_SET):
        """ Set the data storage's current write position to the offset.

        :param offset: Position of the write pointer within the buffer
        :type offset: int
        :param whence: One of:
            * `os.SEEK_SET` which means absolute buffer positioning (default)
            * `os.SEEK_CUR` which means seek relative to the current write\
              position
            * `os.SEEK_END` which means seek relative to the buffer's end
        :rtype: None
        """

    @abstractmethod
    def tell_read(self):
        """ The current position of the read pointer.

        :return: The current position of the read pointer
        :rtype: int
        """

    @abstractmethod
    def tell_write(self):
        """ The current position of the write pointer.

        :return: The current position of the write pointer
        :rtype: int
        """

    @abstractmethod
    def eof(self):
        """ Check if the read pointer is a the end of the data storage.

        :return: Whether the read pointer is at the end of the data storage
        :rtype: bool
        """

    @abstractmethod
    def close(self):
        """ Closes the data storage.

        :rtype: None
        :raise spinn_storage_handlers.exceptions.DataReadException: \
            If the data storage cannot be closed
        """
