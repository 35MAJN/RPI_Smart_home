from PyQt4.QtGui import QGraphicsOpacityEffect, QGraphicsDropShadowEffect

def Opacity(x):
    Return = QGraphicsOpacityEffect()
    Return.setOpacity(x)
    return Return


def newOrder(self, text):
    self.BaleBot5 = self.BaleBot4
    self.BaleBot4 = self.BaleBot3
    self.BaleBot3 = self.BaleBot2
    self.BaleBot2 = self.BaleBot1
    self.BaleBot1 = self.LastOrderName + " : " + text
    self.SocialTabTXT.setText("<h3>The last five orders:</h3>" + self.BaleBot1
                              + "<br/>" + self.BaleBot2 + "<br/>" + self.BaleBot3
                              + "<br/>" + self.BaleBot4 + "<br/>" + self.BaleBot5)


def Shadow(BlurRadius, Offset, XOffset, YOffset):
    Return = QGraphicsDropShadowEffect()
    Return.setBlurRadius(BlurRadius)
    Return.setOffset(Offset)
    Return.setXOffset(XOffset)
    Return.setYOffset(YOffset)
    return Return
