# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2
import os


from Tkinter import *

#-----------------------------------------------------------------------

class BigRedBut:
	def __init__(self):
		self.but = Button(root,
						text="Старт",
						width=30,height=5,
						bg="red",fg="green")
		self.but_1 = Button(root,
						text="Test",
						width=30,height=5,
						bg="white",fg="green")
		#обработчик события нажатия на кнопку мыши				
		self.but.bind("<Button-1>", self.starts)
		self.but_1.bind("<Button-1>", self.train)
		#распаковывает нашу кнопку на область root
		self.but.pack()
		self.but_1.pack()
		
	def  starts(self,event):
		execfile('GenDat.py')
		
	def train(self, event):
		execfile('TrainAndTest.py')
		
#-----------------------------------------------------------------------

#----------------------___main___---------------------------------------

root = Tk()
obj = BigRedBut()
mainloop()		

