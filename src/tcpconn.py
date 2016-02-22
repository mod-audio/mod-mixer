# ----------------------------------------------------------------------------
#
#  Copyright (C) 2012-2015 Fons Adriaensen <fons@linuxaudio.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http:#www.gnu.org/licenses/>.
#
# ----------------------------------------------------------------------------


import socket
import struct
import pickle


class Tcpconn ():
    """"
    Simple data send/receive routines for a TCP connection.
    All functions should be called inside a try/except block
    catching the OSError exception. This will be raised also
    by the blocking receive functions when the other side
    disconnects.
    """

    def __init__ (self, sock):
        """
        The socket must represent an open TCP connection.
        """
        self._sock = sock

    def send_object (self, O):
        """
        Send an arbitrary python object.
        """
        b = pickle.dumps (O)
        h = struct.pack ("!i", len (b))
        self._sock.sendall (h)
        self._sock.sendall (b)

    def recv_object (self):
        """
        Receive an arbitrary python object.
        """
        b = self._rx (4)
        n = struct.unpack ("!i", b)[0]
        b = self._rx (n)
        return pickle.loads (b)

    def send_array (self, A):
        """
        Send the data of a numpy array without making
        an intermediate copy. The receiver must have
        been informed of at least the data size before.
        """
        v = memoryview (A).cast ('B')
        self._sock.sendall (v)

    def recv_array (self, A):
        """
        Receive the data of a numpy array without making
        an intermediate copy. The data size of 'A' must
        exactly match the amount of data sent.
        """
        v = memoryview (A).cast ('B')
        while len (v):
            k = self._sock.recv_into (v)
            if not k: raise OSError
            v = v [k:]

    def _rx (self, n):
        """
        For internal use only, replaces missing recvall().
        """
        b = b''
        while n:
            d = self._sock.recv (n)
            k = len (d)
            if not k: raise OSError
            b += d
            n -= k
        return b

