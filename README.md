# 2D Map creator with Python 3
This Python script generates a 2D square random map and establishes a path between a specified starting point and a goal point. The map is defined by positive coordinate values within the range (0,0) to (n,m), where n is the maximum width and m is the maximum height of the map.

![alt text](https://github.com/lm17918/2D-Map-creator-with-Python-3/blob/master/images/example1.png)

![alt text](https://github.com/lm17918/2D-Map-creator-with-Python-3/blob/master/images/example2.png)

## Usage
To generate a new map, initialize the MapGenerator class with the following inputs and then call the createMap() method:

```
Inputs:
- self.mapSize = touple with coordinates (max width, max height). 
- minDistance = Minimum path lenght between the initial point and the goal.
- startingPoint = Coordinates of the starting point. It can be set to None for generating the point randomly.
- goal = Coordinated of the goal point. It can be set to None for generating the point randomly.
- wallPercentage = Percentage of the map coordinates that are not accessible,  It can be set to None for generating a value between 30% and 50% is selected.
- folder = Folder where the output data is saved.
- plotMap = If true an image is saved representig the created map.
```
## Map Values
Each coordinate in the generated map is associated with an integer value. The value 0 indicates points considered free, allowing movement from the starting point to the goal. The value 1 is assigned to coordinates that cannot be reached, simulating the presence of a "wall." Other values (different from 0 and 1) can be used to define the start and end of a path, with 2 representing the starting point and 3 representing the goal.

## Outputs
```
Outputs:
- path = Coordinated of the path find between the starting point and the goal.
- completeMap = numpy.ndarray representing the map just created.
- goal = coordinated of the goal point.
- mapSize = Size of the map generated.
- listEmptyPoints = List of coordintes free from walls
```

## Performance
The time required to generate the map and find the path depends on the map's size, the percentage of the map occupied by walls, and the minimum length of the path. Larger maps, higher wall percentages, and longer required paths will increase the generation time.

## Notes
This project serves as a basic example of how a simple map creator can be structured and is open for improvement. It is recommended to use it for generating maps smaller than (30,30).





