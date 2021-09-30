from PIL import ImageQt, ExifTags


class ImageModel():
    """Model class for the image.

    Basically, this is the class which holds the loaded image, its EXIF data and the modified image which might be eventually saved by the user.
    It also processes said EXIF data, including GPS data (with the relative Google Maps link).

    Attributes:
        image: the current loaded image (PyQt5 image).
        analyzed_image: An image combining both the original image and its manipulation map.
        exif_data: A dictionary containing all EXIF data available for the image (None if there is none).
        filename: The original image's file name (needed for saving).
        path: The original image's absolute path (needed for finding the ground truth when analyzing the image).
        modified_image: A PyQt image (QImage) modified by the user (i.e. a rotated version of the original image). Also needed for saving.
        terminal_flag: Boolean flag needed to determine if the main program has been started from the terminal or an IDE (see main.py).
    """
    def __init__(self, terminal_flag):
        """Inits the class."""
        self.image = None
        self.original_image = None
        self.analyzed_image = None
        self.exif_data = None
        self.filename = None
        self.path = None

        self.modified_image = None
        self.manipulation_flag = False
        self.terminal_flag = terminal_flag

    def set_image(self, image):
        """Image setter."""
        self.image = image

    def set_modified_image(self, modified_image):
        """Modified image setter.."""
        self.modified_image = modified_image

    def load_image(self, image, image_path):
        """Processes an image loaded by and received from the Controller."""
        # Get file name from the absolute image path
        filename = image_path.split('/')
        filename = filename[len(filename) - 1]

        # Store needed data in model
        self.filename = filename
        self.image_path = image_path
        self.image = ImageQt.ImageQt(image)
        self.modified_image = self.image

        # Get file format (needed for the check below)
        format = self.filename.split('.')
        format = format[len(format)-1]

        # PIL only gets EXIF data from JPEG images.
        # To an extent, it also supports PNG EXIF data; however,
        # the image must be loaded before trying to extract these attributes.
        if '_getexif' in dir(image) and image._getexif() is not None:  # JPEG with EXIF data
            self.exif_data = {ExifTags.TAGS[k]: v for k, v in image._getexif().items() if k in ExifTags.TAGS}
            self.set_gps_data()
        elif format == 'png':  # PNG
            image.load()
            self.exif_data = image.info

    def close_image(self):
        """Reset all the attributes to their original state. Intended to be used for properly closing an image."""
        self.image = None
        self.analyzed_image = None
        self.exif_data = None
        self.filename = None
        self.manipulation_flag = False

    def set_gps_data(self):
        """EXIF data setter."""
        exif_data_gps = self.process_gps_data()

        if exif_data_gps is not None:
            self.exif_data = exif_data_gps
        else:
            return

    def process_gps_data(self):
        """Process GPS EXIF data, if available.

        PIL's _getexif() function behaves differently according to where the main program has been run from.
        In particular, it returns data in a different format if it has been started from the terminal, or an IDE.
        Failing to acknowledge this fact will result in a crash.
        """
        exif_data = self.exif_data  # EXIF data
        gps_data = self.exif_data.get('GPSInfo')  # Dictionary for storing the GPS EXIF data

        if gps_data is not None:  # GPS EXIF data available
            gps_data_dict = {}  # Contains all GPS EXIF tags with their proper names (and relative values)

            # EXIF GPS tags' numbers taken from: https://exiftool.org/TagNames/GPS.html
            if gps_data.get(0) is not None:
                gps_data_dict['GPSVersionID'] = gps_data.get(0)
            if gps_data.get(1) is not None:
                gps_data_dict['GPSLatitudeRef'] = gps_data.get(1)
            if gps_data.get(2) is not None:
                gps_data_dict['GPSLatitude'] = gps_data.get(2)
            if gps_data.get(3) is not None:
                gps_data_dict['GPSLongitudeRef'] = gps_data.get(3)
            if gps_data.get(4) is not None:
                gps_data_dict['GPSLongitude'] = gps_data.get(4)
            if gps_data.get(5) is not None:
                gps_data_dict['GPSAltitudeRef'] = gps_data.get(5)
            if gps_data.get(6) is not None:
                gps_data_dict['GPSAltitude'] = gps_data.get(6)
            if gps_data.get(7) is not None:
                gps_data_dict['GPSTimeStamp'] = gps_data.get(7)
            if gps_data.get(8) is not None:
                gps_data_dict['GPSSatellites'] = gps_data.get(8)
            if gps_data.get(9) is not None:
                gps_data_dict['GPSStatus'] = gps_data.get(9)
            if gps_data.get(10) is not None:
                gps_data_dict['GPSMeasureMode'] = gps_data.get(10)
            if gps_data.get(11) is not None:
                gps_data_dict['GPSDOP'] = gps_data.get(11)
            if gps_data.get(12) is not None:
                gps_data_dict['GPSSpeedRef'] = gps_data.get(12)
            if gps_data.get(13) is not None:
                gps_data_dict['GPSSpeed'] = gps_data.get(13)
            if gps_data.get(14) is not None:
                gps_data_dict['GPSTrackRef'] = gps_data.get(14)
            if gps_data.get(15) is not None:
                gps_data_dict['GPSTrack'] = gps_data.get(15)
            if gps_data.get(16) is not None:
                gps_data_dict['GPSImgDirectionRef'] = gps_data.get(16)
            if gps_data.get(17) is not None:
                gps_data_dict['GPSImgDirection'] = gps_data.get(17)
            if gps_data.get(18) is not None:
                gps_data_dict['GPSMapDatum'] = gps_data.get(18)
            if gps_data.get(19) is not None:
                gps_data_dict['GPSDestLatitudeRef'] = gps_data.get(19)
            if gps_data.get(20) is not None:
                gps_data_dict['GPSDestLatitude'] = gps_data.get(20)
            if gps_data.get(21) is not None:
                gps_data_dict['GPSDestLongitudeRef'] = gps_data.get(21)
            if gps_data.get(22) is not None:
                gps_data_dict['GPSDestLongitude'] = gps_data.get(22)
            if gps_data.get(23) is not None:
                gps_data_dict['GPSDestBearingRef'] = gps_data.get(23)
            if gps_data.get(24) is not None:
                gps_data_dict['GPSDestBearing'] = gps_data.get(24)
            if gps_data.get(25) is not None:
                gps_data_dict['GPSDestDistanceRef'] = gps_data.get(25)
            if gps_data.get(26) is not None:
                gps_data_dict['GPSDestDistance'] = gps_data.get(26)
            if gps_data.get(27) is not None:
                gps_data_dict['GPSProcessingMethod'] = gps_data.get(27)
            if gps_data.get(28) is not None:
                gps_data_dict['GPSAreaInformation'] = gps_data.get(28)
            if gps_data.get(29) is not None:
                gps_data_dict['GPSDateStamp'] = gps_data.get(29)
            if gps_data.get(30) is not None:
                gps_data_dict['GPSDifferential'] = gps_data.get(30)
            if gps_data.get(31) is not None:
                gps_data_dict['GPSHPositioningError'] = gps_data.get(31)

            # Remove original GPS EXIF data (which is too short and non-descriptive)
            # and replace it with the new, processed dictionary
            exif_data.pop('GPSInfo')

            exif_data_updated = {}  # Contains the original EXIF data + the new GPS EXIF data

            exif_data_updated.update({'GPSLocation': self.build_gmaps_link(gps_data_dict['GPSLatitude'], gps_data_dict['GPSLatitudeRef'], gps_data_dict['GPSLongitude'], gps_data_dict['GPSLongitudeRef'])})
            exif_data_updated.update(gps_data_dict)
            exif_data_updated.update(exif_data)

            return exif_data_updated
        else:  # No GPS EXIF data available
            return None

    def build_gmaps_link(self, lat, lat_ref, lon, lon_ref):
        """Builds a Google Maps link for the specified GPS location.

        Here is where the distinction between terminal and IDE script actually comes in play (see main.py and above)."""
        if not self.terminal_flag:  # IDE
            lat = tuple(lat)
            lon = tuple(lon)
            latitude = str(int(lat[0])) + '°' + str(int(lat[1])) + '\'' + str(lat[2]) + '\"' + lat_ref
            longitude = str(int(lon[0])) + '°' + str(int(lon[1])) + '\'' + str(lon[2]) + '\"' + lon_ref
        else:  # Terminal
            # Latitude and longitude result as integer tuples from the terminal, and need to be divided in order to get the correct float number
            lat_s = float(lat[2][0]/10 ** (len(str(lat[2][1]))-1))
            lon_s = float(lon[2][0] / 10 ** (len(str(lon[2][1])) - 1))
            latitude = str(int(lat[0][0])) + '°' + str(int(lat[1][0])) + '\'' + str(lat_s) + '\"' + lat_ref
            longitude = str(int(lon[0][0])) + '°' + str(int(lon[1][0])) + '\'' + str(lon_s) + '\"' + lon_ref

        link = 'https://www.google.com/maps/place/' + latitude + '+' + longitude

        return link
