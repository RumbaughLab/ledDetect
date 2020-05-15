import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import time 
from scipy.signal import find_peaks

def detectLED(file, myDir, startY=400, endY=439, startX=354, endX=400,  startTime=0):

    """function to be able to identify LED turning on based on finding peak of mean intensity
    based on a define area determined by pixel dimension
    One approach could be to list all the pixel dimension for locating the led store them 
    and then recover them from the stored file (these could be used as ground truth) and pass them in the parameters 
    startY, endY, startX, endX

    Return:
    	meanFrame (timeseries of average intensity of frames)
    	save the meanFrame timeseries to numpy array

    Parameters:
        file (list): list of file to inpute 
        startTime (int): default to 0 could be further expanded to process  only segment of video
        startY (int): pixel value of the area of interest to extract 'top left corner' Y coordinates 
        endY (int): pixel value of the area of interest to extract 'bottom right corner' Y coordinates
        startX (int): pixel value of the area of interest to extract 'top left corner' X coordinates 
        endX (int): pixel value of the area of interest to extract 'bottom right corner' X coordinates
     """

	# print the file being processed
	print(file)
	# create output directory
	os.makedirs(myDir, exist_ok=True)

	# extract the animal id/file id from the file path
	aid=os.path.splitext(file)[0]
	aid=aid.split('/')
	aid=aid[-1]

	# load the video file to be working with
	vcap = cv2.VideoCapture(file)
	fps=int(vcap.get(5)) # frame rate of video acquisition 
	vcap.set(1,fps*startTime*60) # set the first frame of video to work on

	# initialize variable to store the mean intensity of each frame
	meanFrame=[]
	while True:
		# read the frame
		ret, frame = vcap.read()
		# height, width, layers = frame.shape
		frame=frame[startY:endY, startX:endX] #cropping criteria 

		## to show and display the frames 
		# cv2.imshow('Frame',frame)
		# if cv2.waitKey(25) & 0xFF == ord('q'):
	    #    break

	    # mean frame
		meanFrame.append(np.mean(frame))

		## if restriction apply 
		if len(meanFrame) >= vcap.get(7): # limit the analysis on the first 300 frames of video
			break
			vcap.release()

	# normalize the signal 
		
	np.save(myDir+'/'+aid, meanFrame)
	return meanFrame


###################################################
# options for signal processing to be implemented
###################################################

# Peaks strategy - least prefered
	# normalize meanFrame
	meanFrame -= np.mean(meanFrame)
	# distance is calculated based on at least 40 second between shock
	peaks, _ = find_peaks(meanFrame, distance=40*fps, height=10) 
	# remove peaks detected before 2min
	peaks=peaks[peaks>=2*60*fps]

# Threshold strategy
	# normalize meanFrame
	meanFrame -= np.mean(meanFrame)
	# see implementation with what was usded by Seth for likelihood detection
	# threshodl should be based on std 
	# the threshold cut of may need to be adjusted based on signal to noise
	threshold=np.std(meanFrame)*2
	meanFrame=np.where(meanFrame<=threshold, 0, meanFrame)
	meanFrame=np.where(meanFrame>0, 1, meanFrame)

#potential other filter


###################################################
# options for diagnostic plot
###################################################

# 	## generate graphical output
# 	plt.plot(meanFrame)
# 	plt.plot(tt)
# 	plt.xlabel('Frame index')
# 	plt.ylabel('Mean intensity')
# 	plt.tight_layout()
# 	plt.plot(peaks, meanFrame[peaks], "x")
# 	# plt.show(block=False)
# 	# plt.pause(1)
# 	# plt.savefig(myDir+'/'+aid+".png")
# 	# plt.close()


# 	np.savetxt(myDir+'/'+aid+'.txt', peaks, delimiter=',')   # X is an array

# 	# return peaks
# 	print(peaks)


# # run the funciton
# startTime=0
# startY=400
# endY=439
# startX=354
# endX=400
# file='C:/Users/Windows/Desktop/output/628shock.mp4'
# myDir='C:/Users/Windows/Desktop/output'

# detectLED(file, myDir)


