# A* Path Planning Package
# Overview
This is a simple package to plan a path for a quadcopter. It exposes 2 methods

1) Set barriers
2) Get Path

# Installation

Requires:
- Python 3.6
- pip
- python venv

## Linux & windows & MacOS environments
1) Create a python virtual environment somewhere in your documents. Run the Instructions below OR follow this guide https://docs.python.org/3/tutorial/venv.html

  a) Run this command `python3 -m venv venvName` to create a python3 virtual environment.

  b) Run this command cd `venvName` to move into the virtual environement.

  c)
  
    i. (Linux only, required)Run this command source `myenv\Scripts\activate` to source the virtual environment's python installation. Your terminal should now show your venvName before each line.
    
    ii. (Windows only, required)Run this command source `bin/activate` to source the virtual environment's python installation. Your terminal should now show your venvName before each line.

  2) Install the requried pip packages. Run the Instructions below

  a) (Linux only, optional)Run this command `which pip`. Make sure the output points to a file that is in your venv.

  b) Run this command `pip install matplotlib numpy` to install the required packages.
  
## How to use in CopterMove script

### Steps

  1) Test the script
    a) Run the script
    b) Make sure that the output on the graph looks good
  
  2) Package into a library and upload to the "Pypi" library repository; full documentation is here https://packaging.python.org/tutorials/packaging-projects/
    a) `python3 setup.py sdist bdist_wheel`
    b) `pip install twine`
    c) Increment the version number in `setup.py`
    c) `twine upload dist/*`
    
  3) Install this library in the CopterMove script
    a) Step `3)a)` here https://github.com/kholysa/CopterMove#linux-and-macos-environments 
