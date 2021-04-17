import sys, errno
import webbrowser
from PIL import Image, ImageQt, ExifTags
from PyQt5.QtCore import Qt, QEvent, QRect, QAbstractTableModel, QAbstractItemModel
from PyQt5.QtGui import QPixmap, QImage, QTransform, QMouseEvent, QStatusTipEvent, QColor, QPalette, QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QMenu, QMenuBar, QAction, QFileDialog, QMessageBox, QSizePolicy, QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QScrollArea, QTableView, QTableWidget, QFrame, QTableWidgetItem, QHeaderView, QToolBar, QLayout
from widgets import ExifWidget, ImageWidget, StatusBar, MenuBar, ToolBar, Layout
from observer import Subject


class View(Subject, QMainWindow):
    """Main window class.

    Attributes:
        model: The model of the MVC pattern.
        menus: A dictionary containing the main menus (those listed in the bar), individually accessible,
                as well as another dictionary containing their relative actions and separators.
    """
    def __init__(self, model):
        """Inits the class."""
        Subject.__init__(self)
        QMainWindow.__init__(self)

        # TODO
        self.set_state('no_image')

        # Set model
        self.model = model

        # Create interface elements
        self.menu_bar = MenuBar(self)
        self.tool_bar = ToolBar(self)
        self.exif_area = ExifWidget(self)
        self.image_area = ImageWidget(self)
        self.status_bar = StatusBar(self)

        # Disable GUI elements that are unavailable when no image is opened
        self.menu_bar.disable_widgets()
        self.exif_area.hide()

        # Set layout
        self.setCentralWidget(Layout(self).central_widget)

        # Set window properties
        self.set_window_properties()

    def set_window_properties(self):
        """Sets some main window properties."""
        self.setWindowTitle('IEViewer')  # Window title (the one in the title bar)
        self.resize(512, 256)  # These default dimensions should be fine for most displays

    def get_file_dialog(self, caption, filter):
        file_path, _ = QFileDialog.getOpenFileName(caption=caption, directory='', filter=filter)  # By omitting the directory argument (empty string, ''), the dialog should remember the last directory (depends on operating system)
        if file_path == '':
            return None
        else:
            return file_path

    def show_message_box(self, title, text):
        info_box = QMessageBox(self)
        info_box.setIcon(QMessageBox.Information)
        info_box.setWindowTitle(title)
        info_box.setText(text)

    def open(self):
        self.set_state('open')  # Load image
        self.menu_bar.enable_widgets()

    def load_image(self):
        width = self.model.image.width()
        height = self.model.image.height()

        # Recalculate image dimensions so as to have a maximum dimension (height or width) of 512 pixels
        if width >= height and width > 512:
            w = 512
            h = int(512 * height / width)
        elif height >= width and height > 512:
            w = int(512 * width / height)
            h = 512
        else:
            w = width
            h = height

        self.image_area.set_image(self.model.image, w, h)

        self.image_area.resize(self.image_area.w, self.menuBar().height() + self.statusBar().height() + self.image_area.h)
        if w < 280:  # Set a minimum window width so as to correctly display the window title and menu bar; 280px should be good
            self.resize(280, self.menuBar().height() + self.statusBar().height() + h)
        else:
            self.resize(w, self.menuBar().height() + self.statusBar().height() + h)

        # EXIF data
        self.exif_area.load_exif(self)

        # Update window title (the one in the title bar)
        self.setWindowTitle('IEViewer - ' + self.model.filename)

        # Subject state
        self.set_state('one_image')

    def save(self):
        self.set_state('save')

    def saveas(self):
        self.set_state('saveas')

    def close(self):
        self.set_state('close')
        self.setWindowTitle('IEViewer')
        self.image_area.clear_image()
        self.menu_bar.disable_widgets()

    def exit(self):
        self.set_state('exit')

    def rotate180(self):
        self.set_state('rotate180')

    def rotate90c(self):
        self.set_state('rotate90c')

    def rotate90cc(self):
        self.set_state('rotate90cc')

    def reset_image(self):
        self.set_state('reset_image')

    def prev_image(self):
        self.set_state('prev_image')

    def next_image(self):
        self.set_state('next_image')

    def show_exif(self):
        if self.exif_area.isHidden():
            self.exif_area.show()
            self.image_area.hide()
        else:
            self.exif_area.hide()
            self.image_area.show()

    def about(self):
        self.set_state('about')
