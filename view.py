import sys, errno
import webbrowser
from PIL import Image, ImageQt, ExifTags
from PyQt5.QtCore import Qt, QEvent, QRect, QAbstractTableModel, QAbstractItemModel
from PyQt5.QtGui import QPixmap, QImage, QTransform, QMouseEvent, QStatusTipEvent, QColor, QPalette, QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QMenu, QMenuBar, QAction, QFileDialog, QMessageBox, QSizePolicy, QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QScrollArea, QTableView, QTableWidget, QFrame, QTableWidgetItem, QHeaderView, QToolBar

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
