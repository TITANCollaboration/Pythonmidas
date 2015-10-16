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
