import sys
from PIL import Image
from observer import Observer


class Controller(Observer):
    """Concrete Controller class. It is hard to get a more classic MVC implementation than this.

    Here is where the images are loaded and most user input is handled.
    Most, because some PyQt5-related functions have been forcefully moved to the View,
        otherwise they did not work. PyQt5 magic.

    Attributes:
        model: The model for the image.
        view: The view for the image.
    """
    def __init__(self, model, view):
        """Inits the class with the view and model."""
        Observer.__init__(self, view)

        self.model = model
        self.view = view

        self.update()

    def update(self):
        """Overrides the Observer update method; alternatively, can also be used to manually set stuff (although it should not, or at least I think it is uglier)."""
        state = self.subject.state
        if state == 'open':  # Open an image
            self.open()
        if state == 'close':  # Close opened image
            self.close()
        if state == 'exit':  # Exit application
            sys.exit()
        if state == 'save':  # Save image
            self.save()
        if state == 'saveas':  # Save image as
            self.saveas()

    def get_main_window(self):
        """View (main window) getter."""
        return self.view

    def open(self):
        """Opens an image file using the PIL library.

        Although images are later processed as QImage onjects, PIL is needed to extract any eventual EXIF data.
        Checks that the file is a valid image, then passes it to the model (if it is, otherwise returns an error message).
        """
        # Get file dialog in order to obtain an image file path
        image_path = self.view.get_open_file_dialog(caption='Open', filter='Image Files (*.bmp *.gif *.jpg *.jpeg *.png *.pbm *.pgm *.ppm *.xbm *.xpm);; All Files (*.*)')

        # Load image and EXIF data
        # Only proceeds if a file has been chosen; if the user chose "Cancel" in the file dialog, or closed it, the program just returns to its previous state
        if image_path is not None:
            # Get file name from the absolute image path
            filename = image_path.split('/')
            filename = filename[len(filename)-1]

            # Check if the image is valid
            try:
                image = Image.open(image_path)
            except IOError:
                self.view.show_message_box(title='IEViewer', text='Could not open "{}". \nInvalid file or format not supported.'.format(filename))
                return

            # Close an image that has been already opened in the viewer (needed for correct display and EXIF data)
            if self.model.image is not None:
                self.view.close()

            # Update model and view
            self.model.load_image(image, filename)
            self.view.load_image()
        else:  # No image has been chosen
            pass

    def close(self):
        """Closes an image (model method wrapper)."""
        self.model.close_image()

    def save(self):
        """Saves an image (model method wrapper)."""
        self.model.image.save(self.model.filename)

    def saveas(self):
        """Saves an image with a different name (mainly a model method wrapper)."""
        image_path, format = self.view.get_save_file_dialog(caption='Save As', filter='JPEG (*.jpg; *.jpeg);; PNG (*.png);; BMP (*.bmp);; PPM (*.ppm);; XBM (*.xbm);; XPM (*.xpm)')
        self.model.modified_image.save(image_path + '.' + format)
