import math
import random
import numpy as np
import matplotlib.pyplot as plt


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, mapSize):
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
    passaggi = 0
    size = mapSize[0] * mapSize[1]
    # Loop until you find the end
    while len(open_list) > 0:
        if passaggi > size * 10:
            return None
        passaggi += 1
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
            # return path[::-1] # Return reversed path
            return path
        # Generate children
        children = []
        for new_position in [
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]:  # Adjacent squares
            # Get node position
            node_position = (
                current_node.position[0] + new_position[0],
                current_node.position[1] + new_position[1],
            )
            # Make sure within range
            if (
                node_position[0] > (len(maze) - 1)
                or node_position[0] < 0
                or node_position[1] > (len(maze[len(maze) - 1]) - 1)
                or node_position[1] < 0
            ):
                continue
            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 1:
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
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                (child.position[1] - end_node.position[1]) ** 2
            )
            child.f = child.g + child.h
            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            # Add the child to the open list
            open_list.append(child)


class MapGenerator:
    def __init__(
        self,
        mapSize="example",
        minDistance=5,
        startingPoint=None,
        goal=None,
        wallPercentage=None,
        folder="",
        plotMap=True,
    ):
        """
        Create the 2D map.

        Inputs:
        - self.mapSize = touple with coordinates (max width, max height).
        - minDistance = Minimum path lenght between the initial point and the goal.
        - startingPoint = Coordinates of the starting point.
        - goal = Coordinated of the goal point.
        - wallPercentage = Percentage of the map coordinates that are not accessible, if empty a value between 30% and 50% is selected.
        - folder = Folder where the output data is saved.
        - plotMap = If true an image is saved representig the created map.

        Outputs:
        - path = Coordinated of the path find between the starting point and the goal.
        - completeMap = numpy.ndarray representing the map just created.
        - goal = coordinated of the goal point.
        - mapSize = Size of the map generated.
        - listEmptyPoints = List of coordintes free from walls.

        - if plotMap is True:
            Plot representing the new map.
        """
        self.folder = folder
        self.plotMap = plotMap
        if mapSize == "example":
            self.mapSize = (random.randrange(8, 12), random.randrange(8, 12))
        else:
            self.mapSize = mapSize

        if wallPercentage is None:
            self.wallPercentage = random.randrange(30, 50)
        else:
            self.wallPercentage = wallPercentage

        if startingPoint is None:
            self.startingPoint = (
                random.randrange(0, self.mapSize[0]),
                random.randrange(0, self.mapSize[1]),
            )
        else:
            self.startingPoint = startingPoint

        self.goal = goal
        while self.goal == None:
            # choose randomly the goal with the minimunm distance specified
            goal = (
                random.randrange(0, self.mapSize[0] - 1),
                random.randrange(0, self.mapSize[1] - 1),
            )
            dist = math.sqrt(
                sum([(a - b) ** 2 for a, b in zip(goal, self.startingPoint)])
            )
            if dist > minDistance:
                self.goal = goal

    def mapCreator(self):
        # Create an empty map of the designed size.
        BasicMap = np.zeros(self.mapSize)
        # Assign the start and the end point in the map.
        BasicMap[self.startingPoint] = 2
        BasicMap[self.goal] = 3
        # Create a list with all the map's points not occupated.
        xempty, yempty = np.where(BasicMap == 0)
        coordinates = []
        for x, y in zip(xempty, yempty):
            coordinates.append((x, y))
        # Here the number of positions in the map occupated by walls, is calculated.
        wallPoints = round((len(coordinates) / 100) * self.wallPercentage)
        path = None
        while path is None:
            completeMap = BasicMap.copy()
            # Random coordinates in the map are chosen and are set as not available (wall).
            wallCoordinates = random.sample(coordinates, k=wallPoints)
            # Using the A* algorithm, check if there is at least one path between the start and the goal.
            for wallPoint in wallCoordinates:
                completeMap[wallPoint] = 1
            path = astar(completeMap, self.startingPoint, self.goal, self.mapSize)
            if path is not None:
                self.path = path
                self.completeMap = completeMap
                continue

        if self.plotMap is True:
            self._savePlotMap()

        xempty, yempty = np.where(self.completeMap != 1)
        listEmptyPoints = []
        for x, y in zip(xempty, yempty):
            listEmptyPoints.append([x, y])

        return (
            self.path,
            self.completeMap,
            self.mapSize,
            self.startingPoint,
            self.goal,
            listEmptyPoints,
        )

    def _savePlotMap(self):
        for i in range(1, 4):
            x, y = np.where(self.completeMap == i)
            if i == 1:
                walls = plt.scatter(x, y, color="red", marker="s")
            elif i == 2:
                start = plt.scatter(x, y, color="blue", marker="x", s=150)
            elif i == 3:
                end = plt.scatter(x, y, color="black", s=150)

        # draw the path between start and end point
        xCoord = [p[0] for p in self.path]
        yCoord = [p[1] for p in self.path]
        plt.plot(xCoord, yCoord, color="green")

        plt.legend(
            (walls, start, end),
            ("walls", "start", "end"),
            loc="center left",
            bbox_to_anchor=(1, 0.5),
        )
        title = "Map of size {} startingpoint {} and goal in {}".format(
            self.mapSize, self.startingPoint, self.goal
        )
        plt.title(title)
        plt.savefig(title + ".png")


if __name__ == "__main__":
    MapGenerator = MapGenerator(mapSize=(10, 10), minDistance=5, wallPercentage=50)
    (
        path,
        completeMap,
        mapSize,
        startingPoint,
        goal,
        listEmptyPoints,
    ) = MapGenerator.mapCreator()
