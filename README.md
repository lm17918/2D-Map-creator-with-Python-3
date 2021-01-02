# 2D Map creator with Python 3
This code generates a 2-D square random map and creates a path between a starting point (given) and a goal point (that can be set as random). 
The map must have positives coordinates values been (0,0) and (n,m) with n = max width and m = max height of the map. 

![alt text](https://github.com/lm17918/2D-Map-creator-with-Python-3/blob/master/images/Map%20of%20size%20(10%2C%209)%20startingpoint%20(7%2C%200)%20and%20goal%20in%20(2%2C%207).png)

![alt text](https://github.com/lm17918/2D-Map-creator-with-Python-3/blob/master/images/Map%20of%20size%20(20%2C%2030)%20startingpoint%20(3%2C%2029)%20and%20goal%20in%20(18%2C%201).png)
To generate a new map the class called "MapGenerator" must be initialized with the following inputs. and then mapCreator() must be called.

```
Inputs:
- self.mapSize = touple with coordinates (max width, max height). 
- minDistance = Minimum path lenght between the initial point and the goal.
- startingPoint = Coordinates of the starting point.
- goal = Coordinated of the goal point.
- wallPercentage = Percentage of the map coordinates that are not accessible, if empty a value between 30% and 50% is selected.
- folder = Folder where the output data is saved.
- plotMap = If true an image is saved representig the created map.
```

To each coordinate of the generated map is associated an integer value. The value 0 is associated to points in the map that are considered free (and can be accessed to move from the starting point to the goal point), the value of 1 is assigned to coordinated that cannot be reached simulating the presence of a "wall" in those points. Other values, different from 0 and 1, can be used to define the start and the end of a path in the map. In this case 2 represents the starting point and 3 represensts the goal.

The coordinates of the "walls" in the map are chosen randomly. and the user can set a percentage of the map that can be occupated by those walls. I suggest to not use a value that goes over 70%. The A* search algorithm is used to verify and return the presence of at least one possible path between the starting point and the goal.

The output are: 

```
Outputs:
- path = Coordinated of the path find between the starting point and the goal.
- completeMap = numpy.ndarray representing the map just created.
- goal = coordinated of the goal point.
- mapSize = Size of the map generated.
- listEmptyPoints = List of coordintes free from walls
```

The creation of the map requires a period of time that is dipendent from its sizes (the bigger the map the more time it will take to generate it and find the path between the starting point and the goal) and the percentage of the map that is occupied from walls.









