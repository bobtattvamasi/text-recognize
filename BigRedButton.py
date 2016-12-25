# -*- coding: utf-8 -*-
# BigRedButton.py

import sys
import numpy as np
import cv2
import os


from Tkinter import *

MIN_CONTOUR_AREA = 100

#-----------------------------------------------------------------------

class BigRedBut:
	def __init__(self):
		
		#-------------BUTTONS-----------------------
		# Train button
		self.but_train = Button(root,
						text="Старт",
						width=30,height=5,
						bg="red",fg="green")
		
		# Testing button
		self.but_test = Button(root,
						text="Test",
						width=30,height=5,
						bg="white",fg="green")
		# Clean button
		self.but_clean = Button(root,
								text="Clean",
								width=30,height=5,
								bg="white",fg="green")
		# Recognize button
		self.but_rec = Button(root,
								text="Recognize",
								width=30,height=5,
								bg="white",fg="green")
		
		#-------------HANDLER------------------------				
		#обработчик события нажатия на кнопки мыши				
		self.but_train.bind("<Button-1>", self.test)
		self.but_test.bind("<Button-1>", self.train)
		self.but_clean.bind("<Button-1>",self.clean)
		self.but_rec.bind("<Button-1>",self.rec)
		
		#-------------PACK---------------------------
		#распаковывает наши кнопки на область root
		self.but_train.pack()
		self.but_test.pack()
		self.but_clean.pack()
		self.but_rec.pack()
		
		
	def  test(self,event):
		execfile('GDat.py')
		
	def train(self, event):
		execfile('TrainAndTest.py')
	
	def clean(self,event):
		pass
	
	def recognize(self,event):
		pass
	
	def rec(self, event):
		pass			
#-----------------------------------------------------------------------

#----------------------___main___---------------------------------------

root = Tk()
obj = BigRedBut()
mainloop()	
