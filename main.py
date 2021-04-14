def main(args):  # TODO Implement args
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QIcon
    from IEViewer  import ImageViewer

    app = QApplication(sys.argv)  # Note: There must be exactly one instance of QApplication active at a time
    app.setWindowIcon(QIcon('icons/ieviewer.png'))

    imageViewer = ImageViewer()
    imageViewer.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description='A simple Python image & EXIF data viewer.')
    parser.add_argument('-p', '--path', help='Path of the image to be opened.')

    args = parser.parse_args()

    main(args)
