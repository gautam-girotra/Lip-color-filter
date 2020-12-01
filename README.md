# Lip-color filter
Using **OpenCV**, face **landmark detection** is done and then a filter is applied to the lips.  
First I perform face detection using the **dlib library's detector** .  
Then I perform landmark detection using **shape_predictor** with a .dat file that gives 68 landmarks available [here]( https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2).    
After choosing the landmarks which represent the lips, I create a mask which singles out the lips.  
Then I change the colour of the lips and merge it with the original image.  

### This project can be used to change the colour of any part of the face by passing the respective landmark indices while calling the filter function.
