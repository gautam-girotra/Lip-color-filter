import cv2
import dlib
import numpy as np

######################################################
img = cv2.imread('Rohit Sharma.png')
img = cv2.resize(img,(500,500))
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #Grayscale image should be used for detection of face and its landmarks.
color = (0,0,255) # The color you want to apply (in BGR format).
######################################################


def face_detection(gray_img):
    detector = dlib.get_frontal_face_detector()
    faces = detector(gray_img)
    return faces


def landmark_detection(faces,gray_img):
    landmark_detector = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") 
    for face in faces:
        landmarks = landmark_detector(gray_img,face)
        face_points = []
        for n in range(68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            face_points.append([x,y])
            face_points_array = np.array(face_points) # Creating an array of coordinates of the landmarks.
            #cv2.circle(img,(x,y),2,(0,0,255),2,cv2.FILLED)
            #cv2.putText(img,str(n),(x,y-10),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.5,(255,0,0),1)
            # The above two lines can be used to display the landmarks and get the indices of other parts like nose,eyes etc.
    return face_points_array


def filter(img,points,scale=5,masked=False,cropped=True):
    if masked:
        mask = np.zeros_like(img)
        mask = cv2.fillPoly(mask,[points],(255,255,255))
        img = cv2.bitwise_and(img,mask)
    if cropped:
        bounding_box = cv2.boundingRect(points)
        x,y,w,h = bounding_box
        cropped_part = img[y:y+h,x:x+w]
        cropped_part = cv2.resize(cropped_part,(0,0),None,scale,scale)
        return cropped_part
    else:
        return mask


faces = face_detection(img_gray)
face_landmarks = landmark_detection(faces,img_gray)
img_lips = filter(img,face_landmarks[49:61],3,masked=True,cropped=False)


img_color_lips = np.zeros_like(img_lips)
img_color_lips[:] = color  # Creating a fully colored image of the color selected .
img_color_lips = cv2.bitwise_and(img_lips,img_color_lips)  # Getting colored lips.
img_color_lips = cv2.GaussianBlur(img_color_lips,(7,7),10) # Blurring to get better effect on merging.

final_image = cv2.addWeighted(img,1,img_color_lips,0.4,0)  # Merging with original image.
# Can work around with the weight of img_color_lips to get the best desired effect.

cv2.imshow("Lips",img_lips)
cv2.imshow("Original Image",img)
cv2.imshow("FINAL IMAGE",final_image)

cv2.imwrite("Mask.png",img_lips)
cv2.imwrite("FINAL IMAGE.png" ,final_image)
cv2.imwrite("Original Image Resized.png",img)

cv2.waitKey(0)