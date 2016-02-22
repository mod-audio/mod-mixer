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


class PGAcontrol (RotaryBase):

    style = None

    def __init__(self, parent):
        super (PGAcontrol, self).__init__(parent, PGAcontrol.style)
        self.scale = 48 / 270.0
        self.set_value (24)

    def set_value (self, v):
        v = max (min (v, 48), 0)
        self.value = v
        self.angle = (v - 24) / self.scale - 90.0
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
        v = int (RotaryBase.v0 + (dx - dy) // 2)
        self.set_value (v)
        self.valueEvent.emit (self)
        
    def wheelEvent (self, E):
        d = E.delta ()
        if d > 0: d = 2
        else:     d = -2
        if E.modifiers () == QtCore.Qt.ShiftModifier:
            d //= 2
        self.set_value (self.value + d)
        self.valueEvent.emit (self)

    @classmethod
    def make_style (cls, rad, tlw, pal, col0, col1):
        pm, qp = make_widget_pixmap (65, 51, pal)
        rx = 32.5
        ry = 28.5
        qp.translate (rx, ry)
        qp.setPen (QtGui.QPen(pal.color (pal.WindowText), tlw))
        qp.setBrush (QtCore.Qt.NoBrush)
        r1 = rad + 2
        r2 = rad + 5
        cs = [ 0.7, 1.0, 0.7, 0.0, -0.7, -1.0, -0.7, 0.0, 0.7, 1.0 ]
        pt = QtGui.QPainterPath ()
        for i in range (7):
            c = cs [i]
            s = cs [i + 2]
            pt.moveTo (c * r1, s * r1)
            pt.lineTo (c * r2, s * r2)
        qp.drawPath (pt)
        ft = QtGui.QFont("freesans", 15, QtGui.QFont.Bold)
        ft.setPixelSize (9)
        qp.setFont (ft)
        qp.drawText ( -1, -19, '0')
        qp.drawText (-30,  18, '-12')
        qp.drawText ( 13,  18, '+12')
        RotaryBase.make_pixmap (qp, rad, col0, col1) 
        bgc = blackorwhite (col1)
        cls.style = RotaryStyle (pm, rad - 2, bgc, 2.5, rx, ry)

        
