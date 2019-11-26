# Cirrus IMG Viwer

## Requirements
- dash
- numpy
- pyfladesk (only if using for desktop bundle)
- pyinstaller (only if using for desktop bundle)

## Usage
For development, simply:
```
$ python app.py
```

For build for desktop, you will need to edit the dependency path for ```app.spec``` for your environment for those *.js files, which will be ignored by the Pyinstaller, for a light-weight application, it would be the best to create a new environment for building this app only with the packages only needed.

With the updated ```app.spec``` file, you may run:
```
$ pyinstaller app.spec
```