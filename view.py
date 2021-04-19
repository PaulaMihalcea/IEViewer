import sys, errno
import webbrowser
from PIL import Image, ImageQt, ExifTags
from PyQt5.QtCore import Qt, QEvent, QRect, QAbstractTableModel, QAbstractItemModel
from PyQt5.QtGui import QPixmap, QImage, QTransform, QMouseEvent, QStatusTipEvent, QColor, QPalette, QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QMenu, QMenuBar, QAction, QFileDialog, QMessageBox, QSizePolicy, QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QScrollArea, QTableView, QTableWidget, QFrame, QTableWidgetItem, QHeaderView, QToolBar, QLayout
from widgets import ExifWidget, ImageWidget, StatusBar, MenuBar, ToolBar, Layout, AboutWidget
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

        self.set_state('no_image')

        # Set model
        self.model = model

        # Create interface elements
        self.menu_bar = MenuBar(self)
        self.tool_bar = ToolBar(self)
        self.exif_area = ExifWidget(self)
        self.image_area = ImageWidget(self)
        self.status_bar = StatusBar(self)
        about_text = 'IEViewer 1.0' \
                     '<br><br>' \
                     'Copyright © 2021 by' \
                     '<br>' \
                     'Paula Mihalcea' \
                     '<br>' \
                     '<a href="mailto:paula.mihalcea@live.com">paula.mihalcea@live.com</a>' \
                     '<br><br>' \
                     'This program uses PyQt5, a comprehensive set of Python bindings for Qt v5. Qt is a set of cross-platform C++ libraries that implement high-level APIs for accessing many aspects of modern desktop and mobile systems.\n' \
                     '<br><br>' \
                     'PyQt5 is copyright © Riverbank Computing Limited. Its homepage is <a href="https://www.riverbankcomputing.com/software/pyqt/">https://www.riverbankcomputing.com/software/pyqt/</a>.' \
                     '<br><br>' \
                     'No genasi were harmed in the making of this application. <a href="https://www.dndbeyond.com/races/genasi#WaterGenasi">#GenasiLivesMatter#NereisThalian</a>'
        self.about = AboutWidget('About IEViewer', about_text, image_path='icons/about_img.png')

        # Disable GUI elements that are unavailable when no image is opened
        self.menu_bar.disable_widgets()
        self.exif_area.hide()

        # Set layout
        self.setCentralWidget(Layout(self).central_widget)

        # Set window properties
        self.set_window_properties()
        self.image_area.installEventFilter(self)

    def set_window_properties(self):
        """Sets some main window properties."""
        self.statusBar()
        self.setStatusTip('Ready.')
        self.setWindowTitle('IEViewer')  # Window title (the one in the title bar)
        self.resize(512, 256)  # These default dimensions should be fine for most displays

    def get_open_file_dialog(self, caption, filter):
        #  # TODOile_dialog = QFileDialog(self, caption=caption, directory='')
        #print(filter)
        #file_dialog.setNameFilters([filter])
        #file_dialog.setOption(QFileDialog.DontUseNativeDialog)
        file_path, _ = QFileDialog.getOpenFileName(caption=caption, directory='', filter=filter)  # By omitting the directory argument (empty string, ''), the dialog should remember the last directory (depends on operating system)
        if file_path == '':
            return None
        else:
            return file_path

    def get_save_file_dialog(self, caption, filter):
        file_path, _ = QFileDialog.getSaveFileName(caption=caption, directory='', filter=filter)  # By omitting the directory argument (empty string, ''), the dialog should remember the last directory (depends on operating system)
        if file_path == '':
            return None
        else:
            return file_path

    def show_message_box(self, title, text, icon=QMessageBox.Information):
        info_box = QMessageBox(self)
        if icon is not None:
            info_box.setIcon(icon)
        info_box.setWindowTitle(title)
        info_box.setText(text)
        info_box.show()

    def event(self, e):  # TODO
        if e.type() == QEvent.StatusTip:
            if e.tip() == '':
                e = QStatusTipEvent('Ready.')
        return super().event(e)

    def open(self):
        self.set_state('open')  # Load image

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

        #self.image_area.resize(self.image_area.w, self.menuBar().height() + self.statusBar().height() + self.image_area.h)  # TODO

        print('DIMENSIONS:', self.menu_bar.height())

        diff = 130  # TODO 112, nel widget 20
        if w < 280:  # Set a minimum window width so as to correctly display the window title and menu bar; 280px should be good
            self.resize(280, h + diff)
        else:
            self.resize(w, h + diff)

        self.image_area.pixmap.scaled(w, h)

        # EXIF data
        self.exif_area.load_exif()

        # Update window title (the one in the title bar)
        self.setWindowTitle('IEViewer - ' + self.model.filename)

    def save(self):
        self.model.set_image(self.model.image.transformed(QTransform().rotate(self.image_area.rot), Qt.SmoothTransformation))
        self.set_state('save')

    def saveas(self):
        self.model.set_image(self.model.image.transformed(QTransform().rotate(self.image_area.rot), Qt.SmoothTransformation))
        self.set_state('saveas')

    def eventFilter(self, widget, event):
        if event.type() == QEvent.Resize and widget is self.image_area and self.image_area.pixmap is not None:  # The resizing filter is only applied to the image area label
            self.image_area.setPixmap(QPixmap.fromImage(self.model.modified_image).scaled(self.image_area.width(), self.image_area.height(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
            # Update new dimensions for later use
            self.image_area.w = self.image_area.width()
            self.image_area.h = self.image_area.height()
            return True
        return QMainWindow.eventFilter(self, widget, event)

    def close(self):
        self.set_state('close')
        self.setWindowTitle('IEViewer')
        self.menu_bar.disable_widgets()
        self.image_area.clear_image()
        self.exif_area = ExifWidget(self)
        self.setCentralWidget(Layout(self).central_widget)
        self.exif_area.hide()
        self.image_area.show()

    def exit(self):
        self.set_state('exit')

    def rotate(self, degree):
        '''Here, the View directly changes the Model. Arguably, this is a violation of the MVC pattern. It happens though tha for some reason, returning (a reference to) the rotated image to the Controller in order to have it change the Model instead does not work, probably because it only returns a reference and not a copy of the rotated image. PyQt5 does not allow deep copies of its objects, so the following seems to be the only way to make it work.'''
        self.model.set_modified_image(self.model.image.transformed(QTransform().rotate(self.image_area.rot+degree), Qt.SmoothTransformation))
        self.image_area.set_image(self.model.modified_image, self.image_area.w, self.image_area.h)
        self.image_area.rot += degree

    def rotate180(self):
        self.rotate(180)

    def rotate90c(self):
        self.rotate(90)

    def rotate90cc(self):
        self.rotate(-90)

    def reset_image(self):
        self.rotate(-self.image_area.rot)

    def show_exif(self):
        if self.exif_area.isHidden():
            self.image_area.hide()
            self.exif_area.show()
        else:
            self.image_area.show()
            self.exif_area.hide()

    def about(self):
        self.about.show()
