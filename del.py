#!/bin/python

# DEP:
# 1. PIL

from optparse import OptionParser
import os, os.path
import logging
from PIL import Image

FILENAME2 = ['item', 'list']
FILENAME = [ 'saved_resource' , 'counter3', 'counter6' , 'recommend', 'sug', 'summarydata']
HTMFILENAME = [ 'recommend', 'fetchDc', 'getMallBar', 'initItemDetail' ,
                'list_detail_rate' , 'list_dsr_info' , 'listTagClouds' , 'listTryReport',
                'seller_info', 'dealRecords', 'link' , 'activity' , 'asyn' , 'ifq',
                'validateDc', 'item_imgs' , 'promotionNew' , 'sib', 'login',
                'stp-1_1_0' ]
COUNT = 0

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


def checkfilesize(filepath):
    return 

def checkexplictfilename(filename):
    return filename in FILENAME2



def checkfilename(filename):
    for f in FILENAME:
        if f in filename :
            return True
    return False

def checkhtmfilename(filename):
    if os.path.splitext(filename)[1] == '.htm':
        for f in HTMFILENAME:
            if f in filename:
                return True
    return False

def checkimage(filename, filepath):
    if os.path.splitext(filename)[1] not in ['.jpg', '.jpeg', '.png', '.gif'] :
        return False
    im = Image.open(filepath)
    if im.size[0] < 100:
        return True
    if im.size[1] < 100:
        return True
    return False

def is_good_pic(filename):
    # These file type is not pic.
    if os.path.splitext(filename)[1] in ['.js', '.css', '.php', '.do', '.aw', 'html', 'htm' ]:
        return False

    #fixme: chinese support
    # file size must not zero
    #if os.path.getsize(filepath) == 0:
    #    return False
    
    if checkfilename(f) or checkhtmfilename(f) or checkexplictfilename(f):
        xlog( 'delete upon filename' )
        return False
    if checkimage(f, fullpath): 
        xlog( 'delete upon image resolution' )
        return False

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
        if depth is 1:
            continue
        
        # loop every files in depth 2.
        for f in files:
            fullpath = os.path.join(root, f)
            xlog("processing files in depth2 dir : " + fullpath)
            
            if is_good_pic(f):
                continue
            else:
                counter()
                os.remove(fullpath)

    xlog("files count : " + str(COUNT))
    xlog("= END =")

if __name__ == "__main__":
    main()