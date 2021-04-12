import sys, errno
from PIL import Image
from PyQt5.QtWidgets import QMainWindow, QLabel, QMenu, QMenuBar, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage


def initUI(viewer):

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
    viewer.image_area = QLabel()

    # Window properties
    viewer.setWindowTitle('IEViewer')
    viewer.resize(512, 256)

    return


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        initUI(self)

    def open_image(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        image_path = QFileDialog.getOpenFileName(self, 'Open', '', 'Image Files (*.bmp; *.gif; *.jpg; *.jpeg; *.png; *.pbm; *.pgm; *.ppm; *.xbm; *.xpm)', options=options)[0]

        filename = image_path.split('/')
        filename = filename[len(filename)-1]

        if image_path:
            image = QImage(image_path)

            if image.isNull():  # TODO Controlla cosa intende per null; aggiungi check ulteriore per file di formato sbagliato (cioè formato giusto ma contenuto sbagliato)
                QMessageBox.information(self, 'IEViewer', 'Cannot open %s.', filename)
                return

            self.image_area.setPixmap(QPixmap.fromImage(image))
            #self.scaleFactor = 1.0  # TODO

            #self.scrollArea.setVisible(True)
            #self.printAct.setEnabled(True)
            #self.fitToWindowAct.setEnabled(True)
            #self.updateActions()

            #if not self.fitToWindowAct.isChecked():
            #    self.imageLabel.adjustSize()

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
