# -*- coding: utf-8 -*-
# BigRedButton.py

import sys
import numpy as np
import cv2
import os
import logging


from Tkinter import *
from tkFileDialog import *
import fileinput
from tkMessageBox import *

from TrainAndTest import *
from GenData import *

#-----------------------------------------------------------------------

kN = None
MIN_CONTOUR_AREA = 100
imtest = []
imtrain = []

logging.basicConfig(
			level=logging.DEBUG,
			format='%(asctime)s : %(levelname)s : %(massage)s')


class GenAndTrain:
	
	def __init__(self):
		
		fra=fra1
		
		#-------------BUTTONS-----------------------	
		
		# Generate data button
		self.gen_data = Button(fra,
						text="Generate Data",
						width=10,height=2,
						bg="white",fg="green")
						
		# Browse test file
		self.but_browse = Button(fra,
									text="Browse",
									bg="white",fg="green")
						
		# Train button
		self.but_train = Button(fra,
						text="Train",
						width=30,height=5,
						bg="red",fg="green")
		
		# однострочное окно
		self.ent = Entry(fra,width=20,bd=3)
		
		# exit
		self.but_exit = Button(fra,
								text="Exit",
								width=10,height=2,
								bg="white",fg="green",command=quit)
								
								
		#------------PACK----------------------------
		self.gen_data.pack()
		self.but_browse.pack()
		self.ent.pack()
		self.but_train.pack()
		self.but_exit.pack()
		
		
		
		#-------------HANDLER------------------------				
		#обработчик события нажатия на кнопки мыши				
		self.gen_data.bind("<Button-1>", self._generate)
		self.but_browse.bind("<Button-1>",self.browse)
		self.ent.bind("<Return>",self.entry_ent)
		self.but_train.bind("<Button-1>",self.train)
		#self.but_train.bind("<Button-1>",self.but_quit)
		
		
		
	#-----------------FUNCTIONS----------------------
	
	def but_quit(self,event):
		root.destroy()
		
	def _generate(self,event):
		
		if not imtrain:
			showwarning("ERROR", "train image not read from file \n\nfirst load it")
			os.system("pause")         
		else:
			Generate(imtrain)
			print imtrain
		
	def browse(self,event):
		
		global imtrain
		
		op=askopenfilename()
		im = PhotoImage(file=op)
		# initiate imtrain to our dowload 
		imtrain=op.encode('utf-8')
		l = Label(root, image=im)
		self.ent.delete(0,END)
		self.ent.insert(0, op)
			
	def train(self, event):
		
		global kN
		
		kN = TRAIN()
		
		if kN is None:
			showwarning("ERROR", "image not read from file \n\nfirst load it")
			os.system("pause")
		
		if os.stat("classifications.txt").st_size == 0 and os.stat("flattened_images.txt").st_size == 0:
			showwarning("ERROR", "can't read data from text file \n\nfirst generate it")
			os.system("pause")
		
		
	def entry_ent(self,event):
		t = ent.get()

			

class TestAndClean:
	
	def __init__(self):
		
		fra=fra2
		
		#-------------BUTTONS-----------------------
		
		#Browse section
		self.but_browse = Button(fra,
							text="browse test",
							width=30,height=5,
							bg='white',fg='green')
		
		self.ent = Entry(fra,width=30, bd=3)
		
		# Test Recognition section(2 picture)

		
		# Recognize button
		self.but_rec = Button(fra,
								text="Recognize",
								width=30,height=5,
								bg="white",fg="green")
		
		# Clean button
		self.but_clean = Button(fra,
								text="Clean",
								width=30,height=5,
								bg="white",fg="green")
								
		#Text space
		self.text = Text(fra3,font='Arial 14',wrap=WORD)
								
		#------------PACK----------------------------
		self.but_browse.pack()
		self.ent.pack()
		self.but_rec.pack()
		self.but_clean.pack()
		#self.text.pack(side=BOTTOM)
								
														
								
		#-------------HANDLER------------------------				
		#обработчик события нажатия на кнопки мыши				
		self.but_browse.bind("<Button-1>", self.browse)
		self.but_rec.bind("<Button-1>",self.rec)
		self.but_clean.bind("<Button-1>",self.clean)
		self.ent.bind('<Return>', self.entry_ent)
		
		
	#-----------------FUNCTIONS----------------------

		
	def clean(self,event):
		
		pass
		"""
		f = open ('classification.txt','w')
		r = open ('flattened_images.txt','w')
		f.close()
		r.close()
		"""
	
	def rec(self, event):
		
		#if you don't browse image
		if not imtest:
			
			showwarning("ERROR", "image not read from file \n\nfirst load it")
			os.system("pause")
		
		#if you don't train	
		elif not(kN):
			
			showwarning("ERROR", "First need to train!\n\n")
			os.system("pause")
			         
		else:
			TEST(imtest, kN)
		
	def browse(self,event):
		
		global imtest
		
		op = askopenfilename()
		imtest = op.encode('utf-8')
		im = PhotoImage(file=op)
		l = Label(fra3, image=im)
		l.image = im
		self.ent.delete(0,END)
		self.ent.insert(0, op)
		l.pack(side=TOP)
	
	def entry_ent(self,event):
		t = ent.get()
								
		
#-----------------------------------------------------------------------

#----------------------___main___---------------------------------------

root = Tk()
fra1=Frame(root,width=500,height=100,bd=5)
fra2=Frame(root,width=500,height=100,bd=5)
fra3=Frame(root,width=500,height=100,bd=5)
root.title('TextRecognition_0.01')
fra1.pack(side="left")
fra2.pack(side="right")
fra3.pack(side="right")

#root.geometry('600x600')
obj0 = GenAndTrain()
obj1 = TestAndClean()

mainloop()		
