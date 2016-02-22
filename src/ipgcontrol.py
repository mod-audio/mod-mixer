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


from PyQt4 import QtGui, QtCore
from pixutils import *
from rotarybase import *


class IPGcontrol (RotaryBase):

    style = None
    
    def __init__(self, parent):
        super (IPGcontrol, self).__init__(parent, IPGcontrol.style)
        self.set_value (0)

    def set_value (self, v):
        self.value = min (max (v, 0), 3)
        self.angle = 45 * (self.value + 4.5)
        self.update ()
        
    def get_value (self):
        return self.value

    def mousePressEvent (self, E):
        if E.button() == 4: return
        RotaryBase.x0 = E.x()
        RotaryBase.y0 = E.y()
        RotaryBase.v0 = self.value
        
    def mouseReleaseEvent (self, E):
        if E.button() == 4: return

    def mouseMoveEvent (self, E):
        dx = E.x() - RotaryBase.x0
        dy = E.y() - RotaryBase.y0
        v = RotaryBase.v0 + int (0.04 * (dx - dy))
        self.set_value (v)
        self.valueEvent.emit (self)
        
    def wheelEvent (self, E):
        d = E.delta ()
        if d > 0: d = 1
        else:     d = -1
        v = self.value + d
        self.set_value (v)
        self.valueEvent.emit (self)

  
    @classmethod       
    def make_style (cls, rad, tlw, pal, col0, col1):
        pm, qp = make_widget_pixmap (65, 45, pal)
        rx = 32.5
        ry = 30.5
        qp.translate (rx, ry)
        qp.setPen (QtGui.QPen(pal.color (pal.WindowText), tlw))
        qp.setBrush (QtCore.Qt.NoBrush)
        r1 = rad + 2
        pt = QtGui.QPainterPath ()
        pt.moveTo (0, 0)
        pt.lineTo (-15, -6)
        pt.moveTo (0, 0)
        pt.lineTo (-6, -15)
        pt.moveTo (0, 0)
        pt.lineTo (6, -15)
        pt.moveTo (0, 0)
        pt.lineTo (15, -6)
        qp.drawPath (pt)
        ft = QtGui.QFont("freesans", 15, QtGui.QFont.Bold)
        ft.setPixelSize (9)
        qp.setFont (ft)
        qp.drawText (-23,  -3, '0')
        qp.drawText (-15, -17, '12')
        qp.drawText (  6, -17, '25')
        qp.drawText ( 18,  -3, '36')
        RotaryBase.make_pixmap (qp, rad, col0, col1) 
        bgc = blackorwhite (col1)
        cls.style = RotaryStyle (pm, rad - 2, bgc, 2.5, rx, ry)


       
