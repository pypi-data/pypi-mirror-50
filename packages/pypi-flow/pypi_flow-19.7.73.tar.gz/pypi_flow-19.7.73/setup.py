import setuptools, os, sys, re
from grtoolkit.File import name, filesInFolder
from grtoolkit.Storage import search, regexList

packageName = "pypi_flow"

with open("README.md", "r") as fh:
    long_description = fh.read()

_, CLSfilesearch = search("{packageName}/",depth=1,lastValue=True)
CLSfilesearch = regexList(CLSfilesearch,r"CLS_.*.py")
CLS_List = [f"{name(file)[4:]} = {packageName}.{name(file)}:main" for file in CLSfilesearch]

# print("LOOK HERE!!!")
# print(search('cmdline/', depth=1, lastValue=True)[1])

# NOTE: PATHS CALCULATED IN SETUP.PY NEED UNIX STYLE PATH REFERENCES WITH DIFFERENT SLASHES

setuptools.setup(
    name="pypi_flow",
    version="19.07.73",
    author="Gabriel Rosales",
    author_email="gabriel.alejandro.rosales@gmail.com",
    description="Create and upload new packages to PyPI within seconds.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZenosParadox/pypi_flow",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # scripts=[f'cmdline\\{file}' for file in filesInFolder('cmdline/',"*")],
    scripts=[f'cmdline\\{file}' for file in search('cmdline/', depth=1, lastValue=True)[1]],
    entry_points={
            'console_scripts': CLS_List
          },
    install_requires=[],
    include_package_data=True,
)