import sys, errno
import webbrowser
from PIL import Image, ImageQt, ExifTags
from PyQt5.QtCore import Qt, QEvent, QRect, QAbstractTableModel, QAbstractItemModel
from PyQt5.QtGui import QPixmap, QImage, QTransform, QMouseEvent, QStatusTipEvent, QColor, QPalette, QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QMenu, QMenuBar, QAction, QFileDialog, QMessageBox, QSizePolicy, QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QScrollArea, QTableView, QTableWidget, QFrame, QTableWidgetItem, QHeaderView, QToolBar, QLayout
from view_elements import ExifWidget, ImageWidget, StatusBar, MenuBar, ToolBar, Layout
from model import processGPSData


class ImageViewer(QMainWindow):
    """Main window class.

    Attributes:
        model: The model of the MVC pattern.
        menus: A dictionary containing the main menus (those listed in the bar), individually accessible,
                as well as another dictionary containing their relative actions and separators.
    """
    def __init__(self, model):
        """Inits the class."""
        super().__init__()

        # Set model
        self.model = model

        # Create interface elements
        self.menu_bar = MenuBar(self)
        self.tool_bar = ToolBar(self)
        self.exif_area = ExifWidget(self)
        self.image_area = ImageWidget(self)
        self.status_bar = StatusBar(self)

        # Disable unavailable elements of the interface
        self.menu_bar.disable_widgets()

        # Set layout
        self.setCentralWidget(Layout(self).central_widget)

        # Set window properties
        self.set_window_properties()

    def set_window_properties(self):
        """Sets some main window properties (title and size)."""
        self.setWindowTitle('IEViewer')  # Window title (the one in the title bar)
        self.resize(512, 256)  # These default dimensions should be fine for most displays

    def open(self):
        print('ciao')

    def save(self):
        print('ciao')

    def saveas(self):
        print('ciao')

    def close(self):
        if self.image_area.pixmap() is not None:
            print('ciao')

    def exit(self):
        print('ciao')

    def rotate180(self):
        print('ciao')

    def rotate90c(self):
        print('ciao')

    def rotate90cc(self):
        print('ciao')

    def reset_image(self):
        print('ciao')

    def prev_image(self):
        print('ciao')

    def next_image(self):
        print('ciao')

    def show_exif(self):
        print('ciao')

    def about(self):
        print('ciao')
