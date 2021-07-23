from PyQt4.QtGui import QApplication
from sys import argv, exit
from Syntax_UI import SyntaxUI, GPIOsetup

if __name__ == "__main__":
    GPIOsetup()
    app = QApplication(argv)
    form = SyntaxUI()
    form.BaleBotT.start()
    form.show()
    exit(app.exec_())