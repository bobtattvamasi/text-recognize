# -*- coding: utf-8 -*-
# GenData.py

import sys
import numpy as np
import cv2
import os
import string

# module level variables ##########################################################################
MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

###################################################################################################

# Загружаем Картинку с буквами
def LoadPicLett(file):
	imgTrainingNumbers = cv2.imread(file)            # read in training numbers image

	if imgTrainingNumbers is None:                          # if image was not read successfully
		print "error: image not read from file \n\n"        # print error message to std out
		os.system("pause")                                	# 
	return imgTrainingNumbers
	
def im2thresh(im):
	imgGray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)          # get grayscale image
	imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                        # blur

                                                        # filter image from grayscale to black and white
	imgThresh = cv2.adaptiveThreshold(imgBlurred,                           # input image
                                  255,                                  # make pixels that pass the threshold full white
                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       # use gaussian rather than mean, seems to give better results
                                  cv2.THRESH_BINARY_INV,                # invert so foreground will be white, background will be black
                                  11,                                   # size of a pixel neighborhood used to calculate threshold value
								   2)
	return imgThresh

								 
#--------------------------____Main____-------------------------------------------------------------
def Generate(im_train):
	
	imgTrainingNumbers = LoadPicLett(im_train)
	imgThresh = im2thresh(imgTrainingNumbers)

	#cv2.imshow("imgThresh", imgThresh)      # show threshold image for reference

	imgThreshCopy = imgThresh.copy() 

	imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,        # input image, make sure to use a copy since the function will modify this image in the course of finding contours
                                                 cv2.RETR_EXTERNAL,                 # retrieve the outermost contours only
                                                 cv2.CHAIN_APPROX_SIMPLE)           # compress horizontal, vertical, and diagonal segments and leave only their end points

	
	npaFlattenedImages =  np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

	intClassifications = []  

	# Массив символов ------------------------------------------------------------------------------------

	intValidChars = []
	
	# Create list of digits and chars
	intValidChars = list(string.digits + string.ascii_lowercase)
		
	
	#intValidChars = string.digits + string.ascii_lowercase
	
	print (intValidChars)
	
	#------------------------------------------------------------------------------------------------------

	# Около каждого контура рисуем прямоугольник
	for npaContour in npaContours:                          # for each contour
		if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:          # if contour is big enough to consider
			[intX, intY, intW, intH] = cv2.boundingRect(npaContour)         # get and break out bounding rect

                                                # draw rectangle around each contour as we ask user for input
			cv2.rectangle(imgTrainingNumbers,           # draw rectangle on original training image
                          (intX, intY),                 # upper left corner
                          (intX+intW,intY+intH),        # lower right corner
                          (0, 0, 255),                  # red
                          2)                            # thickness

			imgROI = imgThresh[intY:intY+intH, intX:intX+intW]                                  # crop char out of threshold image
			imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))     # resize image, this will be more consistent for recognition and storage

			#cv2.imshow("imgROI", imgROI)                    # show cropped out char for reference
			cv2.imshow("imgTrainingChars", imgTrainingNumbers)      # show training numbers image, this will now have red rectangles drawn on it
			cv2.imshow("imgROIResized", imgROIResized)      # show resized image for reference

			intChar = cv2.waitKey(0)                     # get key press
			print chr(intChar)
			print intChar
			
			if intChar == 27:                   # if esc key was pressed
				os.system('pause')                      # exit program
				break
				 
			elif chr(intChar).upper() in intValidChars:      # else if the char is in the list of chars we are looking for . . .
				intClassifications.append(intChar)                                              # append classification char to integer list of chars (we will convert to float later before writing to file)

				print intClassifications
				
				npaFlattenedImage = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  # flatten image to 1d numpy array so we can write to file later
				npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage,0)                    # add current flattened impage numpy array to list of flattened image numpy arrays
			
		else:
			break
			# end if
		# end if
	# end for

	# Запись в нужные файлы --------------------------------------------------------------------------

	fltClassifications = np.array(intClassifications, np.float32)                   # convert classifications list of ints to numpy array of floats

	npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))   # flatten numpy array of floats to 1d so we can write to file later

	
	print "\n\ngeneration complete !!\n"

	np.savetxt("classifications.txt", npaClassifications)           # write flattened images to file
	np.savetxt("flattened_images.txt",npaFlattenedImages)          

	cv2.destroyAllWindows()             # remove windows from memory
