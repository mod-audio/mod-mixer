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


from PyQt4 import QtGui, QtCore


class RotaryStyle ():
    
    def __init__(self, pixmap, radius, markcol, marklw, rx, ry):
        self.pixmap = pixmap
        self.radius = radius
        self.markcol = markcol
        self.marklw = marklw
        self.rx = rx
        self.ry = ry
        

class RotaryBase (QtGui.QWidget):

    valueEvent = QtCore.pyqtSignal(object)
    button = 0
    modifs = 0
    x0 = 0
    y0 = 0
    v0 = 0

    def __init__(self, parent, style):
        super (RotaryBase, self).__init__(parent)
        self.style = style
        self.angle = 0.0
        self.resize(style.pixmap.width(), style.pixmap.height())

        
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        st = self.style
        pm = st.pixmap
        qp.begin(self)
        qp.setRenderHint (QtGui.QPainter.Antialiasing)
        qp.drawPixmap (0, 0, pm, 0, 0, pm.width(), pm.height() )
        qp.translate (st.rx, st.ry)
        qp.rotate (self.angle) 
        qp.setPen (QtGui.QPen(QtGui.QColor (st.markcol), st.marklw, QtCore.Qt.SolidLine))
        qp.setBrush (QtCore.Qt.NoBrush)
        qp.drawLine (2, 0, st.radius, 0)
        qp.end()


    @classmethod    
    def make_pixmap (cls, qp, rad, col0, col1):
        qp.setPen(QtCore.Qt.NoPen)
        bl = QtGui.QColor(0, 0, 0)
        qp.setBrush(bl)
        d = rad / 5
        qp.drawEllipse (QtCore.QPoint (d, d), rad, rad)
        cg = QtGui.QRadialGradient (0, 0, rad, -0.5 * rad, -0.5 * rad)
        cg.setColorAt (0, col0)
        cg.setColorAt (1, col1)
        qp.setPen (QtGui.QPen(bl, 0.4))
        qp.setBrush(cg)
        qp.drawEllipse (QtCore.QPoint (0, 0), rad, rad)


        
