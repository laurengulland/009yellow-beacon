# Queen Software Set Up

Using Python 3.6.3 for Windows as a base.  Download Python 3.6.3 [here](https://www.python.org/downloads/release/python-363/).

## Installing Packages and Dependencies
_Note:_ if your Python 3 install uses the alias `python3`, make sure to run that instead of `python` for all of the following installations.


First, upgrade pip (which should come preinstalled with your download of Python 3.6):
```bash
python -m pip install -U pip
```

Install selected elements of SciPy ecosystem (NumPy, SciPy, Pandas, PyTables):

```bash
python -m pip install --user numpy scipy pandas
```

Install PyGame for the simple Queen GUI:
```bash
python -m pip install --user pygame
```

## Installing PyTables and its prerequisites:

Install HDF5:
Install HDF5 for HDF Group website: [installation_link]https://www.hdfgroup.org/downloads/hdf5/
It should be noted that one must sign in in order to download this.  Signin information for the HDF Group is on our document for signin information.

Install Numexpr and Cython packages:
```bash
python -m pip install --user numexpr cython
```

Install PyTables from local .whl File:
```bash
python =m pip install --user tables-3.4.2-cp36-cp36m-win_amd64.whl
```
32-bit must be installed for the Queen tablet itself:
```bash
python =m pip install --user tables-3.4.2-cp36-cp36m-win32.whl
```
Note: This can only be done when in the root 009yellow-beacon directory.

If not running Anaconda and running Windows (i.e., Queen tablet), do some mumbo-jumbo with DLL files:
Specifically, there are DLL files in `C:\\Users\[Owner]\AppData\Roaming\Python\Lib\site-packages\tables\`.
Copy them to `C:\\Users\[Owner]\AppData\Roaming\Python\Python36\site-packages\tables\`.

This should fix the error `ImportError: Could not load any of ['hdf5.dll', 'hdf5dll.dll'], please ensure that it can be found in the system path`.  If it does not, contact John Bell.