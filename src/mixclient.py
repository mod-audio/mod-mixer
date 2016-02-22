#!/usr/bin/python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
#  Copyright (C) 2015 Fons Adriaensen <fons@linuxaudio.org>
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


import sys
import signal
import socket
from tcpconn import Tcpconn
from PyQt4 import QtGui, QtCore
from buttonbase import *
from ipgcontrol import *
from pgacontrol import *
from daccontrol import *
from auxcontrol import *
from k20meter import *

servaddr = ('192.168.51.1', 4000)


def make_styles (pal):
    global BYPstyle
    global FXBstyle
    global IPGstyle
    global HP1style
    global HP2style
    global K20metrics
    bgcol = pal.color (pal.Window)
    fgcol = [ QtGui.QColor (80, 80, 80), QtGui.QColor (255, 50, 50) ]              
    txcol = [ QtGui.QColor (255, 255, 255), QtGui.QColor (255, 255, 255) ]
    font = QtGui.QFont("freesans", 12, QtGui.QFont.Normal)
    font.setPixelSize (12)
    BYPstyle = ButtonStyle (ButtonBase.make_pixmap (60, 22, bgcol, fgcol, 'Bypass', txcol, font), 2)             
    FXBstyle = ButtonStyle (ButtonBase.make_pixmap (60, 26, bgcol, fgcol, 'FX Byp', txcol, font), 2)             
    fgcol = [ QtGui.QColor (80, 80, 80), QtGui.QColor (220, 180, 50) ]              
    txcol = [ QtGui.QColor (255, 255, 255), QtGui.QColor (0, 0, 0) ]
    HP1style = ButtonStyle (ButtonBase.make_pixmap (30, 16, bgcol, fgcol, 'In', txcol, font), 2)             
    HP2style = ButtonStyle (ButtonBase.make_pixmap (30, 16, bgcol, fgcol, 'Out', txcol, font), 2)             
    IPGcontrol.make_style (12, 1.4, pal, QtGui.QColor (255, 255, 255), QtGui.QColor (110, 110, 255))
    PGAcontrol.make_style (12, 1.5, pal, QtGui.QColor (255, 255, 255), QtGui.QColor (110, 110, 255))
    DACcontrol.make_style (12, 1.5, pal, QtGui.QColor (255, 255, 255), QtGui.QColor (220, 180, 50))
    AUXcontrol.make_style (12, 1.5, pal, QtGui.QColor (255, 255, 255), QtGui.QColor (220, 180, 50))
    K20metrics = k20metrics (bgcol, 220)

    

class Mainwin(QtGui.QMainWindow):

    def __init__(self): 
        super (Mainwin, self).__init__()
        self.setGeometry(100, 100, 420, 270)
        self.setWindowTitle('MOD Mixer')
        x = 0
        self.makelabel (x + 5, 3, 80, 14, "Chan 1")
        self.ipgctl1 = IPGcontrol (self)
        self.ipgctl1.move (x + 8, 30)
        self.ipgctl1.valueEvent.connect (self.ipgevent)
        self.pgactl1 = PGAcontrol (self)
        self.pgactl1.move (x + 8, 75)
        self.pgactl1.valueEvent.connect (self.pgaevent)
        self.makelabel (x + 5, 130, 80, 11, "Input gain")
        self.dacctl1 = DACcontrol (self)
        self.dacctl1.move (x + 8, 150)
        self.dacctl1.valueEvent.connect (self.dacevent)
        self.makelabel (x + 5, 205, 70, 11, "Output")
        self.bpch1 = ButtonBase (self, BYPstyle, 0);
        self.bpch1.bpressEvent.connect (self.bypass)
        self.bpch1.move (x + 10, 235)
        self.meters1 = Kmeter (self, K20metrics, 2, 5)
        self.meters1.move (x + 83, 18)
        x += 150
        self.makelabel (x + 5, 3, 80, 14, "Chan 2")
        self.ipgctl2 = IPGcontrol (self)
        self.ipgctl2.move (x + 8, 30)
        self.ipgctl2.valueEvent.connect (self.ipgevent)
        self.pgactl2 = PGAcontrol (self)
        self.pgactl2.move (x + 8, 75)
        self.pgactl2.valueEvent.connect (self.pgaevent)
        self.makelabel (x + 5, 130, 80, 11, "Input gain")
        self.dacctl2 = DACcontrol (self)
        self.dacctl2.move (x + 8, 150)
        self.dacctl2.valueEvent.connect (self.dacevent)
        self.makelabel (x + 5, 205, 70, 11, "Output")
        self.bpch2 = ButtonBase (self, BYPstyle, 1);
        self.bpch2.bpressEvent.connect (self.bypass)
        self.bpch2.move (x + 10, 235)
        self.meters2 = Kmeter (self, K20metrics, 2, 5)
        self.meters2.move (x + 83, 18)
        x += 150
        self.bpfx = ButtonBase (self, FXBstyle, 2);
        self.bpfx.bpressEvent.connect (self.bypass)
        self.bpfx.move (x + 30, 20)
        self.hpip = ButtonBase (self, HP1style, 0);
        self.hpip.bpressEvent.connect (self.hpinp)
        self.hpip.move (x + 30, 135)
        self.hpop = ButtonBase (self, HP2style, 1);
        self.hpop.bpressEvent.connect (self.hpinp)
        self.hpop.move (x + 61, 135)
        self.auxctl = AUXcontrol (self)
        self.auxctl.move (x + 28, 160)
        self.auxctl.valueEvent.connect (self.auxevent)
        self.makelabel (x + 20, 205, 80, 11, "Monitor")
        self.count = 1
        self.tcpch = None
        self.timer = QtCore.QBasicTimer ()
        self.timer.start (50, self)
        self.show ()

    def makelabel (self, x, y, dx, fs, txt):
        lb = QtGui.QLabel (self)
        lb.setGeometry (x, y, dx, 16)
        ft = QtGui.QFont("freesans", 12, QtGui.QFont.Normal)
        ft.setPixelSize (fs)
        lb.setFont (ft)
        lb.setAlignment (QtCore.Qt.AlignHCenter)
        lb.setText (txt)
        lb.show ()
        return lb
       
    def paintEvent(self, E):
        qp = QtGui.QPainter()
        pal = self.palette ()
        qp.begin(self)
        qp.translate (0.5, 0.5)
        qp.setRenderHint (QtGui.QPainter.Antialiasing)
        qp.setBrush (QtCore.Qt.NoBrush)
        for x in (150, 300):
            qp.setPen (QtGui.QPen(pal.color (pal.Dark), 1.0))
            qp.drawLine (x, 0.0, x, 300) 
            qp.setPen (QtGui.QPen(pal.color (pal.Light), 1.0))
            qp.drawLine (x + 1, 0.0, x + 1, 300) 

    def bypass (self, butt):
        s = butt.get_state () ^ 1
        butt.set_state (s)
        if   butt == self.bpch1:self.send (['mixer', 4, [s]])
        elif butt == self.bpch2:self.send (['mixer', 5, [s]])
        # !!!! INVERTED - DRIVER BUG
        elif butt == self.bpfx:self.send (['mixer', 9, [s ^ 1]])
        
    def hpinp (self, butt):
        s = butt.get_state () ^ 1
        i = butt.get_index ()
        butt.set_state (s)
        if i == 0: self.hpop.set_state (0)
        if i == 1: self.hpip.set_state (0)
        self.send_hpinp ()
        
    def send_hpinp (self):
        s = self.hpop.get_state () + 2 * self.hpip.get_state ()
        self.send (['mixer', 8, [s]])
        
    def ipgevent (self, ctl):
        if ctl == self.ipgctl1:
            self.send (['mixer', 2, [self.ipgctl1.get_value ()]])
        elif ctl == self.ipgctl2:
            self.send (['mixer', 3, [self.ipgctl2.get_value ()]])
        
    def pgaevent (self, ctl):
        # !!!! SWAPPED - DRIVER BUG
        self.send (['mixer', 7, [self.pgactl1.get_value (), self.pgactl2.get_value ()]])
        
    def dacevent (self, ctl):
        self.send (['mixer', 6, [self.dacctl2.get_value (), self.dacctl1.get_value ()]])
        
    def auxevent (self, ctl):
        self.send (['mixer', 1, [self.auxctl.get_value ()]])

    def sendall (self):
        self.auxevent (None)
        self.ipgevent (self.ipgctl1)
        self.ipgevent (self.ipgctl2)
        self.send (['mixer', 4, [self.bpch1.get_state ()]])
        self.send (['mixer', 5, [self.bpch1.get_state ()]])
        self.dacevent (None)
        self.pgaevent (None)
        self.send_hpinp ()
        self.send (['mixer', 9, [self.bpfx.get_state () ^ 1]]) # INVERTED
        
    def send (self, mesg):
        if self.tcpch is not None:
            try:
                self.tcpch.send_object (mesg)
            except:
                self.sock.close ()
                self.tcpch = None
                self.count = 20

    def recv (self):
        if self.tcpch is not None:
            try:
                M =  self.tcpch.recv_object ()
                if M [0] == 'levels': self.levels (M [1])
            except:
                self.sock.close ()
                self.tcpch = None
                self.count = 20

    def levels (self, L):
        self.meters1.setval (0, L [0])
        self.meters1.setval (1, L [1])
        self.meters1.update ()
        self.meters2.setval (0, L [2])
        self.meters2.setval (1, L [3])
        self.meters2.update ()
                
    def timerEvent (self, ev):
        if self.tcpch is None:
            self.count -= 1
            if self.count == 0:
                try:
                    self.sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.sock.connect (servaddr)
                    self.tcpch = Tcpconn (self.sock)
                    self.sendall ()
                except socket.error:
                    self.count = 60
        else:
            self.send (['levels'])
            self.recv ()
                   
        
def main():

    signal.signal (signal.SIGINT, signal.SIG_DFL)
    app = QtGui.QApplication(sys.argv)
    bgc = QtGui.QColor (70, 70, 70)
    fgc = QtGui.QColor (255, 255, 255)
    pal = app.palette()
    pal.setColor(pal.Window, bgc)
    pal.setColor(pal.Button, bgc)
    pal.setColor(pal.Base, bgc)
    pal.setColor(pal.WindowText, fgc)
    pal.setColor(pal.ButtonText, fgc)
    pal.setColor(pal.Text, fgc)
    pal.setColor(pal.Dark, QtGui.QColor (0, 0, 0))
    pal.setColor(pal.Light, QtGui.QColor (140, 140, 140))
    app.setPalette (pal)
    make_styles (pal)
    win = Mainwin ()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
