"""
with this code you generate a 2-D map in python 3. To generate your map you have to first initialize its "Size". 
All maps will have a square form (for example Size=[3,3] will generate a square map with values on the x-coordinated
between 0 and 3 and y-coordinated between 0 and 3). The new map is saved as a numpy.ndarray, where different values
are associated to the map's coordinates. Every position of the map have a numeric value. In this case, the value 0 is associated with
points in the map that can be reached, the value of 1 is assigned to coordinated that cannot be reached simulating the presence of a "wall"
in those points. Other values, different from 0 and 1, can be used to define the start and the end of a path in the map.
Everytime a map is created, the coordinates of the "walls" in the map are chosen randomly. It is possible to control a value 
called "perc_walls" that indicate the percentage of points in the map that cannot be reached given the presence of walls.
(for example, if the size of the map is 3x3, we have 9 positions. if we choose perc_walls=30, we have a wall in the 30% of the 
coordinates of the map. (int)(9/100)*30=3 positions occupied by a wall in the map)
To verify that the random map created has a at least a path between the start and the stop position, we use the A* algorithm. 
If a path between the two points is not found, a new map is created.  
The output of this code is the new map generated, the path bestween the start and stop position and the coordinates of the map 
where there are no walls.
"""

import numpy as np
import random
import math
import matplotlib.pyplot as plt





class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    # Initialize both open and closed list
    open_list = []
    closed_list = []
    # Add the start node
    open_list.append(start_node)
    # Loop until you find the end
    while len(open_list) > 0:
        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            #return 
            return "possible",path[::-1] # Return reversed path
        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue
            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 1 :
                continue
            # Create new node
            new_node = Node(current_node, node_position)
            # Append
            children.append(new_node)
        # Loop through children
        for child in children:
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            # Add the child to the open list
            open_list.append(child)




def Create_map(start,stop,bs,perc_walls):
    mapp= np.zeros(bs)
    mapp[start]=2
    mapp[stop]=4
    x,y = np.where(mapp ==0 )
    coordinates = []
    for i in range (0,len(x)):#coordinates of the environment
        coordinates.append((x[i],y[i]))      
    n_walls=(round((len(coordinates)/100)*perc_walls))#number of walls in the map
    possible_map="not ok"
    initial_map=mapp.copy()
    while (possible_map!="ok"):
        mapp=initial_map.copy()
        walls=random.sample(coordinates, k=n_walls) #choose random coordinated for the walls  
        for m in walls :
            mapp[m]=1               
        string, path = astar(mapp,start,stop)#use A* to find a possible path
        if(string=="impossible"):
            continue
        else:
            possible_map="ok"
    return mapp,path



def initialz (Size,min_dist,perc_walls):
    start = (random.randrange(0,Size[1]),random.randrange(0,Size[1]))#random staert position
    s_=0                
    while(s_==0):    
        stop  = (random.randrange(0,Size[1]),random.randrange(0,Size[1])) #random stop position   
        dist1 = math.sqrt(sum([(a - b) ** 2 for a, b in zip(start , stop)]))#distance between start or stop
        if (dist1>min_dist):
            s_=1 # stop the while cycle if the 2 coordinates are far enough                           
            
    mappa, path= Create_map(start,stop,Size,perc_walls)
    return mappa, path,start,stop
            
  

def plotting_results (mapp,path):
    x,y = np.where(mapp ==1 )
    plt.scatter(x,y, color="red")#walls
    
    x,y = np.where(mapp ==2 )#start
    plt.scatter(x,y, color="blue",marker='x',s=150)
    
    x,y = np.where(mapp ==4 )#stop
    plt.scatter(x,y, color="black",s=150)
    
    x = [p[0] for p in path]
    y = [p[1] for p in path]
    plt.plot(x,y, color="green")# path

    plt.show()    
    plt.title('map of size {} start in {} stop {}'.format(Size,start,stop))
    plt.savefig('map of size {} start in {} stop {} .png'.format(Size,start,stop))
    
    x,y = np.where(mapp !=1 )
    list_= []
    for i in range (0,len(x)):
        list_.append([x[i],y[i]])
    return list_ #return the list of coordintes free from walls
    
#-----------------------------------------------------------------------------------------------    
#-----------------------------------------------------------------------------------------------


perc_walls= 30   #percentage of coordinates occupied by walls
Size=(15,15)     #size of the map     
min_dist=8       #min distance between start and stop


mapp, path , start ,stop =initialz (Size,min_dist,perc_walls)
list_=plotting_results(mapp,path)





