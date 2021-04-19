import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from model import ImageModel
from view import View
from controller import Controller


def main(terminal_flag):
    """Main program."""
    # Create PyQt5 application
    app = QApplication(sys.argv)  # Note: There must be exactly one instance of QApplication active at a time
    app.setWindowIcon(QIcon('icons/ieviewer.png'))  # Set program icon

    # Create model, view and controller
    model = ImageModel(terminal_flag)
    view = View(model)
    controller = Controller(model, view)

    # Start main window
    main_window = controller.get_main_window()
    main_window.show()

    sys.exit(app.exec_())


# Determine if the script has been run from the terminal or an IDE.
# Needed because it seems that PIL's _getexif() function behaves differently according to these cases, returning data in a different format.
# Failing to acknowledge this fact will result in a crash.
if sys.stdin.isatty():  # Terminal
    main(True)
else:  # IDE
    main(False)
