import datetime, sys, os, shutil
from pypi_flow import delDotPrefix, filesInFolder, directoryLastValue, File, replaceWords, packageDir

def LicenseCheck(licenseType):
    if licenseType == "":
        #Find default option listed in License Dictionary
        for k,v in LicenseDict.items(): 
            if "MIT" in v:  #DEFAULT SELECTION
                licenseType = k
    try:
        return LicenseDict[licenseType]
    except:
        print("Error: Invalid licence entry. Aborting project.")
        exit()

# UI
print("\n\nWelcome to the pypi_flow project creator!\n\nA project will be created in this directory based on the following information:\n")

projectFolder = os.getcwd() 
templateSource = packageDir("pypi_flow") + "\\packageTemplate"
licenceTemplateFolder = templateSource + '\\LicenseTemplates'

# COLLECT PROJECT INPUT FROM USER
packageName = input("package name: ")
author = input("author: ")
description = input("project description: ")
email = input("contact email: ")
url = input("project website: ")
year = str(datetime.datetime.now().year)

LicenceFiles = filesInFolder(licenceTemplateFolder)
print(LicenceFiles)
LicenseDict = {"0":"None",}
i = 1
for file in LicenceFiles:
    tempfilename = directoryLastValue(file).split(".")[0]
    LicenseDict[str(i)] = tempfilename
    i+=1

print("\nSupported project license types:")
for k,v in LicenseDict.items():
    if v == "MIT":
        print(f"{k}) {v} (Default)")
    else:
        print(f"{k}) {v}")

project_license = LicenseCheck(input('\nProceed with: '))
print(f"{project_license}\n")

# REPLACEMENT WORDS DICTIONARY
projectDictionary = {
    "$package-name$":packageName,
    "$author$":author,
    "$description$":description,
    "$email$":email,
    "$url$":url,
    "$year$":year,
}

# CREATE DIRS TO COPY INTO
packageRoot = projectFolder + f"\\{packageName}"
packageFolder = packageRoot + f"\\{packageName}"
cmdlineFolder = packageRoot + f"\\cmdline"
os.makedirs(packageRoot)
os.makedirs(packageFolder)
os.makedirs(cmdlineFolder)

# COPY ALL FILES IN FOLDER - CANNOT USE SHUTIL.COPY(folder) SINCE IT COPIES PERMISSIONS FROM SITE-PACKAGES AND CAUSES ISSUES
tocopyfilelist = filesInFolder(templateSource)
for file in tocopyfilelist:
    try:
        if "pycache" in  file:
            pass
        else:
            shutil.copyfile(file,f"{packageRoot}{file[len(templateSource):]}")
    except:
        pass

# COPY LICENSE AND PACKAGE __init__.py individually
shutil.copyfile(templateSource + '\\package_name\\__init__.py', packageFolder + '\\__init__.py')
if project_license != "None":
    shutil.copyfile(f'{licenceTemplateFolder}\\{project_license}.txt',f"{packageRoot}\\LICENSE")


# REPLACE KEY WORDS IN COPIED TEMPLATES
filelist = filesInFolder(packageRoot)
for file in filelist:
    tempfile = File(file)
    content = tempfile.read()
    content = replaceWords(content, projectDictionary)
    tempfile.write(content)