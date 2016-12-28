# -*- coding: utf-8 -*-
# TrainAndTest.py

import cv2
import numpy as np
import operator
import os

# module level variables ##########################################################################
MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

###################################################################################################
class ContourWithData():

    # member variables ############################################################################
    npaContour = None           # contour
    boundingRect = None         # bounding rect for contour
    intRectX = 0                # bounding rect top left corner x location
    intRectY = 0                # bounding rect top left corner y location
    intRectWidth = 0            # bounding rect width
    intRectHeight = 0           # bounding rect height
    fltArea = 0.0               # area of contour

    def calculateRectTopLeftPointAndWidthAndHeight(self):               # calculate bounding rect info
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self):                            # this is oversimplified, for a production grade program
        if self.fltArea < MIN_CONTOUR_AREA: return False        # much better validity checking would be necessary
        return True

kNearest = cv2.ml.KNearest_create()  

def LoadTest(im):
	imgTestingNumbers = cv2.imread(im)          # read in testing numbers image

	if imgTestingNumbers is None:                           # if image was not read successfully
		print "error: image not read from file \n\n"        # print error message to std out
		os.system("pause")                                  # pause so user can see error message 
	return imgTestingNumbers
	
def load_Classif(txt):
	try:
		classif = np.loadtxt(txt, np.float32)                  # read in training classifications
	except:
		print "error, unable to open %s, exiting program\n" %(txt)
		os.system("pause")
	return 	classif
			
def load_Flatt(txt):
	try:
		flatt = np.loadtxt(txt, np.float32)                 # read in training images
	except:
		print "error, unable to open %s, exiting program\n" %(txt)
		os.system("pause")
	return flatt		
	
def img2thresh(im):
	imgGray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)       # get grayscale image
	imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                    # blur

                                                        # filter image from grayscale to black and white
	imgThresh = cv2.adaptiveThreshold(imgBlurred,                           # input image
                                      255,                                  # make pixels that pass the threshold full white
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       # use gaussian rather than mean, seems to give better results
                                      cv2.THRESH_BINARY_INV,                # invert so foreground will be white, background will be black
                                      11,                                   # size of a pixel neighborhood used to calculate threshold value
                                      2)                                    # constant subtracted from the mean or weighted mean
	return imgThresh


def Contours2validContiours (npaContours):
	
	allContoursWithData = []                # declare empty lists,
	validContoursWithData = []              # we will fill these shortly
	
	# Для каждого найденного контура инициализируем переменные класса
	for npaContour in npaContours:                             # for each contour
		contourWithData = ContourWithData()                                             # instantiate a contour with data object
		contourWithData.npaContour = npaContour                                         # assign contour to contour with data
		contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)     # get the bounding rect
		contourWithData.calculateRectTopLeftPointAndWidthAndHeight()                    # get bounding rect info
		contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)           # calculate the contour area
		allContoursWithData.append(contourWithData)                                     # add contour with data object to list of all contours with data

	# добавление полученных параметров----------------------------------------------------    
	for contourWithData in allContoursWithData:                 # for all contours
		if contourWithData.checkIfContourIsValid():             # check if valid
			validContoursWithData.append(contourWithData)       # if so, append to valid contour list

	# Сортировка контуров------------------------------------------------------------------
	validContoursWithData.sort(key = operator.attrgetter("intRectX"))         # sort contours from left to right
	
	return validContoursWithData

def greenRecognize(validContoursWithData, kNearest):
	
	kNearest = TRAIN()
	
	strFinalString = ""         # declare final string, this will have the final number sequence by the end of the program
	
	imgTestingNumbers = LoadTest("test/test2.png")

	imgThresh = img2thresh(imgTestingNumbers)
	
	imgThreshCopy = imgThresh.copy()  

	# Для каждого контура -----------------------------------------------------------------
	for contourWithData in validContoursWithData:            # for each contour
                                                # draw a green rect around the current char
		cv2.rectangle(imgTestingNumbers,                                        # draw rectangle on original testing image
                      (contourWithData.intRectX, contourWithData.intRectY),     # upper left corner
                      (contourWithData.intRectX + contourWithData.intRectWidth, contourWithData.intRectY + contourWithData.intRectHeight),      # lower right corner
                      (0, 255, 0),              # green
                      2)                        # thickness

		imgROI = imgThresh[contourWithData.intRectY : contourWithData.intRectY + contourWithData.intRectHeight,     # crop char out of threshold image
                           contourWithData.intRectX : contourWithData.intRectX + contourWithData.intRectWidth]

		imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))             # resize image, this will be more consistent for recognition and storage

		npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))      # flatten image into 1d numpy array

		npaROIResized = np.float32(npaROIResized)       # convert from 1d numpy array of ints to 1d numpy array of floats

		retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 1)     # call KNN function find_nearest

		strCurrentChar = str(chr(int(npaResults[0][0])))                                             # get character from results

		strFinalString = strFinalString + strCurrentChar            # append current char to full string
	
	return strFinalString
	

def TRAIN():
	
	npaClassifications = load_Classif("classifications.txt")
	npaFlattenedImages = load_Flatt("flattened_images.txt")
	
	npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))        
	#instantiate KNN object 
	kNearest = cv2.ml.KNearest_create()                  

	kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)
	
	return kNearest
	
def TEST(kNearest):
	
	imgTestingNumbers = LoadTest("test/test2.png")

	imgThresh = img2thresh(imgTestingNumbers)
	
	imgThreshCopy = imgThresh.copy()  

	# -----------------------------------------------------------------------------------------------------
	# Находим контуры
	imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,             # input image, make sure to use a copy since the function will modify this image in the course of finding contours
                                                 cv2.RETR_EXTERNAL,         # retrieve the outermost contours only
                                                 cv2.CHAIN_APPROX_SIMPLE)   # compress horizontal, vertical, and diagonal segments and leave only their end points

	validContoursWithData = Contours2validContiours(npaContours)

	strFinalString = greenRecognize(validContoursWithData, kNearest)

	print "\n" + strFinalString + "\n"                  # show the full string

	cv2.imshow("imgTestingNumbers", imgTestingNumbers)      # show input image with green boxes drawn around found digits
	cv2.waitKey(0)                                          # wait for user key press

	cv2.destroyAllWindows()             # remove windows from memory

	
###################################################################################################
#----------------------------------____MAIN___-----------------------------------------------------
###################################################################################################

#kNearest = TRAIN()
#TEST(kNearest)
