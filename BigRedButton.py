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

from TrainAndTest import *
from GenData import *

#-----------------------------------------------------------------------

kN = None
Image_label = None
MIN_CONTOUR_AREA = 100
imtest = []
imtrain = []


# Class for packing Buttons: Generate, Train
 
class GenAndTrain:
	
	def __init__(self):
		
		fra=fra1
		
		# A litle frame for wrowse section
		browse_frame = Frame(fra,width=30,height=5,bd=5)
		
		#-------------BUTTONS-----------------------	
		
		# Generate data button
		self.gen_data = Button(fra,
						text="Generate Data",
						width=30,height=5,
						bg="white",fg="green")
						
		# Browse test file
		self.but_browse = Button(browse_frame,
									text="Browse",
									bg="white",fg="green")
						
		# Train button
		self.but_train = Button(fra,
						text="Train",
						width=30,height=5,
						bg="red",fg="green")
		
		# однострочное окно
		self.ent = Entry(browse_frame,width=20,bd=3)
		

		#------------PACK----------------------------
		self.gen_data.pack()
		browse_frame.pack()
		self.but_browse.pack(side=LEFT)
		self.ent.pack(side=RIGHT)
		self.but_train.pack()
		
		
		
		#-------------HANDLER------------------------				
		# Обработчик события нажатия на кнопки мыши				
		self.gen_data.bind("<Button-1>", self._generate)
		self.but_browse.bind("<Button-1>",self.browse)
		self.ent.bind("<Return>",self.entry_ent)
		self.but_train.bind("<Button-1>",self.train)
		
		
		
	#-----------------FUNCTIONS----------------------
	
	def _generate(self,event):
		
		if not imtrain:
			showwarning("ERROR", "train image not read from file \n\nfirst load it")
			os.system("pause")         
		else:
			showinfo('Attention', """In subsequent steps you need to press all keys/ 
that you'll see on images with title "imgRoiResized" \n\nRelax, it doesn't take a lot of time\n\n
If you want to return in menu press "Esc" """)
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
			showwarning("ERROR", "can't read data from text file \n\nfirst generate it	")
			os.system("pause")
		
		if os.stat("classifications.txt").st_size == 0 and os.stat("flattened_images.txt").st_size == 0:
			showwarning("ERROR", "can't read data from text file \n\nfirst generate it")
			os.system("pause")
		
		
	def entry_ent(self,event):
		t = ent.get()
			

# Class for packing buttons Test and clean
class TestAndClean:
	
	def __init__(self):
		
		fra=fra2
		
		#-------------BUTTONS-----------------------
		
		# Browse section
		browse_frame = Frame(fra, width=30, height=5)
		
		self.but_browse = Button(browse_frame,
							text="browse test",
							bg='white',fg='green')
		
		self.ent = Entry(browse_frame,width=20, bd=3)
		

		
		# Recognize button
		self.but_rec = Button(fra,
								text="Recognize",
								width=30,height=5,
								bg="white",fg="green")
								
								
		#Text space
		self.text = Text(fra3,font='Arial 14',wrap=WORD)
		
		# exit
		self.but_exit = Button(fra,
								text="Exit",
								width=30,height=5,
								bg="white",fg="green",command=quit)
		
		# Clean button
		self.but_clean = Button(fra,
								text="Clean test",
								width=30,height=5,
								bg="white",fg="green")
								
		#------------PACK----------------------------
		browse_frame.pack()
		self.but_browse.pack(side=LEFT)
		self.ent.pack(side=RIGHT)
		self.but_rec.pack()
		#self.text.pack(side=BOTTOM)
		self.but_clean.pack()
		self.but_exit.pack()
								
														
								
		#-------------HANDLER------------------------				
		#обработчик события нажатия на кнопки мыши				
		self.but_browse.bind("<Button-1>", self.browse)
		self.but_rec.bind("<Button-1>",self.rec)
		self.ent.bind('<Return>', self.entry_ent)
		self.but_clean.bind("<Button-1>",self.clean)
		
		
	#-----------------FUNCTIONS----------------------

		
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
	
	# Browse test image	
	def browse(self,event):
		
		global imtest, Image_label
		
		op = askopenfilename()
		imtest = op.encode('utf-8')
		im = PhotoImage(file=op)
		Image_label = Label(fra3, image=im)
		Image_label.image = im
		self.ent.delete(0,END)
		self.ent.insert(0, op)
		Image_label.pack(side=TOP)
	
	def entry_ent(self,event):
		t = ent.get()
		
	
	# Clean frame	
	def clean(self,event):
		
		
		if Image_label.image is None:
			
			showwarning("ERROR", "image not read from file \n\nfirst load it")
			os.system("pause")
		
		Image_label.image.blank()
		Image_label.image = None
		
	
								
		
#-----------------------------------------------------------------------

#----------------------___main___---------------------------------------

root = Tk()

# Frame for burrons: browse train image, generate data and train on it
fra1=Frame(root,width=500,height=100,bd=5)

# Frame for showing picture and recognized text
fra2=Frame(root,width=500,height=100,bd=5)

# Frame for buttons: browse test image, recognize it, clean image from
# frame2 and Exit
fra3=Frame(root,width=500,height=100,bd=5)

root.title('TextRecognition_0.01')

# Frame packs
fra1.pack(side="left")
fra2.pack(side="right")
fra3.pack(side="right")

#root.geometry('600x600')
obj0 = GenAndTrain()
obj1 = TestAndClean()

mainloop()		
