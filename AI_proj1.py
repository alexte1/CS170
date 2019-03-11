import numpy as np
#https://stackoverflow.com/questions/23726876/copying-lists-editing-copy-without-changing-original
from copy import deepcopy

#stores the children nodes that we will look at.
#stored as a tuple (borad, f(n))
#then select the lowest f(n) out of all the values inside the list
leafNodes = []

#max size of the leafNodes Array
maxSize = -1


#Used to make sure we do not add a duplicate state
duplicate = []
initDuplicate = []
#the board's desired position
key = []
key.append([1, 2, 3])
key.append([4, 5, 6])
key.append([7, 8, 0])

#diameter of 8 Puzzle
DIAMETER = 31

#used to help assign the g(n) in all the moves
storeRow = 9999

#used to take care of first case expanding children
#can see it being used in moving in all direction functions
flag = True

numNodesExpanded = 0

#iterates through all the values to see how many moves
#to their solved position
def manhattanHeuristic(board):
	row = 0
	heuristic = 0

	for i in board:
		for j in range(len(i)):
			if i[j] != 0:

				#find position of value in game board
				nonKeyTuple = findPosition(board, i[j])

				#find position of value in key board
				keyTuple = findPosition(key, i[j])

				#take the absolute value to ensure positive distance
				heuristic += abs(nonKeyTuple[0] - keyTuple[0])+ abs(nonKeyTuple[1] - keyTuple[1])

	return heuristic

#command to move the 0 to the left.
def moveLeft(board, row, column):

	#arbitrary flag used to help computation
	flag2 = True

	#deepcopy so that we can edit the tmpBoard and not the acutal board
	tmpBoard = deepcopy(board)

	#checking to see if we can move left.
	if column <= 0 or column > 2:
		return False

	#swapping positions 0 and whatever is to the left of it.
	tmp = tmpBoard[row][column]
	tmpBoard[row][column] = tmpBoard[row][column - 1]
	tmpBoard[row][column - 1] = tmp

	if flag:
		tupl = (tmpBoard, manhattanHeuristic(tmpBoard), 1)
	else:
		tupl = (tmpBoard, manhattanHeuristic(tmpBoard), leafNodes[storeRow][2] + 1)

		duplicate[0] != tupl[0]

	#					IMPORTANT
	#check to see if we have already seen the board.
	#if if has been seen, do not put it back in the list
	for item in duplicate:
		if item[0] == tupl[0]:
			flag2 = False
	if flag2:
		leafNodes.append(tupl)


	return tmpBoard

#command to move 0 to the right
def moveRight(board, row, column):
	flag2 = True
	tmpBoard = deepcopy(board)
	#check if we can move right
	if column == len(tmpBoard[0]) - 1 or column < 0:
		return False

	tmp = tmpBoard[row][column + 1]
	tmpBoard[row][column + 1] = tmpBoard[row][column]
	tmpBoard[row][column] = tmp

	if flag:
		tupl = (tmpBoard, manhattanHeuristic(tmpBoard), 1)
	else:
		tupl = (tmpBoard, manhattanHeuristic(tmpBoard), leafNodes[storeRow][2] + 1)

	for item in duplicate:
		if item[0] == tupl[0]:
			flag2 = False
	if flag2:
		leafNodes.append(tupl)

	#returns true if move was legal
	return tmpBoard

#command to move 0 down
def moveDown(board, row, column):
	flag2 = True
	#check if we can move down
	tmpBoard = deepcopy(board)
	if row >= 2:
		return False

	tmp = tmpBoard[row + 1][column]
	tmpBoard[row + 1][column] = tmpBoard[row][column]
	tmpBoard[row][column] = tmp

	if flag:
		tupl = (tmpBoard, manhattanHeuristic(tmpBoard), 1)
	else:
		tupl = (tmpBoard, manhattanHeuristic(tmpBoard), leafNodes[storeRow][2] + 1)

	for item in duplicate:
		if item[0] == tupl[0]:
			flag2 = False
	if flag2:
		leafNodes.append(tupl)

	#returns true if move was legal
	return tmpBoard

#command to move the 0 up
def moveUp(board, row, column):
	flag2 = True
	tmpBoard = deepcopy(board)
	#check to see if we can move up
	if row <= 0 or row> 2:
		return False

	tmp = tmpBoard[row][column]
	tmpBoard[row][column] = tmpBoard[row - 1][column]
	tmpBoard[row - 1][column] = tmp

	if flag:
		tupl = (tmpBoard, manhattanHeuristic(tmpBoard), 1)
	else:
		tupl = (tmpBoard, manhattanHeuristic(tmpBoard), leafNodes[storeRow][2] + 1)

	for item in duplicate:
		if item[0] == tupl[0]:
			flag2 = False
	if flag2:
		leafNodes.append(tupl)

	#returns true if move was legal	
	return tmpBoard

#finds the specified value's position (row, column) on board.
def findPosition(board, value):
	row = 0
	for i in board:
		for j in range(len(i)):
			if i[j] == value:
				return (row,j)
		row += 1

#iterates through the game board versus the key board
#then it will return the number of tiles that are not
#in the right place
def misplacedTiles(board):
	misplacedTiles = 0
	iterator = 0
	for i in board:
		for j in range(len(i)):
			if key[iterator][j] != i[j]:
				if i[j] != 0:
					misplacedTiles += 1
		if iterator == 2:
			iterator = 0
		else:
			iterator += 1
	return misplacedTiles

#To display current status of the board
def displayBoard(board):
	print "\nBoard Orientation:"
	for i in range(len(board)):
		print str(board[i][0]) + " " + str(board[i][1]) + " " + str(board[i][2])
	print "\n"

#Astar algorithm
def aStar(board, algorithmType):

	#global variables used to help add to the leafNodes list
	#and compute the A* algorithm
	global numNodesExpanded
	global flag
	global storeRow
	global duplicate
	global maxSize
	#used to keep track of the lowest / best node to expand.
	#this takes place in the while loop f(n) = g(n) + h(n)
	lowest = 9999
	#used to stop the program early to debug and follow code.
	breakCond = 0

	#sets the heuristic. This depends on what the user inputed
	if algorithmType == 1:
		heuristic = 0
	elif algorithmType == 2:
		heuristic = misplacedTiles(board)
	else:
		heuristic = manhattanHeuristic(board)

	#this is taking care of the first case, where we have just 1 board.
	#find where the 0 is and expand to all legal states
	#then delete it 

	zeroRow, zeroColumn = findPosition(board, 0)
	duplicate.append((board, heuristic, 0))
	numNodesExpanded += 1
	moveUp(board, zeroRow, zeroColumn)
	moveDown(board, zeroRow, zeroColumn)
	moveLeft(board, zeroRow, zeroColumn)
	moveRight(board, zeroRow, zeroColumn)

	#this flag is set so that the move operators know that
	#we have taken care of the first board.
	flag = False

	#if you passed in a solved key then just exit function
	#the board is already solved.
	if board == key:
		#print "The best state to expand with a g(n) = ", 0, "and h(n) = ", heuristic, " is..." 
		return

	while 1:
		#used to keep track of the lowest / best node to expand.
		#this takes place in the while loop f(n) = g(n) + h(n)
		lowest = 9999

		#since we are traversing the leafNodes array backwards, we need to make sure
		#we are setting the right now
		tmpRow = len(leafNodes) - 1

		#traversing the leafNodes, and finding out what node is the best one to expand.
		#the node will be found by the row #
		for i in reversed(leafNodes):
			tmpSum = i[1] + i[2]
			if tmpSum < lowest:
				lowest = tmpSum
				row = tmpRow
			tmpRow-=1
			#print i

		#print "Expanding row: ", row

		#print "Displaying board in A*"
		displayBoard(leafNodes[row][0])

		if leafNodes[row][1] == 0:
			print "Solution at depth - ", leafNodes[row][2]
			return True

		print "The best state to expand with a g(n) = ", leafNodes[row][2], "and h(n) = ", leafNodes[row][1], " is..."


		#can toggle on and off if the user wants to stop the program earlier.
		#set breakCond == x and it will stop after x iterations
		#======================================================
		#if breakCond == 500:
		# 	return 0
		#======================================================

		#meat of the algorithm.
		#find where the 0 is and exhaust the different ways we can change the board to different states (non repeating)
		#print "Passing in board: ", leafNodes[row][0]
		storeRow = row
		zeroRow, zeroColumn = findPosition(leafNodes[row][0], 0)
		moveUp(leafNodes[row][0], zeroRow, zeroColumn)
		moveDown(leafNodes[row][0], zeroRow, zeroColumn)
		moveLeft(leafNodes[row][0], zeroRow, zeroColumn)
		moveRight(leafNodes[row][0], zeroRow, zeroColumn)
		duplicate.append(leafNodes[row])
		numNodesExpanded += 1

		# print "len(leafNodes) - ", len(leafNodes)

		if len(leafNodes) > maxSize:
			maxSize = len(leafNodes)

		del leafNodes[row]

		breakCond += 1

#choose what algorithm to use
def Algorithm():
	algorithm_type = input("\nEnter your choice of algoithm\n"
							"	1. Uniform Cost Search\n"
							"	2. A* with the Misplaced Tile heuristic\n"
							"	3. A* with the Manhattan disance heuristic\n\n\t"	
						)

	while algorithm_type != 1 and algorithm_type != 2 and algorithm_type != 3:
		algorithm_type = input("Please enter 1, 2, or 3 - ")
	return algorithm_type

#generating the 8 Tile game board.
def generate_Board():

	puzzleType = input("Type 1 to use a default puzzle, or 2 to enter your own puzzle - ")
	gameBoard = []

	#already made sure that it is either a 1 or 2
	while puzzleType != 1 and puzzleType != 2:
		puzzleType = input("Please enter either 1 or 2 - ")

	if puzzleType == 1:
		#a default board. easy to solve
		#solution at https://www.cs.princeton.edu/courses/archive/spr10/cos226/assignments/8puzzle.html
		row1 = [0, 1, 3]
		row2 = [4, 2, 5]
		row3 = [7, 8, 6]
	else:
		#getting the rows the user wants.
		print("\nEnter your puzzle, use a zero to represent a blank")
		tmp = raw_input("\nEnter the first row, use space or tabs between numbers - ")
		row1 = map(int, tmp.split())
		tmp = raw_input("\nEnter the second row, use space or tabs between numbers - ")
		row2 = map(int, tmp.split())
		tmp = raw_input("\nEnter the third row, use space or tabs between numbers - ")
		row3 = map(int, tmp.split())


	#gameBoard = np.array([row1, row2, row3])
	gameBoard.append(row1)
	gameBoard.append(row2)
	gameBoard.append(row3)

	global initDuplicate
	initDuplicate = gameBoard

	return gameBoard

def display_Message():
	print "Welcome to Alex's 8 puzzle solver."

def main():
	#display welcome message
	display_Message()

	#create the board the user wants to specify. Or default.
	board = generate_Board()
	
	#selecting type of algorithm
	algorithmType = Algorithm()

	#display the board
	displayBoard(board)

	#call the aStar algorithm with specified algorithm type
	if (aStar(board, algorithmType)):
		print "Goal!!"

	print "NUMBER OF NODES EXPANDED - ", numNodesExpanded
	print "MAX QUEUE SIZE - ", maxSize

main()
