import math
import random
import time
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
    size = mapSize[0] * mapSize[1]
    # Loop until you find the end
    start = time.time()
    while len(open_list) > 0:
        # Stop A* if it is taking too long to find a path.
        end = time.time()
        if (end - start) > 30:
            return None
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

        self.path = None
        self.mapSize = mapSize
        self.goal = goal
        self.folder = folder
        self.plotMap = plotMap
        self.minDistance = minDistance
        self.startingPoint = startingPoint
        self.wallPercentage = wallPercentage
        self.basicMap = np.zeros(self.mapSize)

        if self.goal is not None:
            assert (
                self.goal[0] < self.mapSize[0] and self.goal[1] < self.mapSize[1]
            ), "the goal point is outside the map!"

        if self.startingPoint is not None:
            assert (
                self.startingPoint[0] < self.mapSize[0]
                and self.startingPoint[1] < self.mapSize[1]
            ), "the starting point is outside the map!"

        if wallPercentage is None:
            self.wallPercentage = random.randrange(30, 50)

    def createMap(self):
        print("Creating a new map..")
        start = time.time()
        while self.path is None:
            completeMap = self.basicMap.copy()
            completeMap = self._CreateRandomWalls(completeMap)
            if self.startingPoint is None:
                # Create a list with all the map's points not occupated.
                availableCoord = MapGenerator._findFreeCoordinates(completeMap)
                self.startingPoint = random.choice(availableCoord)
            completeMap[self.startingPoint[0], self.startingPoint[1]] = 2

            if self.goal is None:
                # Create a list with all the map's points not occupated.
                availableCoord = MapGenerator._findFreeCoordinates(completeMap)
                self.goal = random.choice(availableCoord)
            completeMap[self.goal[0], self.goal[1]] = 3

            # Using the A* algorithm, check if there is at least one path between the start and the goal.
            path = astar(completeMap, self.startingPoint, self.goal, self.mapSize)
            if path is not None and len(path) > self.minDistance:
                self.path = path
                self.completeMap = completeMap
                continue
            # Set a different timer for different map sizes, if the map size is bigger than (50,50) it will take more time to
            # try the map creation multiple times before giving up.
            if self.mapSize[0] < 30 and self.mapSize[1] < 30:
                maxTime = 120
            else:
                maxTime = 360

            end = time.time()
            assert (
                end - start
            ) < maxTime, "I can't create a map, try to lower the wallPercentage or the minDistance values"

        print("The map i ready!")
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

    @staticmethod
    def _findFreeCoordinates(map):
        xCoords, yCoords = np.where(map == 0)
        availableCoord = []
        for x, y in zip(xCoords, yCoords):
            availableCoord.append((x, y))
        return availableCoord

    def _CreateRandomWalls(self, completeMap):
        # Create a list with all the map's points not occupated.
        availableCoord = MapGenerator._findFreeCoordinates(self.basicMap)
        # Here the number of positions in the map occupated by walls, is calculated.
        wallPoints = round((len(availableCoord) / 100) * self.wallPercentage)
        # Random coordinates in the map are chosen and are set as not available (wall).
        wallCoordinates = random.sample(availableCoord, k=wallPoints)
        for wallPoint in wallCoordinates:
            completeMap[wallPoint] = 1
        return completeMap

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
            bbox_to_anchor=(1.05, 1),
            loc=2,
            borderaxespad=0.0,
        )
        title = "Map of size {} startingpoint {} and goal in {}".format(
            self.mapSize, self.startingPoint, self.goal
        )
        plt.tight_layout()
        plt.savefig(title + ".png")


if __name__ == "__main__":
    MapGenerator = MapGenerator(
        mapSize=(44, 44),
        #  startingPoint=(0, 0),
        #  goal=(10, 3),
        minDistance=12,
        wallPercentage=40,
    )
    (
        path,
        completeMap,
        mapSize,
        startingPoint,
        goal,
        listEmptyPoints,
    ) = MapGenerator.createMap()
