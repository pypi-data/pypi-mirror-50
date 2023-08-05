# Required with every package
# Initializes package upon import call from python
#
# ex.
# import package_name.other_python_file

import re, os


def delDotPrefix(string):
    """Delete dot prefix to file extension if present"""
    return string[1:] if string.find(".") == 0 else string


def filesInFolder(folder, fileType="*"):
    """Returns list of files of specified file type"""
    fileType = delDotPrefix(fileType)
    file_regex = re.compile(
        rf".*\.{fileType}", re.IGNORECASE
    )  # Regular Expression; dot star means find everything
    file_list = []
    for dirpath, _, filenames in os.walk(folder):  # for each folder
        for file in filenames:
            file_search = file_regex.findall(file)
            if file_search:  # if file_search is not empty
                file_list.append(dirpath + "\\" + file)
    return file_list


def replaceWords(textOrFile, dictionary):
    """Replace words in content by dictionary keys and values"""
    base_text = textOrFile
    if os.path.exists(textOrFile):
        base_text = File(textOrFile).read()
    for key, val in dictionary.items():
        try:
            base_text = base_text.replace(key, val)
        except:
            pass
    return base_text


def directoryLastValue(directory):
    """Returns the last value in the directory"""
    return directory.rsplit("\\", 1)[-1]


class File:
    def __init__(self, fileName):
        self.fileName = fileName

    def write(self, content):
        """Overwrites to file - deletes what was there before
        If file did not exist it creates a file"""

        f = open(self.fileName, "w")
        f.write(content)
        f.close()

    def append(self, content, newline=True):
        """Appends content to existing file"""

        f = open(self.fileName, "a")
        f.write("\n" + content) if newline else f.write(content)
        f.close()

    def read(self):
        """Returns existing file content"""

        f = open(self.fileName)
        t = f.read()
        f.close
        return t

    def print(self):
        """Prints existing file content"""

        print(self.read())


def importPackage(package):
    import importlib

    return importlib.import_module(package)


def packagePath(package):
    my_module = importPackage(package)
    return my_module.__file__


def packageDir(package):
    return os.path.dirname(packagePath(package))
