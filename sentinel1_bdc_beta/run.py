import gc
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from snappy import ProductIO, GPF, jpy
from snappy import WKTReader


from .process import imageProcess
from .utils import imageSearch, createS1Imglist, createstack
# Working directory
#input_dir = '/s1-preprocess-docker/preprocess-s1/'
#sys.argv[1]


# Get snappy Operators
GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
# HashMap Key-Value pairs
HashMap = jpy.get_type('java.util.HashMap')
gc.enable()
#images_list = []
#s1list = []

def start(inputfolder=''):
    '''

    '''
    os.chdir(inputfolder)
    os.getcwd()
    s1list, images_list = createS1Imglist(inputfolder=inputfolder,extension='zip')
    for s1img in s1list:
        if isinstance(s1img, imageProcess):
            # Check if it is an object image
            s1img.applyOrbit()
            s1img.applyThermalNoiseRemoval(input_from='orb')
            s1img.applyCalibration(input_from='thermal')
            s1img.applySpeckleFilter(input_from='calib')
            #s1img.applyTerrainCorrection(input_from='speckle')
            s1img.applyOrthorectification(input_from='speckle')
            #s1img.applyOrthorectification(input_from='terrain')
            #s1img.convertToDecibel(input_from='ortho')

#run(inputfolder=input_dir)


def Run_CoRegistration(inputfolder=''):
    '''
    '''
    print('starting Step 2 , CoRegistration')
    os.chdir(inputfolder)
    os.getcwd()
    s1list, images_list = createS1Imglist(inputfolder=inputfolder,extension='zip')
    stackVV = []
    stackVH = []
    # We are looking for image to stack, and we need those which are not stacked
    for s1img in s1list:
        if not s1img.stack:
            # stackVV.append(ProductIO.readProduct(getattr(s1img, 'VVorthoCorrFile')))
            stackVH.append(ProductIO.readProduct(getattr(s1img, 'VHorthoCorrFile')))
            s1img.stack = True
    createstack('VV', stackVV)
    createstack('VH', stackVH)
