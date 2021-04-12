import sys, errno
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap, QImage, QTransform
from PyQt5.QtWidgets import QMainWindow, QLabel, QMenu, QMenuBar, QAction, QFileDialog, QMessageBox, QSizePolicy


def initMenuBar(viewer):
    # Actions
    actions = {'File': {'Open': QAction('&Open...', viewer, shortcut='Ctrl+O', statusTip='Open file', triggered=viewer.openImage),
                                 'Save': QAction('&Save', viewer, shortcut='Ctrl+S', statusTip='Save file', triggered=viewer.saveImage),  # TODO
                                 'SaveAs': QAction('Save &As...', viewer, shortcut='Ctrl+Shift+S', statusTip='Save file as...', triggered=viewer.save_as_image),  # TODO
                                 'Exit': QAction('E&xit', viewer, shortcut='Ctrl+Q', statusTip='Exit application', triggered=viewer.close),
                                 },
                        'Edit': {
                                },
                        'View': {
                                },
                        'Help': {'About': QAction('&About IEViewer', viewer, statusTip='Show version and license information', triggered=viewer.about)  # TODO
                                },
    }

    # Menus
    menus = {'File': QMenu('&File', viewer),  # File menu
             'Edit': QMenu('&Edit', viewer),  # Edit menu
             'View': QMenu('&View', viewer),  # View menu
             'Help': QMenu('&Help', viewer),  # Help menu
             }

    # Actual menu bar creation
    menu_bar = QMenuBar(viewer)
    viewer.setMenuBar(menu_bar)

    # Menu and action assignment
    for menu in menus:
        viewer.menuBar().addMenu(menus[menu])
        for action in actions[menu]:
            menus[menu].addAction(actions[menu][action])

    # Add submenus
    imageRotationMenu = menus['Edit'].addMenu('Ima&ge Rotation')
    imageRotationMenu.addAction(QAction('&180°', viewer, shortcut='Ctrl+1', statusTip='Rotate image by 180 degrees', triggered=viewer.rotateImage180))
    imageRotationMenu.addAction(QAction('&90° Clockwise', viewer, shortcut='Ctrl+2', statusTip='Rotate image by 90 degrees (clockwise)', triggered=viewer.rotateImage90C))
    imageRotationMenu.addAction(QAction('&90° Counter Clockwise', viewer, shortcut='Ctrl+3', statusTip='Rotate image by 90 degrees (counter clockwise)', triggered=viewer.rotateImage90CC))

    return


def initImageArea(viewer):
    # Image area
    viewer.image_area = QLabel(viewer)  # Create image area as a label
    viewer.image_area.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)  # Allow complete control over resizing the window (Expanding does not allow resizing to a smaller size)
    viewer.image_area.setScaledContents(False)  # Avoid stretching the image
    viewer.image_area.setAlignment(Qt.AlignCenter)  # Center image in the window area

    viewer.setCentralWidget(viewer.image_area)  # Set the image area as the central widget

    # Window properties
    viewer.setWindowTitle('IEViewer')  # Window title (the one in the title bar)
    viewer.resize(512, 256)  # These dimensions should be fine for most displays

    return


class ImageViewer(QMainWindow):  # Image viewer main class
    # __init__
    # Constructor; initializes the main window object (the image viewer)
    def __init__(self):
        super().__init__()  # Initialize base class

        initMenuBar(self)  # Initialize menu bar
        initImageArea(self)  # Initialize image area

    # eventFilter
    # Event handler override needed to maintain the image aspect ratio correct when scaling the window
    def eventFilter(self, widget, event):
        if event.type() == QEvent.Resize and widget is self.image_area:  # The resizing filter is only applied to the image area label
            self.image_area.setPixmap(self.image_area.pixmap.scaled(self.image_area.width(), self.image_area.height(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
            return True
        return QMainWindow.eventFilter(self, widget, event)

    # openImage
    # Open an image. Triggered from the "File" menu "Open..." button
    def openImage(self):
        # Open dialog to choose an image file (return an absolute path to the image)
        image_path = QFileDialog.getOpenFileName(self, 'Open', '', 'Image Files (*.bmp; *.gif; *.jpg; *.jpeg; *.png; *.pbm; *.pgm; *.ppm; *.xbm; *.xpm)')[0]  # By omitting the directory argument (empty string, ''), the dialog should remember the last directory (depends on operating system)

        # Get file name from the absolute image path
        filename = image_path.split('/')
        filename = filename[len(filename)-1]

        if image_path:  # Only continues if a file has been chosen; if the user chose "Cancel" in the previous dialog, the program just returns to its default state
            # Load image
            image = QImage(image_path)

            # Get original image size (dimensions are equal to zero for invalid image files)
            w = image.width()
            h = image.height()

            # Check that image is valid
            if image.isNull() or w == 0 or h == 0:
                QMessageBox.information(self, 'IEViewer', 'Could not open "{}". \nInvalid file or format not supported.'.format(filename))
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

            # Resize image area and window
            self.image_area.resize(new_w, self.menuBar().height() + new_h)

            if new_w < 220:  # Set a minimum window width so as to correctly display the window title and menu bar; 220px should be good
                self.resize(220, self.menuBar().height() + new_h)
            else:
                self.resize(new_w, self.menuBar().height() + new_h)

            # Add pixmap from image and resize it accordingly
            pixmap = QPixmap.fromImage(image).scaled(new_w, new_h, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)

            self.image_area.setPixmap(pixmap)
            self.image_area.pixmap = QPixmap(pixmap)
            self.image_area.installEventFilter(self)  # Install the new event handler

        return

    # saveImage
    def saveImage(self):  # TODO
        print('save')
        return

    def save_as_image(self):  # TODO
        print('save_as')
        return

    # rotateImage180
    # Rotate image by 180 degrees. Triggered from the "Edit" menu "Image Rotation" button
    def rotateImage180(self):
        pixmap = self.image_area.pixmap.transformed(QTransform().rotate(180), Qt.SmoothTransformation)
        self.image_area.setPixmap(pixmap)
        self.image_area.pixmap = QPixmap(pixmap)
        return

    # rotateImage90C
    # Rotate image by 90 degrees (clockwise). Triggered from the "Edit" menu "Image Rotation" button
    def rotateImage90C(self):  # TODO
        print('rotate')
        return

    # rotateImage90CC
    # Rotate image by 90 degrees (counter clockwise). Triggered from the "Edit" menu "Image Rotation" button
    def rotateImage90CC(self):  # TODO
        print('rotate')
        return

    def about(self):  # TODO
        print('about')
        return
