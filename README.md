# text-recognize

--------------------------
<h1>description<h1>
This aplication can read characters from images of string. 


<h2>usage instruction<h2>

1) Run BigRedButton.py
   Now you'll see application with buttons. 

2) We have a choice:
    A) Generation data
    B) Train on it
    C) Use for recognition
    
--------------------------
A) If you need to generate data (It mean to create files classification.txt and flattened_images.txt) you need browse train picture from folder 'train' (training_chars.png) and then press button 'Generate data'. In this data stored information about classification between characters and it ascii code. When you press the button, you will see the pictures. imgTrainingData is our train picture. imgROI is image of keychar that we should press. Thus program run along all the train image, bound chars and ask us to press the corresponding key to classificate. When all chars onumage is done - generating is over. All data stored in 2 files: 
    classification.txt
    flattened_images.txt
    
B) 
