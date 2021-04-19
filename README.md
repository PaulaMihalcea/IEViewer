# IEViewer: a Python image & EXIF viewer
## Author: Paula Mihalcea
#### Università degli Studi di Firenze

---

![](https://img.shields.io/github/repo-size/paulamihalcea/Neural3DMM_BU3DFE)

This project aims to build a simple, yet fully functional and failsafe (to an extent), **image and EXIF viewer** using the **Python** programming language and the **PyQt5** GUI toolkit.

**[EXIF](cipa.jp/std/documents/download_e.html?DC-008-Translation-2019-E "EXIF")** (Exchangeable Image File Format) is a standard that specifies the formats for images, sound, and ancillary tags used by digital cameras (including smartphones), scanners and other systems handling image and sound files recorded by digital cameras. The specification uses the following existing file formats with the addition of specific metadata tags.

The metadata tags defined in the EXIF standard cover a broad spectrum:
- date and time information;
- camera settings, such as the camera model and make, and information that varies with each image e.g. (orientation, aperture, shutter speed, focal length, metering mode, and ISO speed information);
- a thumbnail for previewing the picture on the camera's LCD screen, in file managers, or in photo manipulation software;
- descriptions;
- copyright information.
<sub></sub(from>(adapted from [Wikipedia](https://en.wikipedia.org/wiki/Exif "Wikipedia"))</sub>

## Features
The program features the following operations:
- **Open** and **display an image** in one of the supported formats (see below)
- **Show** any available **EXIF data** (JPEG and PNG images only)
- **Rotate** the image (180°, 90° clock wise, 90° counter clock wise)
- **Reset** the image to its original orientation (if rotated)
- **Save** the rotated image*

#### Supported formats
| Format | Support |
| :------------ | :------------ |
| BMP | Read/Write |
| GIF | Read |
| JPG | Read/Write |
| JPEG | Read/Write |
| PNG | Read/Write |
| PBM | Read |
| PGM | Read |
| PPM | Read/Write |
| XBM | Read/Write |
| XPM | Read/Write |

---

## Technical details
**IEViewer** has been programmed in the **[Python](https://www.python.org/ "Python")** language, and uses the **[PyQt5](https://riverbankcomputing.com/software/pyqt "PyQt5")** library for its graphical user interface.

It features a complete [Model View Controller](https://martinfowler.com/eaaDev/uiArchs.html#ModelViewController "Model View Controller") design pattern, partially complemented with the [Observer](https://martinfowler.com/eaaDev/MediatedSynchronization.html "Observer") pattern:
- **Model**, `model.py`: contains all the information needed to process the image and its EXIF data (if available), including the actual image object used by the other components.
- **View**, `view.py`: defines the main window's appearance and connects its buttons to controller functions; it also is a subject for the controller in the Observer pattern.
- **Controller**, `controller.py`: loads and saves the image (manages the I/O); it is an observer of the view subject.

Additional script files include:
- `observer.py`: a basic, manual implementation of the Observer design pattern;
- `widgets.py`: an overhaul of all the PyQt5 widgets used by the view, appropriately customized for this application.




---

## Installation

Although the original project came with a `requirements.txt` file and some instructions for installation, they were insufficient for creating a working environment for Python 3 with Conda, especially if the desired package was the `mpi-mesh` package.

For this reason, we have written the following guide for creating a **Conda virtual environment** with **Python 3** called `Neural3DMM_BU3DFE` which can be safely used to execute this repository's code:

1. Create Conda virtual environment:

    ```
    conda create --name Neural3DMM_BU3DFE python=3.6
    conda activate Neural3DMM_BU3DFE
    ```
   
2. Install OpenDR for Python 3:
    ```
    conda install -c anaconda numpy
    git clone https://github.com/apoorvjain25/opendr-1
    pip install opendr-1/.
    rm -r opendr-1 # Or simply manually delete the cloned repo of OpenDR, as it is not needed anymore
    ```

3. Install the [MPI-IS/mesh](https://github.com/MPI-IS/mesh) library:
    ```
    conda install -c anaconda boost
    git clone https://github.com/MPI-IS/mesh
    pip install --upgrade -r mesh/requirements.txt
    pip install --no-deps --install-option="--boost-location=$$BOOST_INCLUDE_DIRS" --verbose --no-cache-dir mesh/.
    rm -r mesh # Or simply manually delete the cloned repo of MPI-IS/mesh, as it is not needed anymore
    ```
    Note: if the second `pip` command should fail, please refer to [this issue](https://github.com/MPI-IS/mesh/pull/58#issuecomment-809244983) (make sure to replace `~/anaconda3/` in the suggested solution with the path to your Anaconda 3 installation, if different).

4. Clone this repository and install its requirements:
    ```
    git clone https://github.com/PaulaMihalcea/Neural3DMM_BU3DFE
    pip install --upgrade -r Neural3DMM_BU3DFE/requirements.txt
    conda install -c pytorch pytorch
    conda install -c conda-forge trimesh
    conda install -c conda-forge tensorboardx
    pip install pyrender
    ```
   
    Note: If during execution TensorboardX should output a serialization error (`__new__() got an unexpected keyword argument 'serialized_options'`), uninstall and then reinstall Protobuf using `pip`:
    ```
    pip uninstall protobuf
    pip install -U protobuf
    ```
   If the program still does not work, or gives out a `RuntimeError: CUDA out of memory. Tried to allocate...` error, try installing version 3.6.0 of Protobuf (ignore `pip`'s warnings about package incompatibility):
    ```
    pip uninstall protobuf
    pip install -U protobuf==3.6.0
    ```

5. Finally, make sure to obtain the [BU3DFE dataset](http://www.cs.binghamton.edu/~lijun/Research/3DFE/3DFE_Analysis.html) from its authors and reorder its models according to the order specified in `data/BU3DFE/identities.txt`, then save it as `dataset.npy` in `data/BU3DFE/`. `dataset.npy` needs to contain only the models' vertices, as their triangulation (which is the same for all models) can be found in `data/BU3DFE/template/template.obj`.

## Usage

In order to run the program for the first time using the default settings (those that yield the best results), simply run `python3 main.py`.
 
Two optional arguments, `--settings` and `--mode`, allow to choose the settings file to be used and the mode (`train` or `test`), e.g.: `python3 main.py --settings my_fav_settings_file --mode train`.

Please note that, unlike the original project, `data_generation.py` does not need to be run anymore if `split_dataset = True` in the chosen settings file. The `settings` folder has been specially created in order to contain any number of settings files, thus allowing for an easier setup of the model.


The following is the original abstract of the project.
