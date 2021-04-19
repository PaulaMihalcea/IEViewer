from PIL import ImageQt, ExifTags
# TODO documentazione

class ImageModel():
    def __init__(self):
        """Inits the class."""
        self.image = None
        self.exif_data = None
        self.filename = None
        self.modified_image = None

    def set_image(self, image):
        self.image = image

    def set_modified_image(self, modified_image):
        self.modified_image = modified_image

    def load_image(self, image, filename):
        self.filename = filename
        self.image = ImageQt.ImageQt(image)
        self.modified_image = self.image

        if image._getexif() is not None:
            self.exif_data = {ExifTags.TAGS[k]: v for k, v in image._getexif().items() if k in ExifTags.TAGS}
            self.set_gps_data()

    def close_image(self):
        self.image = None
        self.exif_data = None
        self.filename = None

    def set_gps_data(self):
        exif_data_gps = self.process_gps_data()

        if exif_data_gps is not None:
            self.exif_data = exif_data_gps
        else:
            return

    def process_gps_data(self):
        exif_data = self.exif_data
        gps_data = self.exif_data.get('GPSInfo')

        if gps_data is not None:
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

            exif_data.pop('GPSInfo')

            exif_data_updated = {}  # Contains the original EXIF data + the new GPS EXIF data

            exif_data_updated.update({'GPSLocation': self.build_gmaps_link(gps_data_dict['GPSLatitude'], gps_data_dict['GPSLatitudeRef'], gps_data_dict['GPSLongitude'], gps_data_dict['GPSLongitudeRef'])})
            exif_data_updated.update(gps_data_dict)
            exif_data_updated.update(exif_data)

            return exif_data_updated
        else:
            return None

    def build_gmaps_link(self, lat, lat_ref, lon, lon_ref):
        lat = tuple(lat)
        lon = tuple(lon)

        latitude = str(int(lat[0])) + '°' + str(int(lat[1])) + '\'' + str(lat[2]) + '\"' + lat_ref
        longitude = str(int(lon[0])) + '°' + str(int(lon[1])) + '\'' + str(lon[2]) + '\"' + lon_ref

        link = 'https://www.google.com/maps/place/' + latitude + '+' + longitude

        return link
