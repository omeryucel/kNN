import csv
import random
import math
import operator

def loadDataset(filename, split, trainingSet=[] , testSet=[]): #Open the dataset from CSV and split into test/train datasets.
	with open(filename, 'r') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)
	    for x in range(len(dataset)-1):
	        for y in range(4):
	            dataset[x][y] = float(dataset[x][y])
	        if random.random() < split:
	            trainingSet.append(dataset[x])
	        else:
	            testSet.append(dataset[x])


def euclideanDistance(instance1, instance2, length): #Calculate the distance between two data instances.
	distance = 0
	for x in range(length):
		distance += pow((instance1[x] - instance2[x]), 2)
	return math.sqrt(distance)

	
def getNeighbors(trainingSet, testInstance, k): #Locate k most similar data instances.
	distances = []
	length = len(testInstance)-1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

	
def getResponse(neighbors): #Generate a response from a set of data instances.
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

	
def getAccuracy(testSet, predictions): #Summarize the accuracy of predictions.
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0
	
	
def saveResults(result, testSet):
	file1.write("> predicted=" + result + " , actual=" + testSet + "\n")

	
def saveAccuracy(accuracy):
	file2.write("Accuracy: " + repr(accuracy) + " %")
	
	
def main():
	trainingSet=[]
	testSet=[]
	split = 0.67
	loadDataset('iris.data', split, trainingSet, testSet)
	print ('Train set: ' + repr(len(trainingSet)))
	print ('Test set: ' + repr(len(testSet)))
	predictions=[]
	k = 3
	for x in range(len(testSet)):
		neighbors = getNeighbors(trainingSet, testSet[x], k)
		result = getResponse(neighbors)
		predictions.append(result)
		saveResults(repr(result), repr(testSet[x][-1]))
		print('> predicted=' + repr(result) + ' , actual=' + repr(testSet[x][-1]))
	accuracy = getAccuracy(testSet, predictions)
	saveAccuracy(accuracy)
	print('Accuracy: ' + repr(accuracy) + ' %')


file1 = open('results.txt', 'w')
file2 = open('accuracy.txt', 'w')	
main()
file1.close()
file2.close()