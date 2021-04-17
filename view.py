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

        # Set model
        self.model = model

        # Create interface elements
        self.menu_bar = MenuBar(self)
        self.tool_bar = ToolBar(self)
        self.exif_area = ExifWidget(self)
        self.image_area = ImageWidget(self)
        self.status_bar = StatusBar(self)

        # Set layout
        self.setCentralWidget(Layout(self).central_widget)

        # Set window properties
        self.set_window_properties()

    def set_window_properties(self):
        """Sets some main window properties."""
        self.setWindowTitle('IEViewer')  # Window title (the one in the title bar)
        self.resize(512, 256)  # These default dimensions should be fine for most displays

    def get_file_dialog(self, caption, filter):
        file_path =  QFileDialog.getOpenFileName(caption=caption, directory='', filter=filter)[0]  # By omitting the directory argument (empty string, ''), the dialog should remember the last directory (depends on operating system)
        return file_path

    def show_message_box(self, title, text):
        info_box = QMessageBox(self)
        info_box.setIcon(QMessageBox.Information)
        info_box.setWindowTitle(title)
        info_box.setText(text)
        info_box.exec_()

    # eventFilter  # TODO documentazione
    # Event handler override needed to maintain the image aspect ratio correct when scaling the window
    # And also to show current mouse position in the status bar
    def eventFilter(self, widget, event):
        # Window resize
        if event.type() == QEvent.Resize and widget is self.image_area:  # The resizing filter is only applied to the image area label
            self.image_area.setPixmap(self.image_area.pixmap.scaled(self.image_area.width(), self.image_area.height(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
            # Update new dimensions for later use
            self.image_area.w = self.image_area.width()
            self.image_area.h = self.image_area.height()
            return True

        return QMainWindow.eventFilter(self, widget, event)

    def open(self):
        self.set_state('open')  # Load image

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

        # Store new dimensions for later use
        self.image_area.w = w
        self.image_area.h = h

        # Resize image area and window
        self.image_area.resize(w, self.menuBar().height() + self.statusBar().height() + h)
        if w < 280:  # Set a minimum window width so as to correctly display the window title and menu bar; 280px should be good
            self.resize(280, self.menuBar().height() + self.statusBar().height() + h)
        else:
            self.resize(w, self.menuBar().height() + self.statusBar().height() + h)

        # Add pixmap from image and resize it accordingly
        pixmap = QPixmap.fromImage(self.model.image).scaled(w, h, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.image_area.setPixmap(pixmap)
        self.image_area.pixmap = QPixmap(pixmap)
        self.image_area.installEventFilter(self)  # Install the new event handler

        # Update window title (the one in the title bar)
        self.setWindowTitle('IEViewer - ' + self.model.filename)



    def save(self):
        self.set_state('save')

    def saveas(self):
        self.set_state('saveas')

    def close(self):
        self.set_state('close')

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
        self.set_state('show_exif')

    def about(self):
        self.set_state('about')
