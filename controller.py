from PIL import Image
from observer import Observer


class Controller(Observer):
    def __init__(self, model, view):
        """Inits the class."""
        Observer.__init__(self, view)
        self.model = model
        self.view = view

        self.update()

    def update(self):  # Overrides observer update method; alternatively can be manually used to set stuff
        state = self.subject.state
        if state == 'open':  # Open an image
            self.open()
        if state == 'close':  # Close opened image
            self.model.close_image()


    def get_main_window(self):
        return self.view

    def open(self):
        image_path = self.view.get_file_dialog(caption='Open', filter='Image Files (*.bmp; *.gif; *.jpg; *.jpeg; *.png; *.pbm; *.pgm; *.ppm; *.xbm; *.xpm)')

        # Load image and EXIF data
        if image_path is not None:  # Only continues if a file has been chosen; if the user chose "Cancel" in the previous dialog, the program just returns to its default state
            # Get file name from the absolute image path
            filename = image_path.split('/')
            filename = filename[len(filename)-1]

            try:
                image = Image.open(image_path)
            except IOError:
                self.view.show_message_box(title='IEViewer', text='Could not open "{}". \nInvalid file or format not supported.'.format(filename))
                return

            self.model.load_image(image, filename)  # Update model
            self.view.load_image()  # Update view
        else:
            pass
