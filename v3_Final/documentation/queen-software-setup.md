# Queen Software Set Up

Using Python 3.6.3 for Windows as a base.  Download Python 3.6.3 [here](https://www.python.org/downloads/release/python-363/).

## Installing Packages and Dependencies
_Note:_ if your Python 3 install uses the alias `python3`, make sure to run that instead of `python` for all of the following installations.

_Note 2:_ on Ubuntu, I've been running all the following commands as either `pip install PACKAGE_NAME` or `sudo apt-get install python3-PACKAGE_NAME`.

First, upgrade pip (which should come preinstalled with your download of Python 3.6):
```bash
python -m pip install -U pip
```

Install selected elements of SciPy ecosystem (NumPy, SciPy, Pandas):

```bash
python -m pip install --user numpy scipy pandas
```

Install PyGame for the simple Queen GUI:
```bash
python -m pip install --user pygame
```

Install serial for connection to Teensy (?) (I didn't actually write the part that requires this, but got an error that I needed this package, so hopefully this is correct)
```bash
python -m pip install --user serial
```

## Installing PyTables and its prerequisites (possibly out-of-date):

Install HDF5:
Install HDF5 for HDF Group website: [installation_link]https://www.hdfgroup.org/downloads/hdf5/
It should be noted that one must sign in in order to download this.  Signin information for the HDF Group is on our document for signin information.

Install Numexpr and Cython packages:
```bash
python -m pip install --user numexpr cython
```

Install PyTables from local .whl File:
```bash
python -m pip install --user tables-3.4.2-cp36-cp36m-win_amd64.whl
```
32-bit must be installed for the Queen tablet itself:
```bash
python -m pip install --user tables-3.4.2-cp36-cp36m-win32.whl
```
Note: This can only be done when in the root 009yellow-beacon directory.

If not running Anaconda and running Windows (i.e., Queen tablet), do some mumbo-jumbo with DLL files:
Specifically, there are DLL files in `C:\\Users\[Owner]\AppData\Roaming\Python\Lib\site-packages\tables\`.
Copy them to `C:\\Users\[Owner]\AppData\Roaming\Python\Python36\site-packages\tables\`.

This should fix the error `ImportError: Could not load any of ['hdf5.dll', 'hdf5dll.dll'], please ensure that it can be found in the system path`.  If it does not, contact John Bell.

## For map importing code:
Install `requests` and `pillow` (PIL fork for Python 3) packages:
```bash
python -m pip install --user requests pillow
```

# JavaScript Frontend Setup

## Install Node.js
Go to `https://nodejs.org/en/download/` and install the appropriate version of Node.js.

## Install Express
```bash
npm install express --save
```

## Install Leaflet and Accompanying Packages (LocalForage, Leaflet Offline)
```bash
npm install leaflet
```
```bash
npm install localforage leaflet.offline
```

# New Version of Python Backend: Requires
```bash
python -m pip install --user numpy scipy pandas serial pymongo
```