import sys, errno
from PIL import Image
from PyQt5.QtWidgets import QMainWindow, QLabel, QMenu, QMenuBar, QAction
from PyQt5.QtGui import QPixmap


def initUI(viewer):

    # Menu bar actions
    menu_bar_actions = {'File': {'Open': QAction('&Open...', viewer, shortcut='Ctrl+O', statusTip='Open file', triggered=viewer.open_image),  # TODO
                                 'Save': QAction('&Save', viewer, shortcut='Ctrl+S', statusTip='Save file', triggered=viewer.save_image),
                                 'SaveAs': QAction('Save &As...', viewer, shortcut='Ctrl+Shift+S', statusTip='Save file as...', triggered=viewer.save_as_image),
                                 'Exit': QAction('E&xit', viewer, shortcut='Ctrl+Q', statusTip='Exit application', triggered=viewer.close),
                                },
                        'Edit': {'Image Rotation': QAction('&Open...', viewer, shortcut='Ctrl+O', statusTip='Open file', triggered=viewer.open_image)  # TODO
                                },
                        'View': {
                                },
                        'Help': {
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
            print(menu, action)
            menus[menu].addAction(menu_bar_actions[menu][action])

    # Window properties
    viewer.setWindowTitle('Image & EXIF Viewer')
    viewer.resize(512, 256)

    return


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.imageArea = QLabel(self)
        path = 'test/nèreis_palamon_water_genasi_portrait.jpg'

        self.open_image(path)  # TODO metti in un menù

        initUI(self)



    def open_image(self, path):
        try:
            pixmap = QPixmap(path)
            self.imageArea.setPixmap(pixmap)  # TODO Apre un'immagine
            self.imageArea.setScaledContents(True)
        except IOError:
            print('')  # TODO Controlla qual è il codice di errore
            sys.exit(errno.EIO)

    def save_image(self):
        print('save')
        return

    def save_as_image(self):
        print('save_as')
        return
