import gc
import os
import shutil
from datetime import datetime
from pathlib import Path

from snappy import ProductIO, GPF, jpy
from snappy import WKTReader

class imageProcess:

    def __init__(self, path):
        # Basic attributes
        self.path = path
        self.input_dir = os.getcwd()
        # Get snappy Operators
        GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
        # HashMap Key-Value pairs
        self.HashMap = jpy.get_type('java.util.HashMap')
        gc.enable()

        #self.imgpath = ProductIO.readProduct(path)
        self.timestamp = path.split('/')[-1].split('_')[6:7]
        self.coregistrationlist = []

        self.paths = {'orb':'',
                    'thermal':'',
                    'calib':'',
                    'speckle':'',
                    'terrain':'',
                    'ortho':'',
                    'decibels':'',
                    'stack':''
        }
        self.bools = {'orb':False,
                      'thermal':False,
                      'calib':False,
                      'speckle':False,
                      'terrain':False,
                      'ortho':False,
                      'decibels':False,
                      'stack':False
        }

    def getPath(self):
        return self.path

    def setPath(self, path):
        self.path = path

    def silentDelete(self, correction):
        try:
            toRemove = getattr(self, 'correction')
            os.remove(toRemove)
            os.rmdir(correction)
        except OSError:
            print('could not delete directory doesnt exists')
            pass
        except AttributeError:
            print('could not find attribute')
            pass

    def getTimestamp(self):
        return self.timestamp

    def setTimestamp(self, path):
        self.timestamp = path.split('_')[6:7]
        return self.timestamp

    def determineTimeStamp(self):
        self.timestamp = self.path.split('_')[6:7]

    def customTimeStamp(self, usertimestamp):
        # we want to set a timestamp with the given timestamp argument
        self.timestamp = usertimestamp

    def datafolder(self, cor):
        # on veut creer une fonction qui renvoie une chaine de caractere path  pour un object image
        # de type /inputdir/string_timestamp.data/
        data = ''
        try:
            dim = getattr(self, cor)
            if dim:
                data = dim.split('.')[:-1] + 'data/'
        except AttributeError:
            print('Invalid Attribute')
            pass
        return data

    def validate_step(self,step):
        if self.bools[step]:
            print(f'file already exists for {step} ')
            return False
        elif step + '_' + ''.join(self.getTimestamp())+'.dim' in os.listdir(self.input_dir):
            self.paths[step] = os.path.join(self.input_dir, step + '_' + ''.join(self.getTimestamp()))
            print(f'file has already been proccessed before ({step})')
            return False
        else:
            return True


    def applyOrbit(self):
        """
        Applying orbit correction on S1 GRD Object Image File
        """
        step = 'orb'
        if self.validate_step(step):
            # Starting parameters
            parameters = self.HashMap()
            # ---------Input
            orbit_param = GPF.createProduct("Apply-Orbit-File", parameters, ProductIO.readProduct(self.path))
            # --------Output
            self.paths[step] = os.path.join(self.input_dir, step + "_" + ''.join(self.getTimestamp()))
            ProductIO.writeProduct(orbit_param, self.paths[step], 'BEAM-DIMAP')
            print(str(self.getTimestamp()) + " is done")
            # ---------Return
            self.bools[step] = True

        return self.paths[step], self.bools[step]


    def applyThermalNoiseRemoval(self,input_from='orb'):
        """
        Applying Thermal Noise removal on S1 GRD Object Image File
        """
        step = 'thermal'
        if self.validate_step(step):
            print('\tThermal noise removal...')
            # Starting parameters
            parameters = self.HashMap()
            parameters.put('removeThermalNoise', True)
            # ---------Input
            thermal_param = GPF.createProduct("ThermalNoiseRemoval", parameters,
                                                    ProductIO.readProduct(self.paths[input_from]+'.dim'))
            # --------Output
            self.paths[step] = os.path.join(self.input_dir, step + "_" + ''.join(self.getTimestamp()))
            ProductIO.writeProduct(thermal_param, self.paths[step], 'BEAM-DIMAP')
            print(str(self.getTimestamp()) + " is done")
            # ---------Return
            self.bools[step] = True

        return self.paths[step], self.bools[step]

    def applyCalibration(self,input_from='thermal'):
        """
        Input:  Amplitude_VH, Intesity_VH, Amplitude_VV, Intensity_VV : an orbite file corrected
        output: beta0_VH, beta0_VV : a calibrated image file
        """
        step = 'calib'
        if self.validate_step(step):
            print("Now applying calibration")
            # Starting parameters
            parameters = self.HashMap()
            parameters.put('outputSigmaBand', True)
            parameters.put('outputBetaBand', True)
            parameters.put('outputGammaBand', True)
            parameters.put("outputImageScaleInDb", False)
            # ---------Input
            calib_param = GPF.createProduct("Calibration", parameters,
                                                   ProductIO.readProduct(self.paths[input_from]+'.dim'))
            # --------Output
            self.paths[step] = os.path.join(self.input_dir, step + "_" + ''.join(self.getTimestamp()))
            ProductIO.writeProduct(calib_param, self.paths[step], 'BEAM-DIMAP')
            print(str(self.getTimestamp()) + " is done")
            # ---------Return
            self.bools[step] = True

        return self.paths[step], self.bools[step]

    def applySpeckleFilter(self,input_from='calib'):
        '''

        '''
        step = 'speckle'
        if self.validate_step(step):
            print("Now applying Speckle Filtering")
            # Starting parameters
            parameters = self.HashMap()
            # parameters.put('sourceBands', 'Sigma0_VV','Sigma0_VH')
            # parameters.put('numberofLooks', 4)
            parameters.put('filter', 'Lee Sigma')
            parameters.put('windowSize', "7x7")
            parameters.put('sigma', 0.9)
            parameters.put('targetWindowSize', "5")
            # ---------Input
            Speckle_param = GPF.createProduct("Speckle-Filter", parameters,
                                                        ProductIO.readProduct(self.paths[input_from] +'.dim'))
            # --------Output
            self.paths[step] = os.path.join(self.input_dir, step + "_" + ''.join(self.getTimestamp()))
            ProductIO.writeProduct(Speckle_param, self.paths[step], 'BEAM-DIMAP')
            print(str(self.getTimestamp()) + "is done")
            # -------- Return 
            self.bools[step] = True

        return self.paths[step], self.bools[step]

    def applyTerrainCorrection(self, input_from='speckle'):
        '''

        '''
        step = 'terrain'
        if self.validate_step(step):
            print("Now applying terrain correction")
            # Starting parameters
            parameters = self.HashMap()
            # parameters.put('Source Bands', 'VV,VH')
            # parameters.put('demName', 'SRTM 3Sec')
            # parameters.put('mapProjection', proj)
            # parameters.put('externalDEMFile', 'dempath')
            # parameters.put('pixelSpacingInMeter', '10.0')
            parameters.put('demName', 'SRTM 1sec HGT')
            parameters.put('demResamplingMethod', 'BILINEAR_INTERPOLATION')
            parameters.put('additionalOverlap', 0.1)
            parameters.put('OversamplingMultiple', 1.5)

            # ---------Input
            terrain_param = GPF.createProduct("Terrain-Flattening", parameters,
                                                    ProductIO.readProduct(self.paths[input_from]+'.dim'))
            # --------Output
            self.paths[step] = os.path.join(self.input_dir, step + "_" + ''.join(self.getTimestamp()))
            ProductIO.writeProduct(terrain_param, self.paths[step], 'BEAM-DIMAP')
            print(str(self.getTimestamp()) + " is done ")
            # -------- Return 
            self.bools[step] = True

        return self.paths[step], self.bools[step]

    def applyOrthorectification(self,input_from='terrain'):
        '''
        #  Correction of geometry of object images , Input = Gamma0 terrain flattened file only
        '''
        step = 'ortho'
        if self.validate_step(step):
            print("Now applying Orthorectification")
            # Starting parameters
            parameters = self.HashMap()
            parameters.put('demResamplingMethod', 'BICUBIC_INTERPOLATION')
            parameters.put('demName', 'SRTM 1Sec HGT')
            # ---------Input
            orth_param = GPF.createProduct("Terrain-Correction", parameters,
                                                ProductIO.readProduct(self.paths[input_from]+'.dim'))
            # --------Output
            self.paths[step] = os.path.join(self.input_dir, step + "_" + ''.join(self.getTimestamp()))
            ProductIO.writeProduct(orth_param, self.paths[step], 'GeoTIFF-BigTIFF')
            print(str(self.getTimestamp()) + " is done ")
            # -------- Return
            self.bools[step] = True
        return self.paths[step], self.bools[step]

    def convertToDecibel(self,input_from='ortho'):
        '''

        '''
        step = 'decibels'
        if self.validate_step(step):
            print("Now converting to decibels")
            # Starting parameters
            parameters = self.HashMap()
            # ---------Input
            decibel_param = GPF.createProduct("LinearToFromdB", parameters,
                                                    ProductIO.readProduct(self.paths[input_from] + '.dim'))
            # -------Output
            self.paths[step] = os.path.join(self.input_dir, step + "_" + ''.join(self.getTimestamp()))
            ProductIO.writeProduct(decibel_param, self.paths[step], 'GeoTIFF-BigTIFF')
            print(str(self.getTimestamp()) + "is done")
            # -------- Return
            self.bools[step] = True
        return self.paths[step], self.bools[step]

        '''
        def converToDecibel(self):
            # We want a function wich take a object , read it into an image and the nperform convert to DB OP
            try:
                print('Converting to DB')
                # Output
                # polarisation = ''
                if 'VV' in self.path:
                    polarisation = 'VV_'
                elif 'VH' in self.path:
                    polarisation = 'VH_'
                else:
                    polarisation = ''
                output = self.input_dir + '/dB_' + polarisation + ''.join(self.getTimestamp())
                # Reading
                im = ProductIO.readProduct(self.path)
                parameters = self.HashMap()
                dbparam = GPF.createProduct("LinearToFromdB", parameters, im)
                # Writing
                ProductIO.writeProduct(dbparam, output, 'GeoTIFF')
            except OSError:
                print('Invalid')
        '''

    def stackRegistration(self):
        stacklist = []
        ProductIO.readProduct(self).append(stacklist)
        self.stack = True
        return stacklist, self.stack


    def addtoCoRegistration(self, coregistrationlist=None):
        self.coregistrationlist.append(ProductIO.readProduct(self.path))
        return self.coregistrationlist
