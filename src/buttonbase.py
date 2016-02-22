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


class ButtonStyle ():

    def __init__(self, pixmap, nstate):
        self.pixmap = pixmap
        self.nstate = nstate
        self.dx = pixmap.width ()
        self.dy = pixmap.height () // nstate


class ButtonBase (QtGui.QWidget):

    bpressEvent = QtCore.pyqtSignal(object)
    brelseEvent = QtCore.pyqtSignal(object)

    def __init__(self, parent, style, index = None):
        super (ButtonBase, self).__init__(parent)
        self.resize (style.dx, style.dy)
        self._style = style
        self._state = 0
        self._index = index

    def set_state (self, s):
        s %= self._style.nstate
        s = (s << 1) | (self._state & 1)
        if s != self._state:
            self._state = s
            self.update ()

    def get_state (self):
        return self._state >> 1

    def get_index (self):
        return self._index

    def mousePressEvent (self, E):
        self._state |= 1
        self.update ()
        self.bpressEvent.emit (self)

    def mouseReleaseEvent (self, E):
        self._state &= ~1
        self.update ()
        self.brelseEvent.emit (self)

    def paintEvent (self, e):
        st = self._style
        pm = st.pixmap
        k = self._state >> 1
        d = self._state & 1
        qp = QtGui.QPainter ()
        qp.begin (self)
        qp.drawPixmap (d, d, pm, 0, k * st.dy, st.dx - d, st.dy - d)
        qp.end ()


    @classmethod
    def make_pixmap (cls, sx, sy, bgcol, fgcol, texts = None, txcol = None, font = None):
        if isinstance (fgcol, (list, tuple)): nc = len (fgcol)
        else:
            fgcol = [fgcol]
            nc = 1
        if texts is None: nt = 0
        elif isinstance (texts, (list, tuple)): nt = len (texts)
        else:
            texts = [texts]
            nt = 1
        n = max (nc, nt)
        pm = QtGui.QPixmap (sx, n * sy);
        pm.fill (bgcol)
        qp = QtGui.QPainter (pm)
        qp.setRenderHint (QtGui.QPainter.Antialiasing)
        sh = QtGui.QColor (0, 0, 0, 180)
        if texts is not None:
            qp.setFont (font)
            fm = qp.fontMetrics ()
            y = 0.5 * (sy - fm.height ()) + fm.ascent ()
        for i in range (n):
            qp.setPen (QtCore.Qt.NoPen)
            d = 1
            pt = QtGui.QPainterPath ()
            pt.moveTo (0, sy - d)
            pt.lineTo (d, sy)
            pt.lineTo (sx, sy)
            pt.lineTo (sx, d)
            pt.lineTo (sx - d, 0)
            pt.lineTo (sx - d, sy - d)
            pt.lineTo (0, sy - d)
            qp.fillPath (pt, sh)
            cg = QtGui.QLinearGradient (0, 0, 2, 2 + sx / 10)
            cg.setColorAt (0, QtGui.QColor (250, 250, 250))
            cg.setColorAt (1, fgcol [i % nc])
            qp.fillRect (0, 0, sx - d, sy - d, cg)
            if texts is not None:
                t = texts [i % nt]
                w = fm.width (t)
                x = 0.5 * (sx - w - 1)
                qp.setPen (txcol [i % nc])
                qp.drawText (x, y, t)
            qp.translate (0, sy)
        qp.end ()
        return pm

