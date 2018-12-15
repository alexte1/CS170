import math
import random
import copy
import numpy
################################################################################################################################################################
########################################################################	EDIT LOG	########################################################################

#	11/30/18. parseFile returns the dataList that is parsed.
#	11/30/18. Added splitFeatureData, eightyTwentySplit, euclidenaDistance
#			  knn_classifier.
#	12/02/18. Finished KNN and checked it with my CS171's implentation of KNN
#			  Results were the same, which means my implementation is correct.
#	12/03/18. Where to start: (FORWARD PROPAGATION)
#			  Now that we have found the best first feature, we need to take
#			  that feature and combine it with the others and test said others.
#	12/09/18. Update: Both forward propagation and backward propagation yeild
#			  The same result. Either they are both right, or both wrong.
#			  Need to check with the profoessor and his answer key.
################################################################################################################################################################


def intro():
	#in python 2.x we want to use raw_input because raw_input returns a string.
	#which is generally what we want to have retunred.
	#In this case it is to make sure we are opening the right file.
	print "Welcome to Alex Te's Feature Selection Algorithm."
	testFile = raw_input('Type in the name of the file to test - ')
	
	algorithmType = input("\nType the number of the algorithm you want to run.\n\t1) Forward Selection\n\t2) Backward Selection\n\t3) Alex's Special Algorithm\n\n\t\t")

	return (testFile, algorithmType)

#passing in file to open
#take care of parsing etc here
#returns the data all parsed.
def parseFile(fileToOpen):
# def parseFile():
	try:
		# file = open("CS170_SMALLtestdata__30.txt", "r")
		# file = open("CS170_SMALLtestdata__30.txt", "r")
		file = open(fileToOpen, "r")
	except IOError:
		print "Open failed"
		return

	data = file.readlines()

	dataList = []

	for i in data:
		parsed = i.split(" ")
		parsed = [float(j) for j in parsed]
		dataList.append(parsed)

	file.close()

	return dataList

#splitting the data from its feature. It will correspond accordingly. i.e
# 1.0000000e+00 8.3624403e-01 1.4527562e+00 1.4174702e+00 -4.0407611e-01 7.3276154e-02 -1.7618845e+00 -3.7207882e-01 1.5982776e+00 7.9518550e-01 3.7655497e-01
# will be split into:
# featureSplit = 1.0
# dataSplit = 8.3624403e-01 1.4527562e+00 1.4174702e+00 -4.0407611e-01 7.3276154e-02 -1.7618845e+00 -3.7207882e-01 1.5982776e+00 7.9518550e-01 3.7655497e-01
# but there will be more because there is more than 1 object.
def splitFeatureData(dataList):
	featureSplit = []
	dataSplit = []

	#make it random so that we can get different results from the same
	#data we are testing
	# random.shuffle(dataList)

	for i in dataList:
		featureSplit.append(i[0])
		dataSplit.append(i[1:])

	return(featureSplit, dataSplit)

#want to split the data into 80 and 20 % to test knn.
#the 80 will be the training set, and the 20 will be the testing set.
def eightyTwentySplit(dataSplit):
	
	trainingSet = []
	testingSet = []

	eighty = math.ceil(len(dataSplit) * .8)
	twenty = len(dataSplit) - eighty

	trainingSet = dataSplit[0:int(eighty)]
	testingSet = dataSplit[int(eighty):]

	return (trainingSet, testingSet)

#we use the LP norm to calculate distance.
#when p = 1. it is the manhattan distacne.
#when p = 2 we are using euclidean distance.
#in this example we will just p = 2
#equation is as follows:
# d_p(x, y) = SUMMATION(from i to n) |(xi)^p - (yi)^p|^(1/p)
def euclideanDistance(list1, list2):

	distance = 0.0

	for i, j in zip(list1, list2):
		distance += abs(i - j)**2

	distance = distance**(1./2)

	return distance

#using k = 5 for example to test 5 nearest neighbors.
#can change to anything
def knn_classifier(trainingSet, testingSet, trainingLabel, testingLabel):

	tmpList = []
	kdiffClasses = []

	#take 1 unseen data point and check it on all the of the points we trained.
	for i in range(len(testingSet)):
		distanceList = []
		#traversing through all the training set.. we need to find the distacne to all of the points
		for j in range(len(trainingSet)):
			# print "Passing in -", trainingSet[j]
			calulatedDistance = euclideanDistance(testingSet[i], trainingSet[j])
			#j is the index of the just calculated distance
			distanceList.append((calulatedDistance, j))

		#sort the distance list by ascending distances
		distanceList = sorted(distanceList, key = lambda tup: tup[0])
		#this is where we pick k of the nearest neighbors. (in this case k = 1)
		# tmpList = distanceList[:5]
		
		#need it to count what the current point's nearest neighbor is
		class1 = 0
		class2 = 0

		# print tmpList

		if trainingLabel[distanceList[0][1]] == 1.0:
			class1 += 1
		else:
			class2 += 1

		#appending the class label (either 1 or 2), then what point we are testing (i)
		if class1 > class2:
			kdiffClasses.append((1.0, i))
		else:
			kdiffClasses.append((2.0, i))

		#this breaks when we have checked all of the points
		if len(kdiffClasses) == len(testingLabel):
			break

	return kdiffClasses

def checkCalculation(resultTuple, testingLabel):

	counter = 0.0

	for i, j in zip(resultTuple, testingLabel):
		if i[0] == j:
			counter += 1.0

	# print "Percent - ", (counter / len(resultTuple)) * 100, "%"

	return (counter / len(resultTuple)) * 100

def getTestAttributes(testingSet):

	rtnList = []
	tmpTest =[]
	for i in range(len(testingSet[0])):
		tmpTest = []
		for j in range(len(testingSet)):
			# for k in range(depth):
			# 	tmpTest.append([testingSet[j][i]])
			tmpTest.append([testingSet[j][i]])
			# tmpTest.append(testingSet[j][i])
			#tmpTest = []
		rtnList.append(tmpTest)
	return rtnList

def getTrainAttributes(trainSet):

	rtnList = []
	for i in range(len(trainSet[0])):
		tmpTest = []
		for j in range(len(trainSet)):
			tmpTest.append([trainSet[j][i]])
			# tmpTest.append(trainSet[j][i])
		rtnList.append(tmpTest)
	return rtnList

def forwardPropagation(testingSet, trainingSet, trainingLabel, testingLabel):

	#stores all the percentages for forward propagation
	bestFeaturePercentList = []
	featureList = []
	flp = []
	#both of these lists have all the single columns.
	testOneColumn = getTestAttributes(testingSet)
	trainOneColumn = getTrainAttributes(trainingSet)

	#used to calculate the highest percentage
	bestFeaturePercent = 0

	for i in range(len(testOneColumn)):
		result = knn_classifier(trainOneColumn[i], testOneColumn[i], trainingLabel, testingLabel)
		percent = checkCalculation(result, testingLabel)
		featureList.append(i)
		flp.append(percent)
		if percent > bestFeaturePercent:
			bestFeaturePercent = percent
			feature = i

	#bestFeatureList will hold all the best features in order when using forward propagation.
	bestFeatureList = []
	bestFeatureList.append(feature)

	# print featureList
	# print flp

	for i in range(len(bestFeatureList)):
		print "Using feature(s) {", bestFeatureList[i], "} accuracy is", flp[i]
	print "Feature set {", feature,"} was best, accuracy is", bestFeaturePercent, "%\n"


	#Defined at the beginning of function.
	bestFeaturePercentList.append(bestFeaturePercent)

	#used so we can test each combination of pairs without editing the master (bestFeatureList) list
 	tmpBestFeatures = []
	featureList = []
	neededToPrintList = []
 	#keeps looping until the TmpBestFeatures (defined above) has reached all features and tried all combinations
	while len(tmpBestFeatures) != len(testOneColumn) - 1:
		#need to reset the percent after trying each iteration
		bestFeaturePercent = 0
		#defined above. tl;dr need a copy so we dont edit the master copy.
		tmpBestFeatures = copy.deepcopy(bestFeatureList)

		neededToPrintList.append(feature)
		needToPrintPercent = []

		for index in range(len(testOneColumn)):
			if index not in bestFeatureList:

				tmpBestFeatures.append(index)
				knnTestingSet = []
				knnTrainingSet = []

				for j in range(len(testingSet)):
					tmp = []
					for i in range(len(tmpBestFeatures)):
						tmp.append(testingSet[j][tmpBestFeatures[i]])
					knnTestingSet.append(tmp)

				for j in range(len(trainingSet)):
					tmp = []
					for i in range(len(tmpBestFeatures)):
						tmp.append(trainingSet[j][tmpBestFeatures[i]])
					knnTrainingSet.append(tmp)

				result = knn_classifier(knnTrainingSet, knnTestingSet, trainingLabel, testingLabel)
				percent = checkCalculation(result, testingLabel)

				featureList.append(index)

				neededToPrintList.append(index)
				needToPrintPercent.append(percent)

				if percent > bestFeaturePercent:
					bestFeaturePercent = percent
					feature = index
				del tmpBestFeatures[-1]

		bestFeatureList.append(feature)
		
		print "Using feature(s) {", bestFeatureList, "} accuracy is", bestFeaturePercent
		print "Feature set {", feature,"} was best, accuracy is", bestFeaturePercent, "%\n"

		# bestFeatureList.append(feature)
		# print bestFeatureList

		# return

		bestFeaturePercentList.append(bestFeaturePercent)

	# print bestFeatureList
	# print bestFeaturePercentList

	highest = -1

	# for i in range(len(bestFeaturePercentList)):
	# 	if bestFeaturePercentList[i] > highest:
	# 		highest = bestFeaturePercentList[i]
	# 		index2 = i

	# for i in range(index2 + 1):
	# 	print "Feature:", bestFeatureList[i] + 1

def backPropagation(testingSet, trainingSet, trainingLabel, testingLabel):

	#stores all the percentages for forward propagation
	bestFeaturePercentList = []

	#both of these lists have all the single columns.
	testOneColumn = getTestAttributes(testingSet)
	trainOneColumn = getTrainAttributes(trainingSet)

	#used to calculate the highest percentage

	percentList = []
	correspondingFeatureList = []

	copyTest = copy.deepcopy(testingSet)
	copyTrain = copy.deepcopy(trainingSet)

	testTheseFeatures = [0,1,2,3,4,5,6,7,8,9]
	ab = 0
	xyz = 0
	efIndex = 0
	while len(testTheseFeatures) > 0:

		run = 0
		tmp2 = []
		featureList = []
		bestFeaturePercent = 0
		excludeFeature = min(testTheseFeatures) - 1
		percentList = []
		correspondingFeatureList = []

		while run != len(testTheseFeatures):

			tmptmp = []
			knnTrainingSet = []
			knnTestingSet = []
			excludeFeature += 1

			while excludeFeature not in testTheseFeatures:
				excludeFeature += 1

			for i in range(len(copyTest)):
				tmp = []
				for j in range(len(testTheseFeatures)):
					if testTheseFeatures[j] != excludeFeature:
						tmp.append(copyTest[i][testTheseFeatures[j]])
				knnTestingSet.append(tmp)

			for k in range(len(copyTrain)):
				tmp = []
				for l in range(len(testTheseFeatures)):
					if testTheseFeatures[l] != excludeFeature:
						tmp.append(copyTrain[k][testTheseFeatures[l]])
				knnTrainingSet.append(tmp)

			result = knn_classifier(knnTrainingSet, knnTestingSet, trainingLabel, testingLabel)
			percent = checkCalculation(result, testingLabel)

			for n in range(len(testTheseFeatures)):
				if testTheseFeatures[n] != excludeFeature and excludeFeature in testTheseFeatures:
					tmptmp.append(testTheseFeatures[n])
			correspondingFeatureList.append(tmptmp)

			percentList.append(percent)

			if percent > bestFeaturePercent:
				featureList = []
				bestFeaturePercent = percent
				for m in range(len(testTheseFeatures)):
					if testTheseFeatures[m] != excludeFeature:
						featureList.append(testTheseFeatures[m])
			run += 1

		index = percentList.index(bestFeaturePercent)
		testTheseFeatures = copy.deepcopy(correspondingFeatureList[index])
		
		print "Using feature(s) {", bestFeatureList, "} accuracy is", bestFeaturePercent
		print "Feature set {", feature,"} was best, accuracy is", bestFeaturePercent, "%\n"

	print percentList
	print correspondingFeatureList
	return

def main():
	#returns the name of the file to open.
	fileToOpen, algorithmNum = intro()
	# algorithmNum = 1

	dataList = parseFile(fileToOpen)
	# dataList = parseFile()

	classLabels, dataSplit = splitFeatureData(dataList)

	trainingSet, testingSet = eightyTwentySplit(dataSplit)
	trainingLabel, testingLabel = eightyTwentySplit(classLabels)

	##################################################################################
	#running it will all the features and not just 1
	resultTuple = knn_classifier(trainingSet, testingSet, trainingLabel, testingLabel)
	percentCorrect = checkCalculation(resultTuple, testingLabel)
	##################################################################################
	if algorithmNum == 1:
		forwardPropagation(testingSet, trainingSet, trainingLabel, testingLabel)
	elif algorithmNum == 2:
		backPropagation(testingSet, trainingSet, trainingLabel, testingLabel)
	elif algorithmNum == 3:
		print "Alex's speical Algorithm (Alpha Beta Pruning)"
	else:
		print "Did not recgonize input"
main()