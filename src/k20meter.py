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


from math import log10
from PyQt4 import QtGui, QtCore


def makek20pixmap0 (sx, sy, m):
    M = QtGui.QPixmap (sx, sy + 2 * m);
    P = QtGui.QPainter (M)
    G = QtGui.QLinearGradient (0, sy + m, 0, m)
    G.setColorAt (0.00, QtGui.QColor (50, 50, 120))
    G.setColorAt (0.20, QtGui.QColor (0, 70, 90))
    G.setColorAt (0.55, QtGui.QColor (0, 90, 0))
    G.setColorAt (0.63, QtGui.QColor (100, 100, 0))
    G.setColorAt (1.00, QtGui.QColor (100, 30, 0))
    P.setPen(QtCore.Qt.NoPen)
    P.setBrush(G)
    P.drawRect (0.0, 0.0, sx, sy + 2 * m)
    return M        

def makek20pixmap1 (sx, sy, m):
    M = QtGui.QPixmap (sx, sy + 2 * m);
    P = QtGui.QPainter (M) 
    G = QtGui.QLinearGradient (0, sy + m, 0, m)
    G.setColorAt (0.00, QtGui.QColor (90, 90, 255))
    G.setColorAt (0.20, QtGui.QColor (0, 190, 190))
    G.setColorAt (0.55, QtGui.QColor (0, 255, 0))
    G.setColorAt (0.63, QtGui.QColor (255, 255, 0))
    G.setColorAt (0.75, QtGui.QColor (255, 128, 50))
    G.setColorAt (1.00, QtGui.QColor (255, 50, 50))
    P.setPen(QtCore.Qt.NoPen)
    P.setBrush(G)
    P.drawRect (0.0, 0.0, sx, sy + 2 * m)
    return M        

def makek20pixmap2 (sx, sy, m, bg):
    M = QtGui.QPixmap (sx, sy + 2 * m);
    P = QtGui.QPainter (M)
    P.setPen(QtCore.Qt.NoPen)
    P.setBrush(bg)
    P.drawRect (0.0, 0.0, sx, sy + 2 * m)
    S = [((120, 120, 255), (0.0, 1.00e-3, 3.16e-3)),
         ((  0, 255,   0), (1.00e-2, 3.16e-2)),
         ((255, 255,   0), (1.00e-1,)),
         ((255,  50,  50), (3.16e-1, 1.00))]
    P.setBrush (QtCore.Qt.NoBrush)
    for X in S:
        C = X [0]
        L = X [1];
        P.setPen (QtGui.QColor (C [0], C [1], C [2]))   
        for v in L:
           d = sy + m - sy * K20mapfunc (v)
           P.drawLine (0, d, sx, d)
    return M        

def makek20pixmap3 (sx, sy, m, bg):
    M = QtGui.QPixmap (sx, sy + 2 * m);
    P = QtGui.QPainter (M)
    P.setPen(QtCore.Qt.NoPen)
    P.setBrush(bg)
    P.drawRect (0.0, 0.0, sx, sy + 2 * m)
    F = QtGui.QFont ('Sans', 7, QtGui.QFont.Normal)
    P.setFont (F)
    dx = sx / 2
    dy = sy + m
    P.setPen (QtGui.QColor (140, 140, 255))
    drawctext (P, dx, dy - sy * K20mapfunc (1.00e-3), "-40");
    drawctext (P, dx, dy - sy * K20mapfunc (3.16e-3), "-30");
    P.setPen (QtGui.QColor (0, 255, 0))
    drawctext (P, dx, dy - sy * K20mapfunc (1.00e-2), "-20");
    drawctext (P, dx, dy - sy * K20mapfunc (3.16e-2), "-10");
    P.setPen (QtGui.QColor (255, 255, 0))
    drawctext (P, dx, dy - sy * K20mapfunc (1.00e-1), "0");
    P.setPen (QtGui.QColor (255, 80, 80))
    drawctext (P, dx, dy - sy * K20mapfunc (3.16e-1), "10");
    drawctext (P, dx, dy - sy * K20mapfunc (1.00), "20");
    return M

def drawctext (P, x, y, s):
    M = P.fontMetrics ()
    w = M.width (s)
    P.drawText (x - w / 2, y + M.ascent () // 2, s)

def k20metrics (bg, size):
    return ((makek20pixmap0 (5, size, 6),
             makek20pixmap1 (5, size, 6),
             makek20pixmap2 (5, size, 6, bg),
             makek20pixmap3 (18, size, 6, bg)),
             K20mapfunc, size, 6)

def K20mapfunc (v):
    a =  3 / 64.0
    b = 30 / 64.0
    c = 67 / 64.0
    d =  6 / 16.0
    if v < 1e-3: return 1e3 * v / 16
    v = log10 (v)
    if v < -1.0: return  c + v * (b + v * a)
    if v > 0.05: v = 0.05;
    return 1 + d * v


class Kmeter (QtGui.QWidget):

    def __init__(self, parent, metrics, n, w):
        super (Kmeter, self).__init__(parent)
        self.pixmaps = metrics [0]
        self.mapfunc = metrics [1]
        self.size = metrics [2]
        self.marg = metrics [3]
        self.n = n
        self.w0 = w
        self.w2 = self.pixmaps [2].width () 
        self.w3 = self.pixmaps [3].width () 
        self.sx = n * (w + self.w2) - self.w2 + 2 * self.w3 
        self.sy = self.pixmaps [0].height ()
        self.rms = [self.marg for i in range (n)]
        self.pks = [self.marg for i in range (n)]
        self.resize (self.sx, self.sy)
        
    def paintEvent (self, ev):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen (QtCore.Qt.NoPen)
        qp.setBrush (QtGui.QColor (255, 255, 255))
        n = self.n
        w0 = self.w0
        w2 = self.w2
        w3 = self.w3
        x = 0
        y = 0
        qp.drawPixmap (x, y, self.pixmaps [3], 0, 0, w3, self.sy)
        x = w3
        for i in range (n):
            self.drawmeter (x, y, qp, i)
            x += w0
            if i < n - 1:
                qp.drawPixmap (x, y, self.pixmaps [2], 0, 0, w2, self.sy)
                x += w2
        qp.drawPixmap (x, y, self.pixmaps [3], 0, 0, w3, self.sy)
        qp.end()

    def drawmeter (self, x, y, qp, ind):
        dx = self.w0
        dy1 = self.rms [ind]
        dy2 = self.pks [ind] + 1
        qp.drawPixmap (x, y + self.sy - dy1, self.pixmaps [1], 0, self.sy - dy1, dx, dy1)
        qp.drawPixmap (x, y, self.pixmaps [0], 0, 0, dx, self.sy - dy1)
        if dy2 > max (40, dy1): qp.drawRect (x, y + self.sy - dy2, dx, 3)
                      
    def setval (self, ind, val):
        self.rms [ind] = self.marg + self.size * self.mapfunc (val [0])
        self.pks [ind] = self.marg + self.size * self.mapfunc (val [1])
        

