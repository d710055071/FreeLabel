
import os
import natsort
from qtpy import QtGui

def getCurrentFolderImages(folderPath):
    # 获取图片格式
    extensions = [".%s" % format.data().decode().lower() for format in QtGui.QImageReader.supportedImageFormats()]
    image_list = []
    for root,dirs,files in os.walk(folderPath):
        for onefile in files:
            if onefile.lower().endswith(tuple(extensions)):
                image_list.append(os.path.join(root,onefile))
    return natsort.os_sorted(image_list)

class create_struct(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

