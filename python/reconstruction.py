import numpy as np
import cv2
from itertools import *
from more_itertools import *


class Reconstructor:
	def __init__(self,params):
		self.cParams = params

	def reconstruct(self,*positions):
		undist = []
		for position,param in zip(positions,self.cParams):
			if position and param:
				pass # Format is unclear, skipping for now
				# point = cv2.undistortPoints(position,param['mtx'],param['dist'])
				# projmat = np.column_stack((
				# 	cv2.Rodrigues(param['rvecs'][0])[0],
				# 	param['tvecs'][0]
				# ))
				# undist.append((point,projmat))
		homo = []
		for (pointA,projMatA),(pointB,projMatB) in combinations(undist,2):			
			if pointA and projMatA and pointB and projMatB :
				homo.append(cv2.triangulatePoints(projMatA, projMatB, pointA,pointB).T)

		#Another way of averaging the results would be welcome
		return np.mean(homo,axis=0) if homo else (None,None,None)

	
#Loading of all the cameras parameters
# with np.load('matrix_dist_rvecs_tvecs_A.npz') as X:
#     mtxA, distA, rvecsA, tvecsA = [X[i] for i in ('mtxA','distA','rvecsA','tvecsA')] #Camera 1 in our setup

# with np.load('matrix_dist_rvecs_tvecs_E.npz') as X:
#     mtxE, distE, rvecsE, tvecsE = [X[i] for i in ('mtxE','distE','rvecsE','tvecsE')] #Camera 2 in our setup

# with np.load('matrix_dist_rvecs_tvecs_Z.npz') as X:
#     mtxZ, distZ, rvecsZ, tvecsZ = [X[i] for i in ('mtxZ','distZ','rvecsZ','tvecsZ')] #Camera 3 in our setup

#Convert 3D Homogeneouse points to 3D points
# points3d = cv2.convertPointsFromHomogeneous(points4D)
# points3d = points3d.tolist()
# points3d = list(map(lambda array: array[0],points3d))