

# Possible boat loads: (missionaries , canibales)
#all possible possibilty to carry one or 2 of members



moves=[(1,0), (0,1) , (2,0), (1,1), (0,2)]  # no (0,0) because boat cannot be empty

#check whether state follows puszzle rules

def stateFollow(state):
  #missionary on left
  ml=state[0]
  #cannibals on left
  cl=state[1]
  #missionary on right
  mr=state[2]
  #cannibals on right
  cr=state[3]

  #check if each count is between 0 and 3
  for i in (ml,cl,mr,cr):
    if i<0 or i >3:
      return False

  #left bank will be false of cannibals outnumber missionary
  if ml>0 and cl>ml:
    return False

  #same rule to check on right
  if mr>0 and cr>mr:
    return False

  return True  #if eveyrthibg correct


  #Find the state with one legal move

def findLegal(state):
    ml=state[0]
    cl=state[1]
    mr=state[2]
    cr=state[3]
    boat=state[4]

    #store next state in the list
    nextState=[]

    for move in moves:
      m=move[0]
      c=move[1]

      if boat=="L":
        #move people from left to right
        new_state=(ml-m , cl-c, mr+m, cr+c, "R")
      else:
        #move people from roght to left
        new_state=(ml+m,cl+c,mr-m,cr-c,"L")

      #only accpet the move if move is valid
      if stateFollow(new_state):
        nextState.append(new_state)

    return nextState


def search(start,search_method):
    #a list of path waiting to be explored
    waiting=[[start]]

    #list of states already explored
    visited=[]

    expansion=0
    while waiting:
      
      if search_method=="DFS":
        #take last path
        path=waiting.pop()
      else:
        #take first path
        path=waiting.pop(0)

      #get last state in path
      current=path[-1]

      #skip state if we already explored it 
      if current in visited:
        continue

      #check eevryone has recahed right bank
      if current[0]==0 and current[1]==0:
        return path,expansion

      visited.append(current)

      #counting this state becasue we will genearte its next move
      expansion=expansion+1

      #check if next state valid
      next_states=findLegal(current)

      if search_method=="DFS":
        next_states.reverse()

      for i in next_states:
        if i not in visited:

          #make diff path
          new_path=path.copy()
          new_path.append(i)

          #save new path so we can explor it later
          waiting.append(new_path)
    return None,expansion

#method for printing result

def result_print(heading,path,expansion):
  print(heading)
  if path is None:
    print("Solution Path: No solution")
    print("Total cost=N/A")
  else:
    print("Solution Path:")
    for i in path:
        print(i)

    print("Total cost=", len(path) -1)

  print("Number of node expansions=", expansion)
  print()


with open("input.txt") as file:
  line=file.readline()
  data=line.strip().split(",")



ml=int(data[0])
cl=int(data[1])
mr=int(data[2])
cr=int(data[3])
boat=data[4].strip()

start=(ml,cl,mr,cr,boat)
#DFS
result=search(start,"DFS")

result_print("The solution of Q1.1.a (DFS) is:",result[0],result[1])


#BFS
result2=search(start,"BFS")


result_print("The solution of Q1.1.b (BFS) is:",result2[0],result2[1])


x