# -*- coding: utf-8 -*-
# BigRedButton.py

import sys
import numpy as np
import cv2
import os


from Tkinter import *
from tkFileDialog import *
import fileinput
from tkMessageBox import *

MIN_CONTOUR_AREA = 100

from TrainAndTest import *

#-----------------------------------------------------------------------

kN = cv2.ml.KNearest_create()
imtest = []
imtrain = []

class GenAndTrain:
	
	def __init__(self):
		root=fra1
		#-------------BUTTONS-----------------------	
		
		# Generate data button
		self.gen_data = Button(root,
						text="Generate Data",
						width=10,height=2,
						bg="white",fg="green")
						
		# Browse test file
		self.but_browse = Button(root,
									text="Browse",
									bg="white",fg="green")
						
		# Train button
		self.but_train = Button(root,
						text="Train",
						width=30,height=5,
						bg="red",fg="green")
		
		# однострочное окно
		self.ent = Entry(root,width=20,bd=3)
		
		
		
		
		#-------------HANDLER------------------------				
		#обработчик события нажатия на кнопки мыши				
		self.gen_data.bind("<Button-1>", self._generate)
		self.but_browse.bind("<Button-1>",self.browse)
		self.ent.bind("<Return>",self.entry_ent)
		self.but_train.bind("<Button-1>",self.train)
		
		
		#-------------PACK---------------------------
		#распаковывает наши кнопки на область root
		self.gen_data.pack()
		self.but_browse.pack()
		self.ent.pack()
		self.but_train.pack()
		
		
	#-----------------FUNCTIONS----------------------
		
	def  _generate(self,event):
		execfile('GenData.py')
		
		
	def browse(self,event):
		
		global imtrain
		
		op=askopenfilename()
		im = PhotoImage(file=op)
		# initiate imtrain to our dowload 
		imtrain=im
		l = Label(root, image=im)
		self.ent.delete(0,END)
		self.ent.insert(0, op)
			
	def train(self, event):
		global kN
		
		kN = TRAIN()
		
		
	def entry_ent(self,event):
		t = ent.get()
			

class TestAndClean:
	
	def __init__(self):
		root=fra2
		#-------------BUTTONS-----------------------
		
		#Browse section
		self.but_browse = Button(root,
							text="browse test",
							width=30,height=5,
							bg='white',fg='green')
		
		self.ent = Entry(root,width=30, bd=3)
		
		# Test Recognition section(2 picture)

		
		# Recognize button
		self.but_rec = Button(root,
								text="Recognize",
								width=30,height=5,
								bg="white",fg="green")
		
		# Clean button
		self.but_clean = Button(root,
								text="Clean",
								width=30,height=5,
								bg="white",fg="green")
								
								
		#-------------HANDLER------------------------				
		#обработчик события нажатия на кнопки мыши				
		self.but_browse.bind("<Button-1>", self.browse)
		self.but_rec.bind("<Button-1>",self.rec)
		self.but_clean.bind("<Button-1>",self.clean)
		self.ent.bind('<Return>', self.entry_ent)
		
		
		#-------------PACK---------------------------
		#распаковывает наши кнопки на область root
		self.but_browse.pack()
		self.ent.pack()
		self.but_rec.pack()
		self.but_clean.pack()
		
	#-----------------FUNCTIONS----------------------

	def clean(self,event):
		
		f = open ('classification.txt','w')
		r = open ('flattened_images.txt','w')
		f.close()
		r.close()
	
	def rec(self, event):
		TEST(kN)
		
	def browse(self,event):

		op=askopenfilename()
		im = PhotoImage(file=op)
		l = Label(root, image=im)
		l.image = im
		self.ent.delete(0,END)
		self.ent.insert(0, op)
		l.pack()
	
	def entry_ent(self,event):
		t = ent.get()
								
		
#-----------------------------------------------------------------------

#----------------------___main___---------------------------------------

root = Tk()
fra1=Frame(root,width=500,height=100,bd=5)
fra2=Frame(root,width=500,height=100,bd=5)
root.title('TextRecognition_0.01')
fra1.pack(side="left")
fra2.pack(side="right")

#root.geometry('600x600')
obj0 = GenAndTrain()
obj1 = TestAndClean()

mainloop()		
