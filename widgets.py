import webbrowser
from collections import OrderedDict
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QMenu, QMenuBar, QAction, QMessageBox, QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QFrame, QTableWidgetItem, QToolBar, QAbstractItemView, QStatusBar


class ImageWidget(QLabel):
    """QWidget for visualizing an image.

    Attributes:
        view: The view of the MVC pattern.
        image: The original, loaded image, which is used as base for all transformations.
        pixmap: The currently displayed pixmap (built from the original image).
        w: The current width of the pixmap.
        h: The current width of the pixmap.
        rot: The current rotation of the displayed pixmap (needed to keep track of all rotations, so as to be able to eventually reset the image).
    """

    def __init__(self, view):
        """Inits the class."""
        super().__init__()

        self.view = view
        self.image = None
        self.pixmap = None
        self.w = 0
        self.h = 0
        self.rot = 0

        # Alignment and resizing
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)  # Allow resizing
        self.setScaledContents(False)  # Avoid stretching the image

    def set_image(self, image, width, height):
        """Displays and image by generating a pixmap from it.

        Keeping the original image is needed in order to avoid generating an increasingly bad quality pixmap with each transformation.

        Args:
            image:
                The original image to be displayed.
            width:
                The width of the displayed image (not its original width).
            height:
                The height of the displayed image (not its original height).
        """
        self.w = width
        self.h = height

        self.installEventFilter(self)  # Install the new event handler

        # Add pixmap from image and resize it accordingly
        pixmap = QPixmap.fromImage(image).scaled(self.w, self.h, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.pixmap = QPixmap(pixmap)

    def clear_image(self):
        """Reset all the attributes to their original state. Intended to be used for properly closing an image."""
        self.clear()
        self.update()
        self.pixmap = None
        self.w = 0
        self.h = 0


class ExifWidget(QFrame):
    """QWidget for visualizing EXIF data.

    It combines a QTabletWidget into a QFrame.

    Attributes:
        view: The view of the MVC pattern.
        exif_data: The EXIF data of the view as a dictionary.
        exif_table: The QTableWidget object containing the EXIF data.
    """

    def __init__(self, view):
        """Inits the class."""
        super().__init__()

        self.view = view
        self.exif_data = None
        self.exif_table = None

    def load_exif(self):
        """Loads the image's EXIF data.

        Data is either stored into a QTableWidget if it exists,
        otherwise a QLabel saying that no EXIF data exists is displayed instead."""
        self.exif_data = self.view.model.exif_data

        if self.exif_data is not None:  # EXIF data exists
            self.get_table()
            self.exif_table.resizeColumnsToContents()  # Resize table cells to fit their contents for better legibility
        else:  # No EXIF data available
            self.exif_table = QLabel()
            self.exif_table.setText('No EXIF data available for this image.')
            self.exif_table.setAlignment(Qt.AlignCenter)

        self.set_layout()  # Set the resulting QFrame layout

    def get_table(self):
        """Initializes the exif_table attribute of the widget with a QTableWidget object."""
        self.exif_table = QTableWidget()

        # Row and column number definition
        self.exif_table.setRowCount(len(self.exif_data))
        self.exif_table.setColumnCount(2)

        # Graphic properties
        self.exif_table.setHorizontalHeaderLabels(('Property', 'Value'))  # Set header labels
        self.exif_table.verticalHeader().setVisible(False)  # Hide rows' header (unneeded)
        self.exif_table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  # Smooth vertical scrolling
        self.exif_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)  # Smooth horizontal scrolling

        # User should not be able to edit table cell values
        self.exif_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Populate table with EXIF data
        i = 0
        for key in self.exif_data:
            self.exif_table.setItem(i, 0, QTableWidgetItem(key))
            self.exif_table.setItem(i, 1, QTableWidgetItem(str(self.exif_data[key])))
            if 'http' in self.exif_table.item(i, 1).text():  # Status bar description for clickable links
                self.exif_table.setStatusTip('Double click on the GPS location link to open a map centered at those GPS coordinates.')
            i += 1

        # Connects double clicking on the GPS location link to the browser.
        self.exif_table.itemDoubleClicked.connect(self.open_link)

    def set_layout(self):
        """Sets the widget layout."""
        layout = QVBoxLayout()
        layout.addWidget(self.exif_table)

        self.setLayout(layout)

    def open_link(self, item):
        """Connects double clicking on the GPS location link to the browser."""
        if 'http' in item.text():
            webbrowser.open(item.text())


class StatusBar(QStatusBar):
    """Simple wrapper for the status bar. For consistency reasons."""

    def __init__(self):
        """Inits the class."""
        super().__init__()

        self.setMinimumHeight(20)
        self.setMaximumHeight(20)
        self.setSizeGripEnabled(False)


class MenuBar(QMenuBar):
    """Menu bar widget.

    Attributes:
        view: The view of the MVC pattern.
        menus: A dictionary containing the main menus (those listed in the bar), individually accessible,
                as well as another dictionary containing their relative actions and separators.
        disabled_menus: A list of the menus that should be disabled when no image is opened.
        disabled_actions: A list of the actions that should be disabled when no image is opened.
    """

    def __init__(self, view):
        """Inits the class."""
        super().__init__()

        self.view = view
        self.menus = OrderedDict()

        self.get_menus()
        self.get_actions()

        self.add_actions_to_menus()
        self.add_menus()

        self.setMinimumHeight(25)
        self.setMaximumHeight(25)

        self.disabled_menus = ['edit', 'view']
        self.disabled_actions = [('file', 'save'),
                                 ('file', 'saveas'),
                                 ('file', 'close'),
                                 ('edit', 'ir_submenu_'),
                                 ('edit', 'ir_sub_rotate180'),
                                 ('edit', 'ir_sub_rotate90c'),
                                 ('edit', 'ir_sub_rotate90cc'),
                                 ('edit', 'resetimage'),
                                 ('view', 'showexif'),
                                 ('view', 'analyze')
                                 ]

    def get_menus(self):
        """Creates the main menus (those listed in the menu bar)."""
        # File
        self.menus['file'] = OrderedDict()
        self.menus['file']['menu_'] = QMenu('&File')
        self.menus['file']['menu_'].menuAction().setStatusTip('File options.')

        # Edit
        self.menus['edit'] = OrderedDict()
        self.menus['edit']['menu_'] = QMenu('&Edit')
        self.menus['edit']['menu_'].menuAction().setStatusTip('Image editing options.')

        # View
        self.menus['view'] = OrderedDict()
        self.menus['view']['menu_'] = QMenu('&View')
        self.menus['view']['menu_'].menuAction().setStatusTip('Interface options.')

        # Help
        self.menus['help'] = OrderedDict()
        self.menus['help']['menu_'] = QMenu('&Help')
        self.menus['help']['menu_'].menuAction().setStatusTip('IEViewer information.')

    def get_actions(self):
        """Creates all available actions and submenus."""
        # Open
        self.menus['file']['open'] = QAction('&Open', self.view)
        self.menus['file']['open'].setShortcut('Ctrl+O')
        self.menus['file']['open'].setStatusTip('Open file.')
        self.menus['file']['open'].setIcon(QIcon('icons/open.png'))
        self.menus['file']['open'].triggered.connect(self.view.open)

        # Separator
        self.menus['file']['sep_1'] = QAction(self.view)
        self.menus['file']['sep_1'].setSeparator(True)

        # Save
        self.menus['file']['save'] = QAction('&Save', self.view)
        self.menus['file']['save'].setShortcut('Ctrl+S')
        self.menus['file']['save'].setStatusTip('Save file.')
        self.menus['file']['save'].setIcon(QIcon('icons/save.png'))
        self.menus['file']['save'].triggered.connect(self.view.save)

        # Save As
        self.menus['file']['saveas'] = QAction('Save &As...', self.view)
        self.menus['file']['saveas'].setShortcut('Ctrl+Shift+S')
        self.menus['file']['saveas'].setStatusTip('Save file with another name.')
        self.menus['file']['saveas'].setIcon(QIcon('icons/saveas.png'))
        self.menus['file']['saveas'].triggered.connect(self.view.saveas)

        # Close
        self.menus['file']['close'] = QAction('&Close', self.view)
        self.menus['file']['close'].setShortcut('Ctrl+W')
        self.menus['file']['close'].setStatusTip('Close current file.')
        self.menus['file']['close'].setIcon(QIcon('icons/close.png'))
        self.menus['file']['close'].triggered.connect(self.view.close)

        # Separator
        self.menus['file']['sep_2'] = QAction(self.view)
        self.menus['file']['sep_2'].setSeparator(True)

        # Exit
        self.menus['file']['exit'] = QAction('E&xit', self.view)
        self.menus['file']['exit'].setShortcut('Ctrl+Q')
        self.menus['file']['exit'].setStatusTip('Exit IEViewer.')
        self.menus['file']['exit'].setIcon(QIcon('icons/exit.png'))
        self.menus['file']['exit'].triggered.connect(self.view.exit)

        # Image Rotation
        self.menus['edit']['ir_submenu_'] = QMenu('Ima&ge Rotation', self.view)
        self.menus['edit']['ir_submenu_'].menuAction().setStatusTip('Rotate image.')
        self.menus['edit']['ir_submenu_'].setIcon(QIcon('icons/rotate90c.png'))

        # Rotate 90° Clockwise
        self.menus['edit']['ir_sub_rotate90c'] = QAction('Rotate &right &90°', self.view)
        self.menus['edit']['ir_sub_rotate90c'].setShortcut('Ctrl+Right')
        self.menus['edit']['ir_sub_rotate90c'].setStatusTip('Rotate the image by 90 degrees right.')
        self.menus['edit']['ir_sub_rotate90c'].setIcon(QIcon('icons/rotate90c.png'))
        self.menus['edit']['ir_sub_rotate90c'].triggered.connect(self.view.rotate90c)

        # Rotate 90° Counter Clockwise
        self.menus['edit']['ir_sub_rotate90cc'] = QAction('Rotate &left 90°', self.view)
        self.menus['edit']['ir_sub_rotate90cc'].setShortcut('Ctrl+Left')
        self.menus['edit']['ir_sub_rotate90cc'].setStatusTip('Rotate the image by 90 degrees left.')
        self.menus['edit']['ir_sub_rotate90cc'].setIcon(QIcon('icons/rotate90cc.png'))
        self.menus['edit']['ir_sub_rotate90cc'].triggered.connect(self.view.rotate90cc)

        # Rotate 180°
        self.menus['edit']['ir_sub_rotate180'] = QAction('Rotate &180°', self.view)
        self.menus['edit']['ir_sub_rotate180'].setShortcut('Ctrl+Up')
        self.menus['edit']['ir_sub_rotate180'].setStatusTip('Rotate the image by 180 degrees.')
        self.menus['edit']['ir_sub_rotate180'].setIcon(QIcon('icons/rotate180.png'))
        self.menus['edit']['ir_sub_rotate180'].triggered.connect(self.view.rotate180)

        # Separator
        self.menus['edit']['sep_3'] = QAction(self.view)
        self.menus['edit']['sep_3'].setSeparator(True)

        # Reset Image
        self.menus['edit']['resetimage'] = QAction('&Reset Image', self.view)
        self.menus['edit']['resetimage'].setShortcut('Ctrl+0')
        self.menus['edit']['resetimage'].setStatusTip('Reset image to default size and rotation.')
        self.menus['edit']['resetimage'].setIcon(QIcon('icons/reset.png'))
        self.menus['edit']['resetimage'].triggered.connect(self.view.reset_image)

        # Show EXIF
        self.menus['view']['showexif'] = QAction('Show &EXIF', self.view)
        self.menus['view']['showexif'].setShortcut('Ctrl+I')
        self.menus['view']['showexif'].setStatusTip('Show EXIF data for the current image.')
        self.menus['view']['showexif'].setIcon(QIcon('icons/showexif.png'))
        self.menus['view']['showexif'].setCheckable(True)
        self.menus['view']['showexif'].triggered.connect(self.view.show_exif)

        # Analyze
        self.menus['view']['analyze'] = QAction('Analyze', self.view)
        self.menus['view']['analyze'].setShortcut('Ctrl+A')
        self.menus['view']['analyze'].setStatusTip('Analyze image to find photo manipulations using an EM algorithm.')
        self.menus['view']['analyze'].setIcon(QIcon('icons/analyze.png'))
        self.menus['view']['analyze'].setCheckable(True)
        self.menus['view']['analyze'].triggered.connect(self.view.analyze)

        # About
        self.menus['help']['about'] = QAction('&About', self.view)
        self.menus['help']['about'].setShortcut('F1')
        self.menus['help']['about'].setStatusTip('About IEViewer.')
        self.menus['help']['about'].setIcon(QIcon('icons/about.png'))
        self.menus['help']['about'].triggered.connect(self.view.about)

    def add_actions_to_menus(self):
        """Adds previously created actions to the toolbar menus."""
        current_submenu = None  # Keep track of the menu we are working on (needed for submenus)

        for m in self.menus:
            for a in self.menus[m]:
                if a != 'menu_':  # Only actions are considered
                    if 'submenu_' in a:  # Submenu found
                        if a != current_submenu:  # Update current submenu and add it the its parent menu
                            current_submenu = a
                            self.menus[m]['menu_'].addMenu(self.menus[m][current_submenu])
                    if 'sub_' in a:  # Submenu action found
                        if isinstance(self.menus[m][a], QAction):  # Add actions
                            self.menus[m][current_submenu].addAction(self.menus[m][a])
                        elif isinstance(self.menus[m][a], QMenu):  # Add submenus
                            self.menus[m][current_submenu].addMenu(self.menus[m][a])
                    else:  # Menu action found
                        if isinstance(self.menus[m][a], QAction):  # Add actions
                            self.menus[m]['menu_'].addAction(self.menus[m][a])
                        elif isinstance(self.menus[m][a], QMenu):  # Add submenus
                            self.menus[m]['menu_'].addMenu(self.menus[m][a])

    def add_menus(self):
        """Adds previously created menus to the toolbar."""
        for m in self.menus:
            self.addMenu(self.menus[m]['menu_'])

    def enable(self, menu, action=None):
        """Enables a menu, submenu or action (if disabled, otherwise does nothing)."""
        if action is None:
            self.menus[menu]['menu_'].setEnabled(True)
        else:
            self.menus[menu][action].setEnabled(True)

    def disable(self, menu, action=None):
        """Disables a menu, submenu or action (if enabled, otherwise does nothing)."""
        if action is None:
            self.menus[menu]['menu_'].setEnabled(False)
        else:
            self.menus[menu][action].setEnabled(False)

    def enable_widgets(self):
        """Enable all elements of the interface which should be available when an image is opened."""
        for m in self.disabled_menus:
            self.enable(m)
        for a in self.disabled_actions:
            self.enable(a[0], a[1])

    def disable_widgets(self):
        """Disable all elements of the interface which should not be available when no image is opened."""
        for m in self.disabled_menus:
            self.disable(m)
        for a in self.disabled_actions:
            self.disable(a[0], a[1])
            if isinstance(self.menus[a[0]][a[1]], QAction) and self.menus[a[0]][a[1]].isChecked():
                self.menus[a[0]][a[1]].setChecked(False)


class ToolBar(QToolBar):
    """Tool bar widget.

    Attributes:
        view: The view of the MVC pattern.
        actions: A dictionary containing the toolbar actions, individually accessible.
        excluded_actions: A list of the menu bar actions that should not appear in the toolbar (including separator actions).
    """

    def __init__(self, view):
        """Inits the class."""
        super().__init__()

        self.view = view
        self.actions = OrderedDict()
        self.excluded_actions = ['sep_2', 'sep_3', 'exit']

        self.get_actions()
        self.add_actions()

        self.setMinimumWidth(408)  # Needed in order to avoid having to resize the main window at startup (otherwise some buttons will be collapsed)
        self.setMovable(False)  # The toolbar should not be moved around, for aesthetic and layout reasons

    def get_actions(self):
        """Retrieves all available actions from the view's menu bar, except those included in the excluded_actions list."""
        menus = self.view.menu_bar.menus
        current_menu = None  # Keep track of the menu to which the current action belongs
        sep_number = 1  # Simple separator counter, to avoid having multiple, identical keys in the dictionary

        for m in menus:
            if m != current_menu:  # Add separators between different menu bar categories
                if current_menu is not None:
                    self.actions['sep_toolbar_' + str(sep_number)] = QAction(self.view)
                    self.actions['sep_toolbar_' + str(sep_number)].setSeparator(True)
                    sep_number += 1
                current_menu = m  # Update current menu
            for a in menus[m]:  # Add actions
                if isinstance(menus[m][a], QAction) and a not in self.excluded_actions:
                    self.actions[a] = menus[m][a]

    def add_actions(self):
        """Adds previously created actions to the toolbar."""
        for a in self.actions:
            self.addAction(self.actions[a])

    def enable_item(self, action):
        """Enables a (disabled) action."""
        self.actions[action].setEnabled(True)

    def disable_item(self, action):
        """Disables an (enabled) action."""
        self.actions[action].setEnabled(True)


class Layout(QVBoxLayout):
    """Layout class. Defines the layout of the whole interface.

    Note: Make sure to apply this layout to the central widget, not the window.

    Attributes:
        view: The view of the MVC pattern.
        central_widget: The actual widget that is going to have this layout (applying the layout directly to the QWindow does not work). A necessary evil, though redundant.
    """

    def __init__(self, view):
        """Inits the class."""
        super().__init__()

        self.view = view
        self.central_widget = None

        self.get_layout()
        self.get_central_widget()

        # Graphic properties
        self.setContentsMargins(0, 0, 0, 0)

    def get_layout(self):
        """Creates the interface layout. Widgets that can change at runtime are managed through their respective show() and hide() functions."""
        toolbars_layout = QVBoxLayout()
        image_exif_layout = QHBoxLayout()

        # No margins
        toolbars_layout.setContentsMargins(0, 0, 0, 0)
        image_exif_layout.setContentsMargins(0, 0, 0, 0)

        # Menu + tool bar
        toolbars_layout.addWidget(self.view.menu_bar)
        toolbars_layout.addWidget(self.view.tool_bar)

        # Exif + image area
        image_exif_layout.addWidget(self.view.exif_area)
        image_exif_layout.addWidget(self.view.image_area)

        # Complete layout
        self.addLayout(toolbars_layout)
        self.addLayout(image_exif_layout)
        self.addWidget(self.view.status_bar)

    def get_central_widget(self):
        """Creates the QWindow central widget (apparently, a necessary, redundant evil)."""
        self.central_widget = QWidget()
        self.central_widget.setLayout(self)

    def enable_widget(self, widget):
        """Enables a (hidden) widget."""
        widget.show()

    def disable_widget(self, widget):
        """Disables a (visible) widget."""
        widget.hide()


class AboutWidget(QMessageBox):
    """About widget class. Displays info about the program."""
    def __init__(self, title, text, image_path):
        """Inits the class."""
        super().__init__()

        self.setWindowTitle(title)
        self.setText(text)
        self.setTextFormat(Qt.RichText)
        self.setIconPixmap(QPixmap(image_path))
