# pypi_flow
Create and upload new packages to PyPI within seconds. 

Available on [PyPI](https://pypi.org/project/pypi-flow/). Tested on Windows 10.

## Installation
pypi-flow can installed using the folling command on your terminal:

    pip install pypi_flow

If you are using a global installation of python make sure you use:

    pip install pypi_flow --user

## Quick Start
Open the terminal on the desired directory where you would like to start a project and enter:

    waterfall.py

The following information is the collected from the user:

- package name
- author
- project description
- contact email
- project website
- license type

A project template will be created in accordance with the specifications provided.

    package_root
    │   .gitignore
    │   MANIFEST.in                 #File names added to this file will be included in the  
    │   LICENSE
    │   PipLocalUpgrade.py
    │   PypiUpload.py
    │   README.md
    │   setup.py
    │───cmdline
    │   └──...ADD CODE FILES HERE TO BE CALLED AS COMMAND LINE PROGRAMS
    └───package_name
        ├── __init__.py             #Add import references to your python code files here
        └──...ADD YOUR PYTHON CODE FILES HERE TO BE USED FROM THE PYTHON INTERPRETER UPON IMPORT

For additional changes and functionality provided beyond this template, please see setuptools documentation: https://setuptools.readthedocs.io/en/latest/setuptools.html

## Launch to Pypi

Once you are satisfied with your project folder just start the following program:

    PypiUpload.py
    
This program automatically date versions the setup.py file (using the format Year.Month.ReleaseVersion) to be newer than the package version available on the PYPI website.

Provide your PyPI account credentials when asked and enjoy the show! 

### That was easy!

Your packages should automatically install/upgrade from the PyPI website. 

Using speedy workflows and functional templates let you focus more on what matters: your code's functionality!
