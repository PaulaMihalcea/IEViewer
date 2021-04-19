###
### This work is licensed under a Creative Commons “Attribution-NonCommercial-ShareAlike 4.0 International” license.
###













import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from model import ImageModel
from view import View
from controller import Controller


def main(terminal_flag):
    app = QApplication(sys.argv)  # Note: There must be exactly one instance of QApplication active at a time
    app.setWindowIcon(QIcon('icons/ieviewer.png'))

    model = ImageModel(terminal_flag)
    view = View(model)

    controller = Controller(model, view)

    main_window = controller.get_main_window()
    main_window.show()

    sys.exit(app.exec_())


if sys.stdin.isatty():
    main(True)
else:
    main(False)
