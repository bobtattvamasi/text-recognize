# text-recognize

--------------------------
<h2>Description</h2>
This aplication can read characters from images of string. 

<h2>Dependencies</h2>
   python

   opencv

   numpy

   tkinter


<h2>Usage instruction</h2>

1) Run BigRedButton.py

Now you'll see application with buttons. 

2) We have a choice:
    
    A) Generation data
    
    B) Train on it
    
    C) Use for recognition
    
--------------------------
A) If you need to generate data (It mean to create files classifications.txt and flattened_images.txt if it don't exist or if you want to generate new data from new train image), you need to browse train picture from folder 'train' (training_chars.png) and then press button 'Generate data'. When you pressed the button, you will see the pictures. imgTrainingData is our train picture with strings of chars. imgROI is image of keychar that we should press. Thus program run along all the train image, bound chars and ask us to press the corresponding key to classificate. When all chars on image is done - generating is over. All data stored in 2 files: 
    classifications.txt - contains codes of pressed keys in 1d vectors
    flattened_images.txt - contains resized to 20x30 images of croped chars from our train image in 1d vectors
    
B) So, if with data all right. We should train our classificator on k-Nearest neighbors method.

C) And now we can recognize. First browse test image from folder 'test' (or wherever you keep it) and load it. Then press button 'Recognize'. If you want to recognize the new test picture, press button 'Clean test'
