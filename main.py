from PyQt4.QtGui import QApplication
from sys import argv, exit
from telegram import Bot
# import RPI
from Syntax_UI import SyntaxUI

if __name__ == "__main__":
    bot = Bot(token='Your Token', base_url="https://tapi.bale.ai/")

    app = QApplication(argv)
    form = SyntaxUI(bot)
    form.show()
    exit(app.exec_())