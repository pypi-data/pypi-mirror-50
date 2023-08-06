import os

from plateNet.tools import message

image_types = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")


def imageFolder2List(basePath, ignoreFolders=None):
    # return the set of files that are valid
    return list(__list_files__(basePath, ignoreFolders=ignoreFolders))


def __list_files__(basePath, ignoreFolders):
    for (rootDir, dirNames, filenames) in os.walk(basePath):

        for filename in filenames:
            if ignoreFolders is not None and rootDir.split("/")[-1] in ignoreFolders:
                continue
            ext = filename[filename.rfind("."):].lower()

            if image_types is None or ext.endswith(image_types):
                imagePath = os.path.join(rootDir, filename)
                yield imagePath


def generateFolder(path, foldername):
    mainPath = os.path.join(path, foldername)

    if not os.path.exists(mainPath):
        os.mkdir(mainPath)
        message("{} folder generated.".format(mainPath), color.CGREEN)

    return mainPath


def generateOutputFolder(path, foldername):
    head, root = os.path.split(path)

    filename = root.split('.')[0]
    mainPath = "{}/{}".format(head, foldername)

    if not os.path.exists(mainPath):
        os.mkdir(mainPath)

    return mainPath, filename
