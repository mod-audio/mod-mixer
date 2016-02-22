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


def blackorwhite (col):
    r = col.red ()
    g = col.green ()
    b = col.blue ()
    v = 0.23 * r + 0.70 *g + 0.07 * b
#    print (r, g, b, v)
    if v > 120: return QtGui.QColor (0, 0, 0)
    else:       return QtGui.QColor (255, 255, 255)

    
def make_widget_pixmap (sx, sy, pal):
    pm = QtGui.QPixmap (sx, sy);
    pm.fill(pal.color (pal.Window))
    qp = QtGui.QPainter (pm)
    qp.setRenderHint (QtGui.QPainter.Antialiasing)
    return pm, qp


def make_led_pixmap (pal, col0, col1):
    pm, qp = make_widget_pixmap (13, 13, pal)
    qp.translate (6.5, 6.5)
    r = 5
    cg = QtGui.QRadialGradient (0, 0, r, -0.4 * r, -0.4 * r)
    cg.setColorAt (0.0, col0)
    cg.setColorAt (0.8, col1)
    qp.setPen (QtCore.Qt.NoPen)
    qp.setBrush(cg)
    qp.drawEllipse (QtCore.QPoint (0, 0), r, r)
    return pm


def make_leds (pal):
    global led0pm, led2pm, led3pm, led4pm, led5pm, led6pm
    led0pm = make_led_pixmap (pal, QtGui.QColor (255, 255, 255), QtGui.QColor (130, 130, 130))
    led2pm = make_led_pixmap (pal, QtGui.QColor (255, 255, 255), QtGui.QColor (255, 0, 0))
    led3pm = make_led_pixmap (pal, QtGui.QColor (255, 255, 255), QtGui.QColor (255, 180, 0))
    led4pm = make_led_pixmap (pal, QtGui.QColor (255, 255, 255), QtGui.QColor (220, 220, 0))
    led5pm = make_led_pixmap (pal, QtGui.QColor (255, 255, 255), QtGui.QColor (0, 220, 0))
    led6pm = make_led_pixmap (pal, QtGui.QColor (255, 255, 255), QtGui.QColor (80, 80, 255))
