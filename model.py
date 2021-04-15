class ImageModel():
    def __init__(self):
        """Inits the class."""
        print('ciao')

    def get_exif_data(self):
        # TODO
        return None

def buildLink(lat, latref, lon, lonref):
    lat = tuple(lat)
    lon = tuple(lon)

    latitude = str(int(lat[0])) + '°' + str(int(lat[1])) + '\'' + str(lat[2]) + '\"' + latref
    longitude = str(int(lon[0])) + '°' + str(int(lon[1])) + '\'' + str(lon[2]) + '\"' + lonref

    link = 'https://www.google.com/maps/place/' + latitude + '+' + longitude

    return link




def processGPSData(exif):
    gps_data = exif.get('GPSInfo')

    if gps_data is not None:
        gps = gps_data
        new_gps = {}

        # https://exiftool.org/TagNames/GPS.html

        if gps.get(0) is not None:
            new_gps['GPSVersionID'] = gps.get(0)
        if gps.get(1) is not None:
            new_gps['GPSLatitudeRef'] = gps.get(1)
        if gps.get(2) is not None:
            new_gps['GPSLatitude'] = gps.get(2)
        if gps.get(3) is not None:
            new_gps['GPSLongitudeRef'] = gps.get(3)
        if gps.get(4) is not None:
            new_gps['GPSLongitude'] = gps.get(4)
        if gps.get(5) is not None:
            new_gps['GPSAltitudeRef'] = gps.get(5)
        if gps.get(6) is not None:
            new_gps['GPSAltitude'] = gps.get(6)
        if gps.get(7) is not None:
            new_gps['GPSTimeStamp'] = gps.get(7)
        if gps.get(8) is not None:
            new_gps['GPSSatellites'] = gps.get(8)
        if gps.get(9) is not None:
            new_gps['GPSStatus'] = gps.get(9)
        if gps.get(10) is not None:
            new_gps['GPSMeasureMode'] = gps.get(10)
        if gps.get(11) is not None:
            new_gps['GPSDOP'] = gps.get(11)
        if gps.get(12) is not None:
            new_gps['GPSSpeedRef'] = gps.get(12)
        if gps.get(13) is not None:
            new_gps['GPSSpeed'] = gps.get(13)
        if gps.get(14) is not None:
            new_gps['GPSTrackRef'] = gps.get(14)
        if gps.get(15) is not None:
            new_gps['GPSTrack'] = gps.get(15)
        if gps.get(16) is not None:
            new_gps['GPSImgDirectionRef'] = gps.get(16)
        if gps.get(17) is not None:
            new_gps['GPSImgDirection'] = gps.get(17)
        if gps.get(18) is not None:
            new_gps['GPSMapDatum'] = gps.get(18)
        if gps.get(19) is not None:
            new_gps['GPSDestLatitudeRef'] = gps.get(19)
        if gps.get(20) is not None:
            new_gps['GPSDestLatitude'] = gps.get(20)
        if gps.get(21) is not None:
            new_gps['GPSDestLongitudeRef'] = gps.get(21)
        if gps.get(22) is not None:
            new_gps['GPSDestLongitude'] = gps.get(22)
        if gps.get(23) is not None:
            new_gps['GPSDestBearingRef'] = gps.get(23)
        if gps.get(24) is not None:
            new_gps['GPSDestBearing'] = gps.get(24)
        if gps.get(25) is not None:
            new_gps['GPSDestDistanceRef'] = gps.get(25)
        if gps.get(26) is not None:
            new_gps['GPSDestDistance'] = gps.get(26)
        if gps.get(27) is not None:
            new_gps['GPSProcessingMethod'] = gps.get(27)
        if gps.get(28) is not None:
            new_gps['GPSAreaInformation'] = gps.get(28)
        if gps.get(29) is not None:
            new_gps['GPSDateStamp'] = gps.get(29)
        if gps.get(30) is not None:
            new_gps['GPSDifferential'] = gps.get(30)
        if gps.get(31) is not None:
            new_gps['GPSHPositioningError'] = gps.get(31)

        exif.pop('GPSInfo')
        new_exif = {}

        new_exif.update({'GPSLocation': buildLink(new_gps['GPSLatitude'], new_gps['GPSLatitudeRef'], new_gps['GPSLongitude'], new_gps['GPSLongitudeRef'])})
        new_exif.update(new_gps)
        new_exif.update(exif)

        return new_exif

    return exif
