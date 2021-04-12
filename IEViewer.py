import sys, errno
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QLabel, QMenu, QMenuBar, QAction, QFileDialog, QMessageBox, QSizePolicy





def initUI(viewer):  # TODO Metti ogni categoria come funzione a sé

    # Menu bar actions
    menu_bar_actions = {'File': {'Open': QAction('&Open...', viewer, shortcut='Ctrl+O', statusTip='Open file', triggered=viewer.open_image),  # TODO
                                 'Save': QAction('&Save', viewer, shortcut='Ctrl+S', statusTip='Save file', triggered=viewer.save_image),  # TODO
                                 'SaveAs': QAction('Save &As...', viewer, shortcut='Ctrl+Shift+S', statusTip='Save file as...', triggered=viewer.save_as_image),  # TODO
                                 'Exit': QAction('E&xit', viewer, shortcut='Ctrl+Q', statusTip='Exit application', triggered=viewer.close),
                                },
                        'Edit': {'Image Rotation': QAction('Ima&ge Rotation', viewer, shortcut='Ctrl+R', statusTip='Open file', triggered=viewer.rotate_image)  # TODO
                                },
                        'View': {
                                },
                        'Help': {'About': QAction('&About IEViewer', viewer, statusTip='Show version and license information', triggered=viewer.about)  # TODO
                                },
    }

    # Menu bar
    menus = {'File': QMenu('&File', viewer),  # File menu
             'Edit': QMenu('&Edit', viewer),  # Edit menu
             'View': QMenu('&View', viewer),  # View menu
             'Help': QMenu('&Help', viewer),  # Help menu
             }

    menu_bar = QMenuBar(viewer)
    viewer.setMenuBar(menu_bar)

    for menu in menus:
        viewer.menuBar().addMenu(menus[menu])
        for action in menu_bar_actions[menu]:
            menus[menu].addAction(menu_bar_actions[menu][action])

    # Image area
    viewer.image_area = QLabel(viewer)
    viewer.image_area.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)  # Allows complete control over resizing the window
    viewer.image_area.setScaledContents(False)
    viewer.setCentralWidget(viewer.image_area)  # TODO

    # Window properties
    viewer.setWindowTitle('IEViewer')
    viewer.resize(512, 256)

    return


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        initUI(self)




    def eventFilter(self, widget, event):
        if event.type() == QEvent.Resize and widget is self.image_area:
            self.image_area.setPixmap(self.image_area.pixmap.scaled(self.image_area.width(), self.image_area.height(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
            return True
        return QMainWindow.eventFilter(self, widget, event)

    def open_image(self):
        image_path = QFileDialog.getOpenFileName(self, 'Open', '', 'Image Files (*.bmp; *.gif; *.jpg; *.jpeg; *.png; *.pbm; *.pgm; *.ppm; *.xbm; *.xpm)')[0]  # By omitting the directory argument (empty string, ''), the dialog remembers the last directory

        filename = image_path.split('/')
        filename = filename[len(filename)-1]

        if image_path:
            # Load image
            image = QImage(image_path)

            # Get original image size (dimensions are equal to zero for invalid image files)
            w = image.width()
            h = image.height()

            # Check that image is valid
            if image.isNull() or w == 0 or h == 0:
                QMessageBox.information(self, 'IEViewer', 'Could not open "{}". \nInvalid file or format not supported.'.format(filename))
                return

            # Recalculate image dimensions so to have a maximum dimension (height or width) of 512 pixels
            if w >= h and w > 512:
                new_w = 512
                new_h = int(512 * h / w)
            elif h >= w and h > 512:
                new_w = int(512 * w / h)
                new_h = 512
            else:
                new_w = w
                new_h = h

            # Resize window
            if new_w < 220:  # Set a minimum window width so as to correctly display the window title and menu bar
                self.image_area.resize(new_w, self.menuBar().height() + new_h)
                self.resize(220, self.menuBar().height() + new_h)
            else:
                self.image_area.resize(new_w, self.menuBar().height() + new_h)
                self.resize(new_w, self.menuBar().height() + new_h)

            # Add pixmap from image and resize it accordingly
            pixmap = QPixmap.fromImage(image).scaled(new_w, new_h, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
            self.image_area.setPixmap(pixmap)  # pixmap() is the corresponding getter
            #self.image_area._pixmap = self.image_area.setPixmap(pixmap)

            self.image_area.pixmap = QPixmap(pixmap)
            self.image_area.installEventFilter(self)

            #self.image_area.pixmap = QPixmap(self.image_area.pixmap)



        return

    def save_image(self):  # TODO
        print('save')
        return

    def save_as_image(self):  # TODO
        print('save_as')
        return

    def rotate_image(self):  # TODO
        print('rotate')
        return

    def about(self):  # TODO
        print('about')
        return
