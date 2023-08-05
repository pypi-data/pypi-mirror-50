import setuptools, os, sys, re
from grtoolkit.File import directoryLastValue

with open("README.md", "r") as fh:
    long_description = fh.read()

def delDotPrefix(string):
    '''Delete dot prefix to file extension if present'''
    return string[1:] if string.find(".") == 0 else string

def filesInFolder(folder, fileType):  # Returns list of files of specified file type
    fileType = delDotPrefix(fileType)
    file_regex = re.compile(
        r".*\." + fileType, re.IGNORECASE
    )  # Regular Expression; dot star means find everything
    file_list = []
    for _, _, filenames in os.walk(folder):  # folders, subfolders, filenames
        for singlefile in filenames:
            file_search = file_regex.findall(singlefile)
            if file_search:  # if file_search is not empty
                file_list.append(singlefile)
    return file_list

def search(rootFolder, viewPrint=False, rootInclude=False, depth=None, abs=True, lastValue=False):
    '''USAGE: 
folders, files = search(path, depth=None, abs=False)

PURPOSE
Application tool for os.walk

ARGUMENTS:
    viewPrint - print to console parent folder, subfolder, and files that search() is encountering
    rootInclude - include root search folder in the output folder search results
    depth - how many levels of folders should the program output, default is no limit
    abs - output absolute or relative paths. Default is absolute path.'''

    files_recursive = list()
    folders_recursive = list()
    rootBaseDepth = rootFolder.count("\\")
    rootFolderLength = len(rootFolder)
    removeStartSlashes = lambda x: x[1:] if x[:1] =='\\' else x

    if rootInclude:
        folders_recursive = [f"{rootFolder}"] if abs else [f"{directoryLastValue(rootFolder)}"]

    for root, subfolders, files in os.walk(rootFolder):

        #CHECK/COMPARE DEPTHS
        depth_current = root.count("\\") - rootBaseDepth + 1
        if depth:
            if depth < depth_current:
                break #breaks out of for loop

        if viewPrint:
            print("Parent Directory:"); print(root)
            print("Subfolders:"); print(subfolders)
            print("Files"); print(files); print("\n")

        if abs: #absolute paths
            files_recursive = files_recursive + list(map(lambda x:f"{root}\\{x}",files))
            folders_recursive = folders_recursive + list(map(lambda x:f"{root}\\{x}",subfolders))
        else:   #relative paths
            files_recursive = files_recursive + list(map(lambda x:removeStartSlashes(root[rootFolderLength:] + '\\' + x) ,files))
            folders_recursive = folders_recursive + list(map(lambda x: removeStartSlashes(root[rootFolderLength:] + '\\' + x) ,subfolders))

        if lastValue:
            files_recursive = list(map(lambda x:directoryLastValue(x),files_recursive))
            folders_recursive = list(map(lambda x:directoryLastValue(x),folders_recursive))

    return folders_recursive, files_recursive

def regexList(unfilteredList, regex):
    '''Returns list filtered by regex'''
    item_regex = re.compile(regex, re.IGNORECASE)  # Regular Expression; dot star means find everything
    filteredList = list()
    for item in unfilteredList:
        filtering = item_regex.findall(item)
        if filtering:
            filteredList.append(item)
    return filteredList

def name(path):
    '''Extracts file name without extension'''
    return path[: path.rfind(".", 0)]

_, CLSfilesearch = search("pypi_flow/",depth=1,lastValue=True)
CLSfilesearch = regexList(CLSfilesearch,r"CLS_.*.py")
CLS_List = []
for file in CLSfilesearch:
    CLS_List.append(f"{name(file)[4:]} = pypi_flow.{name(file)}:main")

# NOTE: PATHS CALCULATED IN SETUP.PY NEED UNIX STYLE PATH REFERENCES WITH DIFFERENT SLASHES

setuptools.setup(
    name="pypi_flow",
    version="19.07.70",
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