import setuptools, os, sys, re
from grtoolkit.File import directoryLastValue, name, delDotPrefix, filesInFolder
from grtoolkit.Storage import search, regexList

with open("README.md", "r") as fh:
    long_description = fh.read()

# def filesInFolder(folder, fileType):  # Returns list of files of specified file type
#     fileType = delDotPrefix(fileType)
#     file_regex = re.compile(
#         r".*\." + fileType, re.IGNORECASE
#     )  # Regular Expression; dot star means find everything
#     file_list = []
#     for _, _, filenames in os.walk(folder):  # folders, subfolders, filenames
#         for singlefile in filenames:
#             file_search = file_regex.findall(singlefile)
#             if file_search:  # if file_search is not empty
#                 file_list.append(singlefile)
#     return file_list

_, CLSfilesearch = search("pypi_flow/",depth=1,lastValue=True)
CLSfilesearch = regexList(CLSfilesearch,r"CLS_.*.py")
CLS_List = []
for file in CLSfilesearch:
    CLS_List.append(f"{name(file)[4:]} = pypi_flow.{name(file)}:main")

# NOTE: PATHS CALCULATED IN SETUP.PY NEED UNIX STYLE PATH REFERENCES WITH DIFFERENT SLASHES

setuptools.setup(
    name="pypi_flow",
    version="19.07.71",
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
    scripts=[f'cmdline\\{file}' for file in filesInFolder('cmdline/',"*")],
    entry_points={
            #   'console_scripts': ['cascade = pypi_flow.CLS_cascade:main'] # "name_of_executable = module.with:function_to_execute"
            'console_scripts': CLS_List
          },
    install_requires=[],
    include_package_data=True,
)