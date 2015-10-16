# Pythonmidas

Pythonmidas is a python package that allows easy access to the MIDAS ODB.

# Installation

We want to install the package in the local repository under the verions of python that we use on the DAQ machines.

On titan01: 

* python2.6 setup.py install --prefix=$HOME/.local
* python2.7 setup.py install --prefix=$HOME/.local
            
python2.7 is shared between titan01 and lxmpet

# Usage

Once Pythonmidas is installed, it can be imported and use as:

    import pythonmidas.pyhonmidas as Midas
    Midas.sendmessage("YOUR NAME", "My first pythonmidas message.")

This will send "[YOUR NAME, USER] My first pythonmidas message." to the MIDAS message stream.

# Tests

Once the package is installed, you can run the tests suite using the command:

    ~/.local/bin/nosetests --with-coverage --cover-package=pythonmidas

This uses nose to run the tests in the "test/" directory. The argument "--with-coverage" checks to see if each line of code is tested in the test script, and the argument "--cover-package=pythonmidas" displays the coverage data for the pythonmidas package.
