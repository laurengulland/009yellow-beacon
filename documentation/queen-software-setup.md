# Queen Software Set Up

Using Python 3.6.3 for Windows as a base.  Download Python 3.6.3 [here](https://www.python.org/downloads/release/python-363/).

## Installing Packages and Dependencies
_Note:_ if your Python 3 install uses the alias `python3`, make sure to run that instead of `python` for all of the following installations.


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
