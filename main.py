from PyQt4.QtGui import QApplication
from sys import argv, exit
from telegram import Bot
# import RPI
from Syntax_UI import SyntaxUI

if __name__ == "__main__":
    bot = Bot(token="Token")

    app = QApplication(argv)
    form = SyntaxUI()
    form.show()
    exit(app.exec_())