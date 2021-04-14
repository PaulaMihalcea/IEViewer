import sys, errno  # TODO Delete unnecessary imports
import webbrowser
from collections import OrderedDict
from PIL import Image, ImageQt, ExifTags
from PyQt5.QtCore import Qt, QEvent, QRect, QAbstractTableModel, QAbstractItemModel
from PyQt5.QtGui import QPixmap, QImage, QTransform, QMouseEvent, QStatusTipEvent, QColor, QPalette, QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QMenu, QMenuBar, QAction, QFileDialog, QMessageBox, QSizePolicy, QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QScrollArea, QTableView, QTableWidget, QFrame, QTableWidgetItem, QHeaderView, QToolBar, QAbstractItemView, QStatusBar


class ImageWidget(QLabel):
    """QWidget for visualizing an image.

    Attributes:
        model: The model of the MVC pattern.
        image_label: The QLabel that will contain the image
    """

    def __init__(self, model):
        """Inits the class."""
        super().__init__()

        self.model = model

        self.image_label = QLabel()

        # Alignment and resizing
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_label.setScaledContents(False)

        # Additional settings
        self.image_label.setMouseTracking(True)

    def update_image_label(self):
        """Updates the widget by drawing the actual image."""
        # TODO


class ExifWidget(QFrame):
    """QWidget for visualizing EXIF data.

    It combines a QTabletWidget into a QFrame.

    Attributes:
        model: The model of the MVC pattern.
        exif_data: The EXIF data of the model as a dictionary.
        exif_table: The QTableWidget object containing the EXIF data.
    """

    def __init__(self, exif):  # TODO model
        """Inits the class."""
        super().__init__()
        #self.model = model  #TODO
        #self.exif_data = model.get_exif_data()  # TODO
        self.exif_data = exif  # TODO

        if self.exif_data is not None:  # TODO Test behavior on images without EXIF data.
            self.create_table()
            self.set_layout()

    def create_table(self):
        """Initializes the exif_table attribute of the widget with a QTableWidget object."""
        self.exif_table = QTableWidget()

        # Row and column number definition
        self.exif_table.setRowCount(len(self.exif_data))
        self.exif_table.setColumnCount(2)

        # Graphical properties
        self.exif_table.setHorizontalHeaderLabels(('Property', 'Value'))
        self.exif_table.verticalHeader().setVisible(False)

        # User should not be able to edit table cell values
        self.exif_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Populate table with EXIF data
        i = 0
        for key in self.exif_data:
            self.exif_table.setItem(i, 0, QTableWidgetItem(key))
            self.exif_table.setItem(i, 1, QTableWidgetItem(str(self.exif_data[key])))
            i += 1

    def set_layout(self):
        """Sets the widget layout."""
        layout = QVBoxLayout()
        layout.addWidget(self.exif_table)

        self.setLayout(layout)


class StatusBar(QStatusBar):
    """Simple wrapper for the status bar. For consistency reasons.

    Attributes:
        text: The text displayed in the status bar.
    """

    def __init__(self):
        """Inits the class."""
        super().__init__()

    def update(self, text):
        """Updates the displayed text."""
        self.showMessage(text)


class MenuBar(QMenuBar):
    """Menu bar widget.

    Attributes:
        model: The model of the MVC pattern.
        menus: A dictionary containing the main menus (those listed in the bar), individually accessible,
                as well as another dictionary containing their relative actions and separators.
    """

    def __init__(self, model):
        """Inits the class."""
        super().__init__()

        self.model = model
        self.menus = OrderedDict()

        self.create_menus()
        self.create_actions()

        self.add_actions_to_menus()
        self.add_menus()

        #self.setNativeMenuBar(False)  # TODO serve?

    def create_menus(self):
        """Creates the main menus (those listed in the bar)."""
        self.menus['file'] = OrderedDict()
        self.menus['file']['menu_'] = QMenu('&File')
        self.menus['file']['menu_'].menuAction().setStatusTip('File options.')

        self.menus['edit'] = OrderedDict()
        self.menus['edit']['menu_'] = QMenu('&Edit')
        self.menus['edit']['menu_'].menuAction().setStatusTip('Image editing options.')

        self.menus['view'] = OrderedDict()
        self.menus['view']['menu_'] = QMenu('&View')
        self.menus['view']['menu_'].menuAction().setStatusTip('Interface options.')
        #self.menus['view']['menu_'].setDisabled(True)  # TODO invoca dal controller

        self.menus['help'] = OrderedDict()
        self.menus['help']['menu_'] = QMenu('&Help')
        self.menus['help']['menu_'].menuAction().setStatusTip('IEViewer information.')

    def create_actions(self):
        """Creates all available actions and submenus."""
        # Open
        self.menus['file']['open'] = QAction('&Open')
        self.menus['file']['open'].setShortcut('Ctrl+O')
        self.menus['file']['open'].setStatusTip('Open file.')
        self.menus['file']['open'].setIcon(QIcon('icons/open.png'))
        self.menus['file']['open'].triggered.connect(self.model.open_image)

        # Separator
        self.menus['file']['sep_1'] = QAction()
        self.menus['file']['sep_1'].setSeparator(True)

        # Save
        self.menus['file']['save'] = QAction('&Save')
        self.menus['file']['save'].setShortcut('Ctrl+S')
        self.menus['file']['save'].setStatusTip('Save file.')
        self.menus['file']['save'].setIcon(QIcon('icons/save.png'))
        self.menus['file']['save'].triggered.connect(self.model.save_image)

        # Save As
        self.menus['file']['saveas'] = QAction('Save &As...')
        self.menus['file']['saveas'].setShortcut('Ctrl+Shift+S')
        self.menus['file']['saveas'].setStatusTip('Save file with another name.')
        self.menus['file']['saveas'].setIcon(QIcon('icons/saveas.png'))
        self.menus['file']['saveas'].triggered.connect(self.model.save_as_image)

        # Close
        self.menus['file']['close'] = QAction('&Close')
        self.menus['file']['close'].setShortcut('Ctrl+W')
        self.menus['file']['close'].setStatusTip('Close current file.')
        self.menus['file']['close'].setIcon(QIcon('icons/close.png'))
        self.menus['file']['close'].triggered.connect(self.model.close_image)

        # Separator
        self.menus['file']['sep_2'] = QAction()
        self.menus['file']['sep_2'].setSeparator(True)

        # Exit
        self.menus['file']['exit'] = QAction('E&xit')
        self.menus['file']['exit'].setShortcut('Ctrl+Q')
        self.menus['file']['exit'].setStatusTip('Exit IEViewer.')
        self.menus['file']['exit'].setIcon(QIcon('icons/exit.png'))
        self.menus['file']['exit'].triggered.connect(self.model.exit)

        # Image Rotation
        self.menus['edit']['ir_submenu_'] = QMenu('Ima&ge Rotation')
        self.menus['edit']['ir_submenu_'].menuAction().setStatusTip('Rotate image.')
        self.menus['edit']['ir_submenu_'].setIcon(QIcon('icons/rotate90c.png'))
        # self.menus['edit']['ir_submenu_'].setDisabled(True)  # TODO invoca dal controller

        # Rotate 90° Clockwise
        self.menus['edit']['ir_sub_rotate90c'] = QAction('Rotate &right &90°')
        self.menus['edit']['ir_sub_rotate90c'].setShortcut('Ctrl+Right')
        self.menus['edit']['ir_sub_rotate90c'].setStatusTip('Rotate the image by 90 degrees right.')
        self.menus['edit']['ir_sub_rotate90c'].setIcon(QIcon('icons/rotate90c.png'))

        # Rotate 90° Counter Clockwise
        self.menus['edit']['ir_sub_rotate90cc'] = QAction('Rotate &left 90°')
        self.menus['edit']['ir_sub_rotate90cc'].setShortcut('Ctrl+Left')
        self.menus['edit']['ir_sub_rotate90cc'].setStatusTip('Rotate the image by 90 degrees left.')
        self.menus['edit']['ir_sub_rotate90cc'].setIcon(QIcon('icons/rotate90cc.png'))

        # Rotate 180°
        self.menus['edit']['ir_sub_rotate180'] = QAction('Rotate &180°')
        self.menus['edit']['ir_sub_rotate180'].setShortcut('Ctrl+U')
        self.menus['edit']['ir_sub_rotate180'].setStatusTip('Rotate the image by 180 degrees.')
        self.menus['edit']['ir_sub_rotate180'].setIcon(QIcon('icons/rotate180.png'))

        # Separator
        self.menus['edit']['sep_1'] = QAction()
        self.menus['edit']['sep_1'].setSeparator(True)

        # Reset Image
        self.menus['edit']['resetimage'] = QAction('&Reset Image')
        self.menus['edit']['resetimage'].setShortcut('Ctrl+0')
        self.menus['edit']['resetimage'].setStatusTip('Reset image to default size and rotation.')
        self.menus['edit']['resetimage'].setIcon(QIcon('icons/reset.png'))
        self.menus['edit']['resetimage'].triggered.connect(self.model.reset_image)

        # Previous Image
        self.menus['view']['prev'] = QAction('Previous Image')
        self.menus['view']['prev'].setShortcut('Left')
        self.menus['view']['prev'].setStatusTip('Show previous image.')
        self.menus['view']['prev'].setIcon(QIcon('icons/prev.png'))
        self.menus['view']['prev'].triggered.connect(self.model.prev_image)

        # Next Image
        self.menus['view']['next'] = QAction('Next Image')
        self.menus['view']['next'].setShortcut('Right')
        self.menus['view']['next'].setStatusTip('Show next image.')
        self.menus['view']['next'].setIcon(QIcon('icons/next.png'))
        self.menus['view']['next'].triggered.connect(self.model.next_image)

        # Separator
        self.menus['view']['sep_1'] = QAction()
        self.menus['view']['sep_1'].setSeparator(True)

        # Show EXIF
        self.menus['view']['showexif'] = QAction('Show &EXIF')
        self.menus['view']['showexif'].setShortcut('Ctrl+I')
        self.menus['view']['showexif'].setStatusTip('Show EXIF data for the current image.')
        self.menus['view']['showexif'].setIcon(QIcon('icons/showexif.png'))
        self.menus['view']['showexif'].triggered.connect(self.model.show_exif)

        # About
        self.menus['help']['about'] = QAction('&About')
        self.menus['help']['about'].setShortcut('F1')
        self.menus['help']['about'].setStatusTip('About IEViewer.')
        self.menus['help']['about'].setIcon(QIcon('icons/about.png'))
        self.menus['help']['about'].triggered.connect(self.model.about)

    def add_actions_to_menus(self):
        """Adds previously created actions to the toolbar menus."""
        current_submenu = None

        for m in self.menus:
            for a in self.menus[m]:
                if a != 'menu_':  # Only actions are considered
                    if 'submenu_' in a:  # Submenu
                        if a != current_submenu:
                            current_submenu = a
                            self.menus[m]['menu_'].addMenu(self.menus[m][current_submenu])
                    if 'sub_' in a:  # Submenu action
                        if isinstance(self.menus[m][a], QAction):  # Add actions
                            self.menus[m][current_submenu].addAction(self.menus[m][a])
                        elif isinstance(self.menus[m][a], QMenu):  # Add submenus
                            self.menus[m][current_submenu].addMenu(self.menus[m][a])
                    else:  # Menu action
                        if isinstance(self.menus[m][a], QAction):  # Add actions
                            self.menus[m]['menu_'].addAction(self.menus[m][a])
                        elif isinstance(self.menus[m][a], QMenu):  # Add submenus
                            self.menus[m]['menu_'].addMenu(self.menus[m][a])

    def add_menus(self):
        """Adds previously created menus to the toolbar."""
        for m in self.menus:
            self.addMenu(self.menus[m]['menu_'])

    def enable_item(self, menu, action=None):
        """Enables a (disabled) menu, submenu or action."""
        if action is None:
            self.menus[menu]['menu_'].setEnabled(True)
        else:
            self.menus[menu][action].setEnabled(True)

    def disable_item(self, menu, action=None):
        """Disables a (enabled) menu, submenu or action."""
        if action is None:
            self.menus[menu]['menu_'].setEnabled(False)
        else:
            self.menus[menu][action].setEnabled(True)


class ToolBar(QToolBar):
    """Tool bar widget.

    Attributes:
        model: The model of the MVC pattern.
        # TODO aggiungi lista azioni da eliminare
        actions: A dictionary containing the toolbar actions, individually accessible.
    """

    def __init__(self, model):
        """Inits the class."""
        super().__init__()

        self.model = model
        self.actions = OrderedDict()

        self.create_actions()
        self.add_actions()

    def create_actions(self):
        """Creates all available actions."""
        # Open
        self.actions['open'] = QAction('&Open')
        self.actions['open'].setShortcut('Ctrl+O')
        self.actions['open'].setStatusTip('Open file.')
        self.actions['open'].setIcon('icons/open.png')
        self.actions['open'].triggered.connect(self.model.open_image)

        # Separator
        self.actions['sep_1'] = QAction()
        self.actions['sep_1'].setSeparator(True)

        # Close
        self.actions['close'] = QAction('&Close')
        self.actions['close'].setShortcut('Ctrl+W')
        self.actions['close'].setStatusTip('Close current file.')
        self.actions['close'].setIcon('icons/close.png')
        self.actions['close'].triggered.connect(self.model.close_image)

        # Save
        self.actions['save'] = QAction('&Save')
        self.actions['save'].setShortcut('Ctrl+S')
        self.actions['save'].setStatusTip('Save file.')
        self.actions['save'].setIcon('icons/save.png')
        self.actions['save'].triggered.connect(self.model.save_image)

        # Save As
        self.actions['saveas'] = QAction('Save &As...')
        self.actions['saveas'].setShortcut('Ctrl+Shift+S')
        self.actions['saveas'].setStatusTip('Save file with another name.')
        self.actions['saveas'].setIcon('icons/.png')  # TODO
        self.actions['saveas'].triggered.connect(self.model.save_as_image)

        # Separator
        self.actions['sep_2'] = QAction()
        self.actions['sep_2'].setSeparator(True)

        # Image Rotation
        self.actions['ir_submenu_'] = QMenu('Ima&ge Rotation')
        self.actions['ir_submenu_'].menuAction().setStatusTip('Rotate image.')
        self.actions[''].setIcon('icons/.png')
        # self.actions['ir_submenu_'].setDisabled(True)  # TODO invoca dal controller

        # Rotate 180°
        self.actions['ir_sub_rotate180'] = QAction('&180°')
        self.actions['ir_sub_rotate180'].setShortcut('Ctrl+1')
        self.actions[''].setIcon('icons/.png')
        self.actions['ir_sub_rotate180'].setStatusTip('Rotate image by 180 degrees.')

        # Rotate 90° Clockwise
        self.actions['ir_sub_rotate90c'] = QAction('&90° Clockwise')
        self.actions['ir_sub_rotate90c'].setShortcut('Ctrl+2')
        self.actions[''].setIcon('icons/.png')
        self.actions['ir_sub_rotate90c'].setStatusTip('Rotate image by 90 degrees (clockwise).')

        # Rotate 90° Counter Clockwise
        self.actions['ir_sub_rotate90cc'] = QAction('90° &Counter Clockwise')
        self.actions['ir_sub_rotate90cc'].setShortcut('Ctrl+3')
        self.actions[''].setIcon('icons/.png')
        self.actions['ir_sub_rotate90cc'].setStatusTip('Rotate image by 90 degrees (counter clockwise).')

        # Separator
        self.actions['sep_1'] = QAction()
        self.actions['sep_1'].setSeparator(True)

        # Reset Image
        self.actions['resetimage'] = QAction('&Reset Image')
        self.actions['resetimage'].setShortcut('Ctrl+0')
        self.actions['resetimage'].setStatusTip('Reset image to default size and rotation.')
        self.actions['resetimage'].setIcon('icons/resetimage.png')
        self.actions['resetimage'].triggered.connect(self.model.reset_image)

        # Show EXIF
        self.actions['showexif'] = QAction('Show &EXIF')
        self.actions['showexif'].setShortcut('Ctrl+I')
        self.actions['showexif'].setStatusTip('Show EXIF data for the current image.')
        self.actions['showexif'].setIcon('icons/showexif.png')
        self.actions['showexif'].triggered.connect(self.model.show_exif)

        # About
        self.actions['about'] = QAction('&About')
        self.actions['about'].setShortcut('F1')
        self.actions['about'].setStatusTip('About IEViewer.')
        self.actions['about'].setIcon('icons/about.png')
        self.actions['about'].triggered.connect(self.model.about)

    def add_actions(self):  # TODO
        """Adds previously created menus to the toolbar."""
        for m in self.actions:
            self.addMenu(self.actions['menu_'])

    def enable_item(self, menu, action=None):  # TODO
        """Enables a (disabled) menu, submenu or action."""
        if action is None:
            self.actions['menu_'].setEnabled(True)
        else:
            self.actions[action].setEnabled(True)

    def disable_item(self, menu, action=None):  # TODO
        """Disables a (enabled) menu, submenu or action."""
        if action is None:
            self.actions['menu_'].setEnabled(False)
        else:
            self.actions[action].setEnabled(True)
