#AZHAR ABBAS SYED, ARIANA SOOKOO
#CMPSC 442- Artificial Intelligence
#Project 1
#----------------------------------------------------------------------------
#QUESTION 3: A* Search with Admissible Heuristics

#imports
import heapq
import math


moves=[(1,0), (0,1) , (2,0), (1,1), (0,2)]  # no (0,0) because boat cannot be empty

def action_cost(move, boat, cost_model):
    m = move [0]
    c = move[1]

    if cost_model == "A":
        return ((2 * m) + c)
    
    elif cost_model == "B":
        if boat == "L":
           return 2 
        else:
           return 1
        
#check whether state follows puzzle rules
def stateFollow(state):
    #missionary on left
    ml = state[0]
    #cannibals on left
    cl = state[1]
    #missionary on right
    mr = state[2]
    #cannibals on right
    cr =state[3]

    #check if each count is between 0 and 3
    for i in (ml, cl, mr, cr):
        if i < 0 or i > 3:
            return False

    #left bank will be false of cannibals outnumber missionary
    if ml > 0 and cl > ml:
        return False

    #same rule to check on right
    if mr > 0 and cr > mr:
        return False

    return True  #if everything is correct

#find the state with one legal move
def findLegal(state):
    ml = state[0]
    cl = state[1]
    mr = state[2]
    cr =state[3]
    boat = state[4]

    #store next state in the list
    nextState=[]

    for move in moves:
      m = move[0]
      c = move[1]

      if boat == "L":
        #move people from left to right
        new_state=(ml - m , cl - c, mr + m, cr + c, "R")
      else:
        #move people from roght to left
        new_state=(ml + m, cl + c, mr - m, cr - c,"L")

      #only accpet the move if move is valid
      if stateFollow(new_state):
        nextState.append((new_state, move))

    return nextState

#astar function
def astar(start, heuristic):
    #counter breaks ties between equal costs so heapq never compares paths
    counter = 0
    waiting = [(heuristic(start), counter, 0, [start])] # priority queue with (f, counter, g, path)
    visited = {}
    expansion = 0
    while waiting:
        f, _, current_cost, path = heapq.heappop(waiting) #pop the path with the lowest f value
        current = path[-1] #current state is the last state in the path

        #skip if we already reached this state more cheaply
        if current in visited and visited[current] <= current_cost:
            continue
        visited[current] = current_cost

        #check if goal state is reached
        if current[0] == 0 and current[1] == 0:
            return path, current_cost, expansion
        
        #increment the expansion counter
        expansion += 1

        #for each legal next state, calculate the cost and add it to the waiting list
        for new_state, move in findLegal(current):
            new_cost = current_cost + action_cost(move, current[4], "A")  #Assuming cost model A for A* search

            if new_state in visited and visited[new_state] <= new_cost:
                continue

            new_path = path.copy()
            new_path.append(new_state)
            counter += 1
            heapq.heappush(waiting, (new_cost + heuristic(new_state), counter, new_cost, new_path)) #push the new path with its f value into the priority queue
    return None, None, expansion

#heuristics
def heuristic1(state):
    ml = state[0]
    cl = state[1]

    #heuristic: Passenger Weight Remaining
    return ((2 * ml) + cl)

def heuristic2(state):
    ml = state[0]
    cl = state[1]

    #heuristic: Trip-Packing Lower Bound
    return math.ceil((((2 * ml) + cl)/3))

#method for printing astar result
def astar_result_print(heading, path, cost, expansion):
  print(heading)
  if path is None:
    print("Solution Path: No solution")
    print("Total cost = N/A")
  else:
    print("Solution Path:", "-> ".join(str(i) for i in path))
    print("Total cost =", cost)
  print("Number of node expansions =", expansion)
  print()

with open("input.txt") as file:
  line=file.readline()
  data=line.strip().split(",")

ml = int(data[0])
cl = int(data[1])
mr = int(data[2])
cr = int(data[3])
boat = data[4].strip()

start=(ml, cl, mr, cr, boat)

for name, heuristic in [("Heuristic 1", heuristic1), 
                        ("Heuristic 2", heuristic2), 
                        ("Heuristic 3", heuristic3)]:
    path, cost, expansion = astar(start, heuristic)
    astar_result_print(f"The solution of Q3.2 ({name}) is:", path, cost, expansion)