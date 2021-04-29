#pygame ?
"""
+5 box on goal
+10 all boxes on goals

box with walls on two or more sides -1

input states [ wall left, wall right, wall up, wall down,

  move left, move right, move up, move down,

  goal left, goal right,
  goal up, goal down
]

output states [move left, move right, move up, move down]
"""

FLOOR = 0
WALL = 1
BOX = 2
GOAL = 3
PLAYER = 4
BOX_AND_GOAL = 5
PLAYER_AND_GOAL = 6

level1 = "########\n# . #  #\n# $ @$.#\n#   #  #\n########"
########
# . #  #
# $ @$.#
#   #  #
########

level2 = "########\n###   ##\n#.@$  ##\n### $.##\n#.##$ ##\n# # . ##\n#$ *$$.#\n#   .  #\n########"
########
###   ##
#.@$  ##
### $.##
#.##$ ##
# # . ##
#$ *$$.#
#   .  #
########

currentLevel = 0
levelPool = [level1, level2]
level = []
playerLocation = {}


def main():
	CreateLevel()


def execute(command):
	lowered = command.lower()
	if lowered == "right":
		movePlayer(0, 1)
	elif lowered == "left":
		movePlayer(0, -1)
	elif lowered == "up":
		movePlayer(-1, 0)
	elif lowered == "down":
		movePlayer(1, 0)
	elif lowered == "reset":
		ResetLevel()


def nextLevel():
	global currentLevel
	global levelPool
	currentLevel += 1
	if currentLevel > len(levelPool):
		currentLevel = 0

	# Temp
	CreateLevel()


def ResetLevel():
	# Temp
	CreateLevel()


def CreateLevel():
	global level
	level = GetCurrentLevel()
	playLevel()


def GetCurrentLevel():
	global levelPool
	global currentLevel

	levelStr = levelPool[currentLevel]
	parsedLevel = ParseLevel(levelStr)

	return parsedLevel


def ParseLevel(levelString):
	global playerLocation
	rows = levelString.count('\n') + 1
	cols = levelString.find('\n')
	
	levelArray = [[-1 for x in range(cols)] for y in range(rows)]

	n = 0
	m = 0
	for s in levelString:
		if s == " ":
			levelArray[m][n] = FLOOR
			n += 1
		elif s == "#":
			levelArray[m][n] = WALL
			n += 1
		elif s == "$":
			levelArray[m][n] = BOX
			n += 1
		elif s == ".":
			levelArray[m][n] = GOAL
			n += 1
		elif s == "@":
			levelArray[m][n] = PLAYER
			playerLocation["col"] = n
			playerLocation["row"] = m
			n += 1
		elif s == "*":
			levelArray[m][n] = BOX_AND_GOAL
			n += 1
		elif s == "+":
			levelArray[m][n] = PLAYER_AND_GOAL
			playerLocation["col"] = n
			playerLocation["row"] = m
			n += 1
		elif s == "\n":
			m += 1
			n = 0
		else:
			print("Level Parser: invalid character: ", s, " found")
			return []
	return levelArray

def printLevel():
	global level
	letters = ["-", "#", "□", "○", "P", "■","◍"]
	for row in level:
		for col in row:
			print(letters[col], end = " ")
		print()
	print()

# checks if any boxes are not on a goal
def CheckWinState():
	global level
	rows = len(level)
	cols = len(level[0])

	for row in range(rows):  # rows
		for col in range(cols):  # cols
			if level[row][col] == BOX:
				return False

	return True


def playLevel():
	global currentLevel
	printLevel()
	levelOneSolve = ["right", 'left', 'left', 'down', 'left', 'up', 'up']
	if currentLevel == 0:
		for command in levelOneSolve:
			execute(command)


# -right = left and -down = up
def movePlayer(down, right):
	global playerLocation
	global level

	col = playerLocation["col"] + right
	row = playerLocation["row"] + down

	if level[row][col] == WALL:
		return

	if level[row][col] == BOX or level[row][col] == BOX_AND_GOAL:
		if level[row+down][col+right] != WALL and level[row+down][col+right] != BOX:
			# updating where box was
			if level[row][col] == BOX:
				level[row][col] = FLOOR
			elif level[row][col] == BOX_AND_GOAL:
				level[row][col] = GOAL

			# updating where box will be
			if level[row+down][col+right] == GOAL:
				level[row+down][col+right] = BOX_AND_GOAL
			else:
				level[row+down][col+right] = BOX

		else:
			return

	# Updating where player was
	if level[playerLocation["row"]][playerLocation["col"]] == PLAYER_AND_GOAL:
		level[playerLocation["row"]][playerLocation["col"]] = GOAL
	else:
		level[playerLocation["row"]][playerLocation["col"]] = FLOOR

	# updating where player is
	if level[row][col] == GOAL:
		level[row][col] = PLAYER_AND_GOAL
	else:
		level[row][col] = PLAYER

	playerLocation["col"] = col
	playerLocation["row"] = row
	onMoveCompleted()


def onMoveCompleted():
	global currentLevel
	if CheckWinState():
		print("You Won level {}!".format(currentLevel + 1))
		nextLevel()
	else:
		printLevel()


if __name__ == "__main__":
	#level = sys.argv[1]
	main()
