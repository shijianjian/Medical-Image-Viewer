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

For cross-platform builds, it is recommand to use [docker-pyinstaller](https://github.com/cdrx/docker-pyinstaller).

## Screenshots
![screenshot](./misc/sc.png)

## Known issues
- The renderer is a bit slow. It is an issues with the ```dash``` library as well as there are six 3D cube rendering tasks. It is recommanded to use the ```Inspect Selected face``` instead of view all the faces.
- UPX is not avaliable for now.