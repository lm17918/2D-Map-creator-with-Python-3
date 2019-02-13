# Map_creator_Python-


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















