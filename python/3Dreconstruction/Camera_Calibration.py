import argparse
import cv2
import numpy as np
import os

parser = argparse.ArgumentParser()
parser.add_argument("inputVideo",type=str) #Input video file
parser.add_argument("outputVideo",type=str) #Output Folder video frames
parser.add_argument("output",type=str) # Output of the file containing the parameters
args = parser.parse_args()

"""
Extraction des frames d'un fichier vidéo
:pathIn: chemin vers le fichier vidéo
:pathOut: chemin vers le dossier de sortie
"""
def extractFrames(pathIn, pathOut):
    os.mkdir(pathOut)
    cap = cv2.VideoCapture(pathIn)
    count = 0
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            print('Read %d frame: ' % count, ret)
            cv2.imwrite(os.path.join(pathOut, "frame{:d}.jpg".format(count)), frame)  # save frame as JPEG file
            count += 1
        else:
            break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
	
extractFrames(args.inputVideo,args.outputVideo)


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*4,3), np.float32)
objp[:,:2] = np.mgrid[0:4,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
"""
Parcours les frames du dossier
Récupère les points objet et image pour la calibration
"""
for i in range(50):
    frame = cv2.imread(args.outputVideo + "/frame"+str(i)+".jpg")
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret2, corners = cv2.findChessboardCorners(gray, (4,6),None)

    # If found, add object points, image points (after refining them)
    if ret2 == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        #img = cv2.drawChessboardCorners(frame, (4,6), corners2,ret2)
        #cv2.imshow('img',img)
        if cv2.waitKey(1) &0XFF == ord('0'):
            break
    #cv2.imshow("My cam video", gray)
    # Close and break the loop after pressing "x" key
    if cv2.waitKey(1) &0XFF == ord('0'):
        break
		
"""
Calibration de la caméra
mtxA: Matrice de la caméra intrinsèque
distA: Coefficients de distortion de la lentille
rvecsA: Vecteurs de rotation, la direction du vecteur spécifie l'axe de rotation et la magniture spécifie l'angle
tvecsA: Vecteurs de translations
"""
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

"""
Sauvegarde des paramètres de calibration
"""
np.savez(args.output, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

