def main(args):  # TODO Usa args
    import sys
    from PyQt5.QtWidgets import QApplication
    from IEViewer import ImageViewer

    app = QApplication(sys.argv)  # TODO Oppure QApplication([])  # This is a requirement of Qt: Every GUI app must have exactly one instance of QApplication

    imageViewer = ImageViewer()
    imageViewer.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description='A simple Python image & EXIF data viewer.')
    parser.add_argument('-p', '--path', help='Path of the image to be opened.')

    args = parser.parse_args()

    main(args)
