# IEViewer: a Python Image & EXIF Viewer
## Author: Paula Mihalcea
#### Università degli Studi di Firenze

---

![](https://img.shields.io/github/repo-size/paulamihalcea/IEViewer)

This project aims to build a simple, yet fully functional and failsafe (to an extent) **image and EXIF viewer** using the **Python** programming language and the **PyQt5** GUI toolkit.

**[EXIF](cipa.jp/std/documents/download_e.html?DC-008-Translation-2019-E "EXIF")** (Exchangeable Image File Format) is a standard that specifies the formats for images, sound, and ancillary tags used by digital cameras (including smartphones), scanners and other systems handling image and sound files recorded by digital cameras. The specification uses the existing file formats with the addition of specific metadata tags, which cover a broad spectrum:
- date and time information;
- camera settings, such as the camera model and make, and information that varies with each image (e.g. orientation, aperture, shutter speed, focal length, metering mode, and ISO speed information);
- a thumbnail for previewing the picture on the camera's LCD screen, in file managers, or in photo manipulation software;
- descriptions;
- copyright information.


## Contents
1. [Features](#features)
    - [Open](#open)
    - [Manipulation analysis](#manipulation-analysis)
    - [EXIF Data](#exif-data)
    - [GPS Data](#gps-data)
    - [Rotate](#rotate)
    - [Reset](#reset)
    - [Save](#save)
    - [GUI features](#gui-features)
    - [Keyboard Navigation](#keyboard-navigation)
    - [Supported file formats](#supported-file-formats)
2. [Installation](#installation)
    * [Requirements](#requirements)
3. [Usage](#usage)
4. [Technical details](#technical-details)
5. [Bibliography](#bibliography)
6. [License](#license)
    - [Disclaimer](#disclaimer)

## Features
The program features the following operations:

### Open
The user can **open** and **display an image** in one of the supported formats through a graphical user interface.
    <p align="center"><img src="https://github.com/PaulaMihalcea/IEViewer/blob/master/screenshots/open_0.png" width="50%" height="50%"></p>
    <p align="center"><img src="https://github.com/PaulaMihalcea/IEViewer/blob/master/screenshots/open_2.png" width="50%" height="50%"></p>

### Manipulation analysis
The program uses an expectation-maximization algorithm [\[1\]](https://doi.org/10.1145/3369412.3395059) [\[2\]](https://github.com/PaulaMihalcea/Photo-Forensics-from-Rounding-Artifacts) to compute a map showing where the original image has been manipulated - assuming that it has previously been tampered with.

**Note:** this feature might take some time to execute for large images, during which the program might stop responding. This does not imply malfunction; it is normal behavior, and the application will resume as soon as it has generated the manipulation map.
    <p align="center"><img src="https://github.com/PaulaMihalcea/IEViewer/blob/master/screenshots/analyze_0.png" width="50%" height="50%"></p>
    <p align="center"><img src="https://github.com/PaulaMihalcea/IEViewer/blob/master/screenshots/analyze_1.png" width="50%" height="50%"></p>

### EXIF Data
Additionally, the user can request the program to **show** any available **EXIF data** (JPEG and PNG images only).
    <p align="center"><img src="https://github.com/PaulaMihalcea/IEViewer/blob/master/screenshots/exif.png" width="50%" height="50%"></p>

### GPS Data
Whenever the EXIF data of an image also contains **GPS data**, the program processes it in order to generate a hyperlink on which the user can double-click in order to open in the browser a **[Google Maps](https://www.google.com/maps/) page centered at the GPS coordinates** contained in the EXIF data.
    <p align="center"><img src="https://github.com/PaulaMihalcea/IEViewer/blob/master/screenshots/gps_1.png" width="50%" height="50%"></p>
    <p align="center"><img src="https://github.com/PaulaMihalcea/IEViewer/blob/master/screenshots/gps_2.png" width="50%" height="50%"></p>

### Rotate
The user can **rotate** the image (180°, 90° clock wise, 90° counter clock wise).
    <p align="center"><img src="https://github.com/PaulaMihalcea/IEViewer/blob/master/screenshots/rotate_1.png" width="50%" height="50%"></p>
    <p align="center"><img src="https://github.com/PaulaMihalcea/IEViewer/blob/master/screenshots/rotate_2.png" width="50%" height="50%"></p>
    <p align="center"><img src="https://github.com/PaulaMihalcea/IEViewer/blob/master/screenshots/rotate_3.png" width="50%" height="50%"></p>

### Reset
After a rotation, the user can **reset** the image to its original orientation with the press of a single button.
    <p align="center"><img src="https://github.com/PaulaMihalcea/IEViewer/blob/master/screenshots/reset.png" width="50%" height="50%"></p>

### Save
The user can **save** the rotated image.
    <p align="center"><img src="https://github.com/PaulaMihalcea/IEViewer/blob/master/screenshots/saveas.png" width="80%" height="80%"></p>

### GUI features
All mentioned operations can be accessed from either the **tool bar** or the **menu bar**, and are accompanied by meaningful icons. Additionally, a **status bar** at the bottom of the window displays a short description for each button when hovered over.

### Keyboard Navigation
A hotkey has also been associated to each operation, implementing a **complete keyboard navigation**.

### Supported file formats
<table>
    <tr>
        <td>
            <table>
                <tr>
                    <th><b>Format</b></th>
                    <th><b>Support</b></th>
                </tr>
                <tr>
                    <td>BMP</td>
                    <td>Read/Write</td>
                </tr>
                <tr>
                    <td>GIF</td>
                    <td>Read</td>
                </tr>
                <tr>
                    <td>JPG</td>
                    <td>Read/Write</td>
                </tr>
                <tr>
                    <td>JPEG</td>
                    <td>Read/Write</td>
                </tr>
                <tr>
                    <td>PNG</td>
                    <td>Read/Write</td>
                </tr>
            </table>
        </td>
        <td>
            <table>
                <tr>
                    <th><b>Format</b></th>
                    <th><b>Support</b></th>
                </tr>
                <tr>
                    <td>PBM</td>
                    <td>Read</td>
                </tr>
                <tr>
                    <td>PGM</td>
                    <td>Read</td>
                </tr>
                <tr>
                    <td>PPM</td>
                    <td>Read/Write</td>
                </tr>
                <tr>
                    <td>XBM</td>
                    <td>Read/Write</td>
                </tr>
                <tr>
                    <td>XPM</td>
                    <td>Read/Write</td>
                </tr>
            </table>
        </td>
    </tr>
</table>

## Installation
Being a Python application, IEViewer has a few basic requirements in order to be up and running. In order to install them, the [pip](https://packaging.python.org/key_projects/#pip "pip") package installer is recommended, as it allows for the automatic installation of all requirements. Nonetheless, the latter have been listed in order to simplify an eventual manual installation.

1. Download the repository and navigate to its folder.

2. Install the requirements using `pip`:

    ```
    pip install --upgrade -r requirements.txt
    ```

### Requirements
Please note that the following versions are to be intended as minimum.

| Package | Version |
| :------------ | :------------ |
| NumPy | 1.21.2 |
| OpenCV | 4.5.3 |
| Python | 3.8 |
| Pillow | 8.2.0 |
| PyQt | 5.9.2 |

## Usage
- **Linux:** Run IEViewer from the terminal:

    ```
    python3 main.py
    ```
   
- **Windows:** You can either run IEViewer from the terminal just like on Linux, or you can modify the given `IEViewer.bat` file with the full path to your Python 3 executable and the full path to the IEViewer `main.py` script in order to create an executable link to IEViewer.

    *For example, if Python 3 has been installed to `C:\ProgramData\Anaconda3\python.exe` and `main.py` can be found in `C:\Users\Username\IEViewer\`, then the `IEViewer.bat` file will be:*

    ```
    "C:\ProgramData\Anaconda3\python.exe" "C:\Users\Username\IEViewer\main.py"
    pause
    ```

## Technical details
**IEViewer** has been programmed in the **[Python](https://www.python.org/ "Python")** language, and uses the **[PyQt5](https://riverbankcomputing.com/software/pyqt "PyQt5")** library for its graphical user interface.

It features a complete [Model View Controller](https://martinfowler.com/eaaDev/uiArchs.html#ModelViewController "Model View Controller") design pattern, partially complemented with the [Observer](https://martinfowler.com/eaaDev/MediatedSynchronization.html "Observer") pattern:
- **Model**, `model.py`: contains all the information needed to process the image and its EXIF data (if available), including the actual image object used by the other components.
- **View**, `view.py`: defines the main window's appearance and connects its buttons to controller functions; it also is a subject for the controller in the Observer pattern.
- **Controller**, `controller.py`: loads and saves the image (manages the I/O); it is an observer of the view subject.

Additional script files include:
- `observer.py`: a basic, manual implementation of the Observer design pattern;
- `widgets.py`: an overhaul of all the PyQt5 widgets used by the view, appropriately customized for this application.

A folder containing several image files suitable for testing the program (`test`) has also been included within this repository, as well as several screenshots of the running application (inside `screenshots`).

## Bibliography

[\[1\]](https://doi.org/10.1145/3369412.3395059) Shruti Agarwal and Hany Farid. 2020. **Photo Forensics From Rounding Artifacts.** In Proceedings of the 2020 ACM Workshop on Information Hiding and Multimedia Security (IH&MMSec '20). Association for Computing Machinery, New York, NY, USA, 103–114, DOI:[10.1145/3369412.3395059](https://doi.org/10.1145/3369412.3395059)

[\[2\]](https://github.com/PaulaMihalcea/Photo-Forensics-from-Rounding-Artifacts) Paula Mihalcea, **Photo Forensics from Rounding Artifacts: a Python implementation**, GitHub, 2021

[\[3\]](https://en.wikipedia.org/wiki/Exif) Wikipedia, **Exif**, 2021

## License
IEViewer is licensed under the **CC BY-NC-SA 4.0 License** (IEViewer) and the **GNU GPL v3 License** & **Riverbank Commercial License** (PyQt5). More details are available in the `LICENSE.md` file. All rights regarding the theory of the implemented algorithm reserved to the original paper's authors [\[1\]](https://doi.org/10.1145/3369412.3395059). 

EXIF info in the present `README.md` file has been adapted from [\[3\]](https://en.wikipedia.org/wiki/Exif).

### Disclaimer

Because of the nature of the EM algorithm employed for the manipulation map feature, **some manipulations will not be detected**. The author declines any responsibility regarding the correctness of the manipulation map and its meaning.
