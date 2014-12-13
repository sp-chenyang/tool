#!/bin/python

# DEP:
# 1. PIL

from optparse import OptionParser
import os, os.path
import logging
from PIL import Image
import sys
import shutil

COUNT = 0

# Decompress a WebP file to an image file, from google.
DWEBP = "E:\\opt\\libwebp-0.4.2-windows-x64\\bin\\dwebp.exe"

# store some info in readme.txt
READMETXT = "readme.txt"

def xlog(str):
    logger = logging.getLogger(__name__)
    logger.info( str )

#http://python-forum.org/viewtopic.php?f=6&t=6352
def walk_depth(root, max_depth):
    # some initial setup for getting the depth
    root = os.path.normpath(root)
    depth_offset = root.count(os.sep) - 1

    for root, dirs, files in os.walk(root, topdown=True):
        # get current depth to determine if we need to stop
        depth = root.count(os.sep) - depth_offset
        yield root, dirs, files, depth
        if depth >= max_depth:
            # modify dirs so we don't go any deeper
            dirs[:] = []

# get file path extension
# input : "c:\\a\\b\\abc.jpg"
# output : ".jpg"
def getpathext(filename):
    return os.path.splitext(filename)[1].lower()

# get file path root
# input : "c:\\a\\b\\abc.jpg"
# ouput : "c:\\a\\b\\abc"
def getpathroot(filename):
    return os.path.splitext(filename)[0]

def is_image(fullpath):
    try:
        im = Image.open(fullpath)
    except:
        xlog("file is not a image : " + fullpath)
        return False
    else:
        return im.format.lower()

def preprocessing(filename, fullpath):
    # convert webp to png.
    if getpathext(filename) == ".webp":
        cmd = DWEBP + ' ' + getpathroot(fullpath) + '.webp -o ' + getpathroot(fullpath) + '.png'
        if os.system(cmd) != 0:
            xlog("Something is wrong when changing webp format : " + filename)
            sys.exit(1)
        xlog("File is webp format, success to change format to png : " + filename)
    
    # file w/o extension, check for image format
    if getpathext(filename) == '':
        fileformat = is_image(fullpath)
        if fileformat:
            newpath = getpathroot(fullpath) + "." + fileformat
            xlog("[preprocessing] give file a extension, from " + fullpath + " to " + newpath)
            shutil.copy2(fullpath, newpath)

def is_good_pic(filename, fullpath):
    # file type must image
    if getpathext(filename) not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        return False
    
    # file size must not zero
    if os.path.getsize(fullpath) == 0:
        return False
    
    try:
        #@fixme: file type must be a image.
        im = Image.open(fullpath)
    except:
        xlog("file is not a image : " + fullpath)
    else:
        if im.size[0] < 300:
            return False
        if im.size[1] < 300:
            return False
    
    # go though test above, this file is a good image
    return True

def counter():
    global COUNT
    COUNT+=1

def initlog(log_file_path):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.FileHandler(log_file_path, 'w+')
    handler.setLevel(logging.INFO)

    # create a logging format

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger

    logger.addHandler(handler)

    #logger.info('Hello baby')
    return logger

def initcmd():
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="xdir",
                      help="dir")

    (options, args) = parser.parse_args()

    if options.xdir is None:
        parser.error("`--dir` must be given")
        exit(1)
    return options

def main():
    global COUNT

    options = initcmd()
    
    DIR = options.xdir
    
    initlog(DIR + os.path.sep + 'del.log')
    xlog( "processing root dir is : " + DIR )
    
    # loop depth must be 2
    #for root, _, files in os.walk(DIR):
    for root, _, files, depth in walk_depth(DIR, 2):
        if depth == 1:
            continue
        
        # loop every files in depth 2.
        for f in files:
            fullpath = os.path.join(root, f)
            xlog("processing files in depth2 dir : " + fullpath)
            
            preprocessing(f, fullpath)
            
            if is_good_pic(f, fullpath):
                continue
            elif f == READMETXT:
                # store some info in this file.
                continue
            else:
                counter()
                xlog("remove file : " + f)
                os.remove(fullpath)

    # backup html page
    for file in os.listdir(DIR):
        fullpath = os.path.join(DIR, file)
        if getpathext(file) != ".html" and getpathext(file) != ".htm":
            continue
        newpath = os.path.join(DIR, getpathroot(file) + "_files", READMETXT)
        xlog("[main] move html to txt, and into sub dir : from %s to %s" % (fullpath, newpath))
        shutil.move(fullpath, newpath)
        
        
    xlog("removed files count : " + str(COUNT))
    xlog("= END =")

if __name__ == "__main__":
    main()