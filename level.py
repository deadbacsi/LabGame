# color code
# \033[foreground/background;2;R;G;Bm
# foreground: 38 background: 48

#####PPP###################

import player, enemy, os, math, time

direction_index = ["▲", "►", "▼", "◄"]
world = []
facingConstant = 0.0

def load_level(fi):
    global world
    world = []
    lineNum = 0
    with open(fi + ".ter") as f:
        for line in f:
            row = []
            for i in range(0,len(line)):
                if line[i] != '\n':
                    row.append(line[i])
                    # if line[i] == 'P':
                    #     player.x = i
                    #     player.y = lineNum
            world.append(row)
            lineNum += 1

    with open(fi + ".inf") as f:
        # Temporary testing measures
        player.x = 1
        player.y = 1
        player.facing = 2
                
def paint_level():
    os.system("clear")
    paint = ""
    for i in range(0, len(world)):
        for j in range(0,len(world[i])):
            tile = world[i][j]
            if tile in ["X"," ","T","F"]:
                paint += "░"
            elif tile in ["#"]:
                paint += "▓"
            elif tile in "P":
                paint += direction_index[player.facing]

            if j < len(world[i])-1:
                try:
                    if tile in ["#"] and world[i][j+1] in ["#"]:
                        paint += "▓"
                    else:
                        paint += "░"
                except:
                    pass

        paint += "\n"
    print(paint)

def paint_vision():
    os.system("clear")
    paint = ""
    tempWorld = world
    tempWorld[player.y][player.x] = "P"
    vision = in_vision([player.y,player.x,player.facing])
    # walls = [] # For debugging purposes
    
    for i in range(0, len(tempWorld)):
        for j in range(0,len(tempWorld[i])):
            if [i,j] in vision:
                tile = tempWorld[i][j]
                if tile in ["X"," ","T","F"]:
                    paint += "░"
                elif tile in ["#"]:
                    paint += "▓"
                    # walls.append([i,j]) # for debugging purposes
                elif tile in "P":
                    paint += direction_index[player.facing]

                if j < len(tempWorld[i])-1:
                    try:
                        if tile in ["#"] and tempWorld[i][j+1] in ["#"]:
                            paint += "▓"
                        else:
                            paint += "░"
                    except:
                        pass
            else:
                paint += " "
                if j < len(world[i])-1:
                    paint += " "
        paint += "\n"
    print(paint)
    # print(walls)

def in_vision(source, viewDistance = 8.5):
    # vision = [[1,1],[1,2],[2,1],[2,2]] # Debug version
    vision = []
    # Setting up maximum possible vision
    couldView = []
    CeilViewDistance = math.ceil(viewDistance)

    # Check in a circle, add cells within to possible vision (couldView)
    for i in range(source[0] - CeilViewDistance, source[0] + CeilViewDistance + 1):
        for j in range(source[1] - CeilViewDistance, source[1] + CeilViewDistance + 1):
            if in_world(i,j):
                if get_distance(source,[i,j]) <= viewDistance:
                    # print(source,get_distance(source,[i,j]),[i,j])
                    couldView.append([i,j])
    
    # Testing if in view
    for coord in couldView:
        angle = (( get_angle([source[0],source[1]],coord) + ( source[2] + 
            facingConstant ) * math.pi/2 ) % ( math.pi * 2 ) )
        if angle < math.pi * 1.3 and angle > math.pi * 0.7:
            if check_visibility([source[0],source[1]],coord):
                vision.append(coord)

    # At the end add area around player in a 3x3 area

    for i in range(0,3):
        for j in range(0,3):
            extraVision = [source[0] - 1 + i, source[1] -1 + j]
            if extraVision not in vision:
                vision.append(extraVision)

    return vision

def get_angle(source,target):
    dx = target[0] - source [0]
    dy = target[1] - source [1]
    return math.atan2(dy,dx)

def get_distance(source,target):
    dx = target[0] - source [0]
    dy = target[1] - source [1]
    return (dx**2 + dy**2)**0.5

def check_visibility(source, target, step = 0.75, sensitivity = 0.5):

    canSee = True
    currentStep = step
    angle = get_angle(source,target)
    distance = get_distance(source,target)
    wiggleRoom = 1.0 # used for searching coordinates around current step
    
    # step through the distance between the target and source
    while currentStep < distance:
        coord = ([source[0] + currentStep * math.cos(angle),
            source[1] + currentStep * math.sin(angle)])

        # during each step, check the coordinates around the current step
        for i in range( math.floor( coord[0] - wiggleRoom ), math.ceil( coord[0] + wiggleRoom ) ):
            for j in range( math.floor( coord[1] - wiggleRoom ), math.ceil( coord[1] + wiggleRoom) ):
                # if the coordinate checked is inside the world
                if in_world(i,j):
                    # if the coordinate is within [sensitivity] 
                    # horizontal and vertical distance from the step
                    if abs(i - coord[0]) < sensitivity and abs(j - coord[1]) < sensitivity:
                        # if there is a wall at that wolrd coordinate (unless it's the target)
                        if world[i][j] in ["#"] and [i,j] != target:
                            # you can not see this tile
                            canSee = False
                            return canSee

        currentStep += step

    return canSee

def in_world(i,j):
    return (i >= 0 and j >= 0 and i < len(world) and j < len(world[i]) )

# Fal = ▓
# Terep = ░
# Player/ Enemy = ▲ ► ▼ ◄
# Enemy = E
# Exit = O

# print(load_level("testmap.txt"))

