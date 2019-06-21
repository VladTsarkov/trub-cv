# import the necessary packages
import numpy as np
import imutils
import cv2

class Stitcher:
	def __init__(self):
		# determine if we are using OpenCV v3.X
		self.isv3 = imutils.is_cv3()

	def stitch(self, images, ratio=0.75, reprojThresh=4.0,
		showMatches=False):
		# unpack the images, then detect keypoints and extract
		# local invariant descriptors from them
		(imageB, imageA) = images
		(kpsA, featuresA) = self.detectAndDescribe(imageA)
		(kpsB, featuresB) = self.detectAndDescribe(imageB)
		# match features between the two images
		M = self.matchKeypoints(kpsA, kpsB,
			featuresA, featuresB, ratio, reprojThresh)

		# if the match is None, then there aren't enough matched
		# keypoints to create a panorama
		if M is None:
			return None

		# otherwise, apply a perspective warp to stitch the images
		# together
		(matches, H, status) = M
		result = cv2.warpPerspective(imageA, H,
			(imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
		#result1 = cv2.warpPerspective(imageB, H,
		#	(imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
		#cv2.imwrite("resultleft.jpg",result1)
		result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

		# check to see if the keypoint matches should be visualized
		if showMatches:
			vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches,
				status)

			# return a tuple of the stitched image and the
			# visualization
			return (result, vis)

		# return the stitched image
		return result

	def detectAndDescribe(self, image):
		# convert the image to grayscale
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# check to see if we are using OpenCV 3.X
		#if self.isv3:
			# detect and extract features from the image

		"""
		descriptor = cv2.xfeatures2d.SIFT_create()
		(kps, features) = descriptor.detectAndCompute(image, None)
		"""

		orb = cv2.ORB_create()
		kps = orb.detect(image,None)
		kps, des = orb.compute(image,	kps)

		# otherwise, we are using OpenCV 2.4.X
		"""else:
			# detect keypoints in the image
			detector = cv2.FeatureDetector_create("SIFT")
			kps = detector.detect(gray)

			# extract features from the image
			extractor = cv2.DescriptorExtractor_create("SIFT")
			(kps, features) = extractor.compute(gray, kps)"""

		# convert the keypoints from KeyPoint objects to NumPy
		# arrays
		kps = np.float32([kp.pt for kp in kps])

		# return a tuple of keypoints and features
		return (kps, des)

	def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB,
		ratio, reprojThresh):
		# compute the raw matches and initialize the list of actual
		# matches
		matcher = cv2.DescriptorMatcher_create("BruteForce")
		#print("A ",len(featuresA))
		#print("kpsA ",kpsA)
		#print("kpsAlen ",len(kpsA))
		#print("B ",featuresB)
		rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
		matches = []

		# loop over the raw matches
		for m in rawMatches:
			# ensure the distance is within a certain ratio of each
			# other (i.e. Lowe's ratio test)
			if len(m) == 2 and m[0].distance < m[1].distance * ratio:
				matches.append((m[0].trainIdx, m[0].queryIdx))

		# computing a homography requires at least 4 matches
		if len(matches) > 4:
			# construct the two sets of points
			ptsA = np.float32([kpsA[i] for (_, i) in matches])
			ptsB = np.float32([kpsB[i] for (i, _) in matches])
			print(ptsA.dtype)
			print([kpsA[i] for (_, i) in matches])
			"""
			ptsB1 = np.float32([[2391.,1128.91],
			[2389.55,1326.73],
			[2502.47,1329.77],
			[2535.24,1495.66],
			[2588.34,1548.62],
			[2605.74,1446.40],
			[2661.89,1562.11],
			[2716.22,1593.61]]
			)
			ptsA1 = np.float32([[228.39,1187.70],
			[193.46,1402.63],
			[297.11,1413.44],
			[331.80,1576.22],
			[396.83,1626.58],
			[409.86,1522.65],
			[454.,1640.16],
			[525.89,1654.61]]
			)
			(H, status) = cv2.findHomography(ptsA1, ptsB1, cv2.RANSAC,
				reprojThresh)
			"""

			"""
			#NEW1-NEW2
			ptsB1 = np.float32([[2630.98,1543.13],
			[2520.20,1864.71],
			[2669.92,1494.41],
			[2657.72,1582.19],
			[2711.66,1553.72],
			[2711.92,1596.90]]
			)
			ptsA1 = np.float32([[295.09,1431.09],
			[232.92,1768.44],
			[334.72,1382.70],
			[322.10,1470.10],
			[384.59,1441.63],
			[385.10,1483.37]]
			)
			(H, status) = cv2.findHomography(ptsA1, ptsB1, cv2.RANSAC,
				reprojThresh)
			"""
			#print("ptsA1",ptsA1)
			print("ptsA ",ptsA)
			print("ptsAlen ",len(ptsA))
			print("ptsB ",ptsB)
			# compute the homography between the two sets of points
			(H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,
				reprojThresh)


			# return the matches along with the homograpy matrix
			# and status of each matched point
			print("matches ",matches)
			print("status ",status)
			print("H ",H)
			return (matches, H, status)

		# otherwise, no homograpy could be computed
		print(len(matches))
		print("RLY?")
		return None

	def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
		# initialize the output visualization image
		(hA, wA) = imageA.shape[:2]
		(hB, wB) = imageB.shape[:2]
		vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
		vis[0:hA, 0:wA] = imageA
		vis[0:hB, wA:] = imageB

		# loop over the matches
		for ((trainIdx, queryIdx), s) in zip(matches, status):
			# only process the match if the keypoint was successfully
			# matched
			if s == 1:
				# draw the match
				ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
				ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
				cv2.line(vis, ptA, ptB, (0, 255, 0), 1)

		# return the visualization
		return vis
