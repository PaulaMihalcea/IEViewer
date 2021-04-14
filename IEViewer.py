import sys, errno
import webbrowser
from PIL import Image, ImageQt, ExifTags
from PyQt5.QtCore import Qt, QEvent, QRect, QAbstractTableModel, QAbstractItemModel
from PyQt5.QtGui import QPixmap, QImage, QTransform, QMouseEvent, QStatusTipEvent, QColor, QPalette, QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QMenu, QMenuBar, QAction, QFileDialog, QMessageBox, QSizePolicy, QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QScrollArea, QTableView, QTableWidget, QFrame, QTableWidgetItem, QHeaderView, QToolBar
from view import ExifWidget, ImageWidget, StatusBar, MenuBar
from model import processGPSData


def initMenuBar(viewer):

    menu_bar = MenuBar(viewer)

    viewer.setMenuBar(menu_bar)

    imageRotationMenu = menu_bar.menus['edit']['ir_submenu_']
    viewMenu = menu_bar.menus['view']['menu_']
    showEXIF = None

    return {'ImageRotation': imageRotationMenu, 'View': viewMenu, 'ShowEXIF': showEXIF}


def initStatusBar(viewer):
    status_bar = StatusBar()
    viewer.setStatusBar(status_bar)

    status_bar.update('Ready.')


def OpenLink(item):
    if 'http' in item.text():
        webbrowser.open(item.text())


# TODO
def getSidebar(exif):
    try:  # TODO Test behavior on images without EXIF data.
        exif_table = ExifWidget(exif)
        exif_table.exif_table.itemDoubleClicked.connect(OpenLink)
        return exif_table
    except (TypeError, ValueError):
        return None




def defaultLayout(viewer):  # TODO
    layout_h = QHBoxLayout()
    layout_v = QVBoxLayout()

    layout_v.setContentsMargins(0,0,0,0)
    layout_h.setContentsMargins(0,0,0,0)

    viewer.menuBar().setMinimumHeight(viewer.menuBar().height() / 3 * 2)
    viewer.menuBar().setMaximumHeight(viewer.menuBar().height() / 3 * 2)

    layout_v.addWidget(viewer.menuBar())
    layout_v.addWidget(viewer.toolbar)

    #layout_h.addWidget(viewer.image_area)
    layout_v.addWidget(viewer.image_area)

    #widget = QWidget()
    #widget.setLayout(layout_v)

    #viewer.setCentralWidget(widget)
    viewer.setLayout(layout_v)
    viewer.setCentralWidget(viewer.image_area)

    viewer.layout_type = 'default'

    return


def createToolbar(viewer):

    openAction = QAction('&Open...', viewer, shortcut='Ctrl+O', statusTip='Open file.', triggered=viewer.open_image)

    active = True
    openAction.setIcon(QIcon("icons/open.png") if active else QIcon("icons/info.png"))

    saveAction = QAction(QIcon('icons/save.png'), "&Save", viewer)
    exifAction = QAction('Show &EXIF', viewer, shortcut='I', statusTip='Show EXIF data for the current image.', triggered=viewer.show_exif, checkable=True)
    exifAction.setIcon(QIcon('icons/exif.png'))
    #exifAction.setEnabled(False)  # TODO

    copyAction = QAction(QIcon(":edit-copy.svg"), "&Copy", viewer)
    pasteAction = QAction(QIcon(":edit-paste.svg"), "&Paste", viewer)
    cutAction = QAction(QIcon(":edit-cut.svg"), "C&ut", viewer)

    fileToolBar = QToolBar()
    fileToolBar.addAction(openAction)
    fileToolBar.addAction(saveAction)
    fileToolBar.addAction(exifAction)

    viewer.toolbar = viewer.addToolBar(fileToolBar)

    return


def exifLayout(viewer):  # TODO
    viewer.sidebar = getSidebar(viewer.exif)

    layout_h = QHBoxLayout()
    layout_v = QVBoxLayout()

    layout_v.setContentsMargins(0,0,0,0)
    layout_h.setContentsMargins(0,0,0,0)
    #layout_v.setSpacing(0)  # TODO È lo spazio a sinistra della sidebar

    viewer.menuBar().setMinimumHeight(viewer.menuBar().height() / 3 * 2)

    layout_v.addWidget(viewer.menuBar())
    layout_v.addWidget(viewer.toolbar)

    #viewer.sidebar.show()

    layout_h.addWidget(viewer.sidebar)
    #layout_h.addWidget(viewer.image_area)

    layout_v.addLayout(layout_h)

    #viewer.setLayout(layout_v)
    #viewer.setCentralWidget(viewer.image_area)

    widget = QWidget()
    widget.setLayout(layout_v)

    viewer.setCentralWidget(widget)

    #layout_h.addWidget(viewer.sidebar)



    viewer.layout_type = 'exif'

    return


def initImageArea(viewer):
    # Image area creation and properties
    viewer.image_area = QLabel(viewer)  # Create image area as a label
    viewer.image_area.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)  # Allow complete control over resizing the window (Expanding does not allow resizing to a smaller size)
    viewer.image_area.setScaledContents(False)  # Avoid stretching the image
    viewer.image_area.setAlignment(Qt.AlignCenter)  # Center image in the window area
    viewer.image_area.setMouseTracking(True)  # Get mouse position in image  # TODO

    return

#TODO ############################################
class EXIFViewer(QMainWindow):
    def __init__(self, viewer):
        super().__init__()  # Initialize base class

        # Window properties
        self.setWindowTitle('EXIF data - ' + viewer.filename)  # Window title (the one in the title bar)
        self.resize(512, 256)  # These dimensions should be fine for most displays



class ImageViewer(QMainWindow):  # Image viewer main class
    def show_exif(self):
        if self.disabledMenus['View'].isEnabled():
            if self.layout_type != 'exif':
                exifLayout(self)
            elif self.disabledMenus['ShowEXIF'].isChecked():
                self.sidebar.show()
            else:
                self.sidebar.hide()
        return


    # __init__
    # Constructor; initializes the main window object (the image viewer)
    def __init__(self):
        super().__init__()  # Initialize base class

        self.exif = None
        createToolbar(self)

        self.disabledMenus = initMenuBar(self)  # Initialize menu bar
        initImageArea(self)  # Initialize image area
        defaultLayout(self)


        # Window properties
        self.setWindowTitle('IEViewer')  # Window title (the one in the title bar)
        self.resize(512, 256)  # These default dimensions should be fine for most displays
        initStatusBar(self)  # Initialize status bar

    def event(self, e):  # TODO
        if e.type() == QEvent.StatusTip:
            if e.tip() == '':
                e = QStatusTipEvent('Ready.')
        return super().event(e)

    # eventFilter
    # Event handler override needed to maintain the image aspect ratio correct when scaling the window
    # And also to show current mouse position in the status bar
    def eventFilter(self, widget, event):
        # Window resize
        if event.type() == QEvent.Resize and widget is self.image_area:  # The resizing filter is only applied to the image area label
            self.image_area.setPixmap(self.image_area.pixmap.scaled(self.image_area.width(), self.image_area.height(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
            # Update new dimensions for later use
            self.image_area.w = self.image_area.width()
            #print(self.image_area.pixmap.width())
            self.image_area.h = self.image_area.height()
            return True

        # Mouse tracking
        if event.type() == QEvent.MouseMove and event.buttons() == Qt.NoButton:  # TODO
            #print(self.image_area.pixmap.rect())
            posX = int(event.pos().x() - (self.width() + self.image_area.w) / 2 + self.image_area.w)
            #print(event.pos().x(), self.width(), self.image_area.w)
            if posX >= 0 and posX <= self.image_area.w:
                self.statusBar().showMessage(str(posX) + ', ' + str(event.pos().y()) + 'px')
            else:
                self.statusBar().showMessage('Ready.')

        return QMainWindow.eventFilter(self, widget, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right and not callable(self.image_area.pixmap):
            self.rotateImage90C()
        if event.key() == Qt.Key_Left and not callable(self.image_area.pixmap):
            self.rotateImage90CC()

    # openImage
    # Open an image. Triggered from the "File" menu "Open..." button
    def open_image(self):
        # Open dialog to choose an image file (return an absolute path to the image)
        self.image_path = QFileDialog.getOpenFileName(self, 'Open', '', 'Image Files (*.bmp; *.gif; *.jpg; *.jpeg; *.png; *.pbm; *.pgm; *.ppm; *.xbm; *.xpm)')[0]  # By omitting the directory argument (empty string, ''), the dialog should remember the last directory (depends on operating system)

        # Get file name from the absolute image path
        self.filename = self.image_path.split('/')
        self.filename = self.filename[len(self.filename)-1]

        if self.image_path:  # Only continues if a file has been chosen; if the user chose "Cancel" in the previous dialog, the program just returns to its default state
            # Load image and EXIF data
            try:
                self.image = Image.open(self.image_path)  # Load PIL image
            except IOError:
                QMessageBox.information(self, 'IEViewer', 'Could not open "{}". \nInvalid file or format not supported.'.format(self.filename))  # TODO unisci messaggio errore (è duplicato)
                return

            self.exif = {ExifTags.TAGS[k]: v for k, v in self.image._getexif().items() if k in ExifTags.TAGS }
            self.exif = processGPSData(self.exif)
            self.sidebar = getSidebar(self.exif)
            self.image = ImageQt.ImageQt(self.image)  # Convert PIL image to a Qt image

            # Get original image size (dimensions are equal to zero for invalid image files)
            w = self.image.width()
            h = self.image.height()

            # Check that image is valid
            if self.image.isNull() or w == 0 or h == 0:
                QMessageBox.information(self, 'IEViewer', 'Could not open "{}". \nInvalid file or format not supported.'.format(self.filename))
                return

            # Recalculate image dimensions so as to have a maximum dimension (height or width) of 512 pixels
            if w >= h and w > 512:
                new_w = 512
                new_h = int(512 * h / w)
            elif h >= w and h > 512:
                new_w = int(512 * w / h)
                new_h = 512
            else:
                new_w = w
                new_h = h

            # Store new dimensions for later use
            self.image_area.w = new_w
            self.image_area.h = new_h

            # Resize image area and window
            self.image_area.resize(new_w, self.menuBar().height() + self.statusBar().height() + new_h)
            if new_w < 280:  # Set a minimum window width so as to correctly display the window title and menu bar; 280px should be good
                self.resize(280, self.menuBar().height() + self.statusBar().height() + new_h)
            else:
                self.resize(new_w, self.menuBar().height() + self.statusBar().height() + new_h)

            # Add pixmap from image and resize it accordingly
            pixmap = QPixmap.fromImage(self.image).scaled(new_w, new_h, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
            self.image_area.setPixmap(pixmap)
            self.image_area.pixmap = QPixmap(pixmap)
            self.image_area.installEventFilter(self)  # Install the new event handler

            # Activate disabled menus
            for key in self.disabledMenus:
                self.disabledMenus[key].setDisabled(False)
            # addDisabledSubmenus(self)  # TODO

            # Update window title (the one in the title bar)
            self.setWindowTitle('IEViewer - ' + self.filename)

        return

    def close_image(self):
        print('close image')
        self.setWindowTitle('IEViewer')  # Update window title (the one in the title bar)
        return

    def exit(self):
        print('exit program has not been implemented yet')
        return

    # saveImage
    def save_image(self):  # TODO
        print('save')
        return

    def save_as_image(self):  # TODO
        print('save_as')
        return

    # rotateImage180
    # Rotate image by 180 degrees. Triggered from the "Edit" menu "Image Rotation" button
    def rotateImage180(self):
        # Get original pixmap
        pixmap = self.image_area.pixmap
        # Transform and update pixmap
        pixmap = pixmap.transformed(QTransform().rotate(180), Qt.SmoothTransformation).scaled(self.image_area.w, self.image_area.h, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.image_area.setPixmap(pixmap)
        self.image_area.pixmap = QPixmap(pixmap)
        return

    # rotateImage90C
    # Rotate image by 90 degrees (clockwise). Triggered from the "Edit" menu "Image Rotation" button
    def rotateImage90C(self):  # TODO L'immagine è sfocata dopo averla rigirata una volta (la rimpicciolisce e poi non la riporta più all'originale)
        # Get original pixmap
        pixmap = self.image_area.pixmap
        # Transform and update pixmap
        pixmap = pixmap.transformed(QTransform().rotate(90), Qt.SmoothTransformation).scaled(self.image_area.w, self.image_area.h, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.image_area.setPixmap(pixmap)
        self.image_area.pixmap = QPixmap(pixmap)
        return

    # rotateImage90CC
    # Rotate image by 90 degrees (counter clockwise). Triggered from the "Edit" menu "Image Rotation" button
    def rotateImage90CC(self):  # TODO L'immagine è sfocata dopo averla rigirata una volta (la rimpicciolisce e poi non la riporta più all'originale)
        # Get original pixmap
        pixmap = self.image_area.pixmap
        # Transform and update pixmap
        pixmap = pixmap.transformed(QTransform().rotate(-90), Qt.SmoothTransformation).scaled(self.image_area.w, self.image_area.h, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.image_area.setPixmap(pixmap)
        self.image_area.pixmap = QPixmap(pixmap)
        return

    def reset_image(self):
        print('reset image')
        return

    def about(self):  # TODO
        print('about')
        return
