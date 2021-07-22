from PyQt4.QtGui import QApplication
from sys import argv, exit
# import RPI
from Syntax_UI import SyntaxUI

if __name__ == "__main__":
    app = QApplication(argv)
    form = SyntaxUI()
    form.show()
    exit(app.exec_())