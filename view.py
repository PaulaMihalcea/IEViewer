from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap, QTransform, QStatusTipEvent
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from observer import Subject
from widgets import ExifWidget, ImageWidget, StatusBar, MenuBar, ToolBar, Layout, AboutWidget


class View(Subject, QMainWindow):
    """Main window class, and the View of the MVC pattern.

    Attributes:
        model: The model of the MVC pattern.
        menu_bar: A menu bar derived from QMenuBar.
        tool_bar: A tool bar derived from QToolBar.
        exif_area: The widget containing any available EXIF data.
        image_area: The widget containing the displayed image.
        status_bar: A status bar derived from QStatusBar.
        about: The classic "About" informative widget (actually a new, separate window).
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
        self.status_bar = StatusBar()
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

        # Install additional event filters
        self.image_area.installEventFilter(self)

    def set_window_properties(self):
        """Sets some main window properties."""
        self.statusBar()
        self.setStatusTip('Ready.')
        self.setWindowTitle('IEViewer')  # Window title (the one in the title bar)
        self.resize(512, 256)  # These default dimensions should be fine for most displays

    def get_open_file_dialog(self, caption, filter):
        """Opens an "Open File" dialog and returns a file path. If no file has been selected and the user has pressed "Cancel" or closed the dialog, then it returns None."""
        file_path, _ = QFileDialog.getOpenFileName(caption=caption, directory='', filter=filter)
        if file_path == '':
            return None
        else:
            return file_path

    def get_save_file_dialog(self, caption, filter):
        """Opens a "Save As" dialog and returns a file path and format. If no name has been entered and the user has pressed "Cancel" or closed the dialog, then it returns None."""
        file_path, format = QFileDialog.getSaveFileName(caption=caption, directory='', filter=filter)  # By omitting the directory argument (empty string, ''), the dialog should remember the last directory (depends on operating system)
        if file_path == '':
            return None, None
        else:
            format = format.split(' ')
            return file_path, format[0]

    def show_message_box(self, title, text, icon=QMessageBox.Information):
        """Opens a simple message box window, with some text and a customizable icon."""
        info_box = QMessageBox(self)

        if icon is not None:
            info_box.setIcon(icon)
        info_box.setWindowTitle(title)
        info_box.setText(text)

        info_box.show()

    def event(self, e):
        """Defines the default status bar message (when nothing else is displayed)."""
        if e.type() == QEvent.StatusTip:
            if e.tip() == '':
                e = QStatusTipEvent('Ready.')
        return super().event(e)

    def open(self):
        """Only needed to notify observers (i.e. the controller) that they should load an image."""
        self.set_state('open')

    def load_image(self):
        """Displays the image contained in the model."""
        # Get original image dimensions
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

        # Generate and set a pixmap from the image
        self.image_area.set_image(self.model.image, w, h)

        # Resize the window and pixmap (generated from the image),
        # so as to display correctly the window title, menu bar and image (actually, its pixmap)
        #
        # The diff parameter is another piece of PyQt5 magic.
        # Without it, an image larger than 512 pixels might be displayed smaller
        # than the maximum 512 that it has been resized to
        # (despite having been resized to 512 pixels).

        diff = 130  # This value is good for both Windows 10 and Ubuntu 20.04
        if w < 280:  # Again, this should suffice for both OSs
            self.resize(280, h + diff)
        else:
            self.resize(w, h + diff)
        self.image_area.pixmap.scaled(w, h)

        # Add EXIF data from the model
        self.exif_area.load_exif()

        # Update window title
        self.setWindowTitle('IEViewer - ' + self.model.filename)

        # Enable menus
        self.menu_bar.enable_widgets()

    def save(self):
        """Saves the modified image. Uses the stored original image, not the modified version currently displayed in the window."""
        self.model.set_image(self.model.image.transformed(QTransform().rotate(self.image_area.rot), Qt.SmoothTransformation))
        self.set_state('save')

    def saveas(self):
        """Saves the modified image with another name. Uses the stored original image, not the modified version currently displayed in the window."""
        self.model.set_image(self.model.image.transformed(QTransform().rotate(self.image_area.rot), Qt.SmoothTransformation))
        self.set_state('saveas')

    def eventFilter(self, widget, event):
        """Adds new behavior for certain events."""

        # Resize event
        # Or what should happen to the image widget when the user resizes the main window
        if event.type() == QEvent.Resize and widget is self.image_area and self.image_area.pixmap is not None:
            self.image_area.setPixmap(QPixmap.fromImage(self.model.modified_image).scaled(self.image_area.width(), self.image_area.height(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
            # Update new dimensions for later use
            self.image_area.w = self.image_area.width()
            self.image_area.h = self.image_area.height()
            return True

        return QMainWindow.eventFilter(self, widget, event)

    def close(self):
        """Closes an image."""
        self.set_state('close')

        # Clear image area widget and adjust layout
        self.image_area.clear_image()
        self.exif_area = ExifWidget(self)
        self.setCentralWidget(Layout(self).central_widget)

        # Disable unavailable menus
        self.menu_bar.disable_widgets()

        # Hide EXIF area (if visible) and show blank image widget
        self.exif_area.hide()
        self.image_area.show()

        # Update window title
        self.setWindowTitle('IEViewer')

    def exit(self):
        """Only needed to notify observers (i.e. the controller) that they should exit the application."""
        self.set_state('exit')

    def rotate(self, degree):
        """Base function for rotation.

        Subsequent rotation functions are only needed as hooks for menu actions; actual rotations happen here.
        Here, the View directly changes the Model. Arguably, this is a violation of the MVC pattern. It happens that, for some reason, returning a reference to the rotated image to the Controller in order to have the Controller itself change the Model does not work, probably because it only returns a reference and not a copy of the rotated image. PyQt5 does not allow deep copies of its objects, so the following seems to be the only way to make it work.
        """
        self.model.set_modified_image(self.model.image.transformed(QTransform().rotate(self.image_area.rot+degree), Qt.SmoothTransformation))  # Rotate image
        self.image_area.set_image(self.model.modified_image, self.image_area.w, self.image_area.h)  # Display rotated image
        self.image_area.rot += degree  # Update rotation history

    def rotate180(self):
        """Rotate the displayed image by 180 degrees."""
        self.rotate(180)

    def rotate90c(self):
        """Rotate the displayed image by 90 degrees clock wise."""
        self.rotate(90)

    def rotate90cc(self):
        """Rotate the displayed image by 90 degrees clock wise."""
        self.rotate(-90)

    def reset_image(self):
        """Reset the displayed image to its original orientation."""
        self.rotate(-self.image_area.rot)

    def show_exif(self):
        """Display EXIF data (and at the same time hide the image)."""
        if self.exif_area.isHidden():
            self.image_area.hide()
            self.exif_area.show()
        else:
            self.image_area.show()
            self.exif_area.hide()

    def about(self):
        """Display info about the program."""
        self.about.show()
