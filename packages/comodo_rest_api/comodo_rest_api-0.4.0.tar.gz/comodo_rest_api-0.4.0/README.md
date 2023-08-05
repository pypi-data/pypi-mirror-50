# comodo_rest_api
This library provides a simpler restful API interface to Comodo/Sectigo's REST API.

## Installation:
This program forgoes using setuptools for [flit](https://pypi.org/project/flit/) so
flit must first be installed in order to install ddi. 

To install flit and comod_rest_api local to your user, in the ddi base directory run:

    pip install --user flit
    flit install --user 

### Development Installation:
To install comodo_rest_api in a development environment
[pipenv](https://pypi.org/project/pipenv/) must first be installed. After pipenv
is installed setup the environment and then run flit to symlink in the library
like so:

    pipenv install --dev
    pipenv shell
    flit install --symlink 
    
After that is done you will have a vitrualenv with the required library installed.

## Release Procedure
Releasing means pushing the library to pypi

1. Bump __version__ in comodo_rest_api/__init__.py
2. git tag -s <version>
3. Update the change log in History.rst
4. run: flit build
5. run: flit publish
