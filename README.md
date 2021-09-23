# Open-Street-Map-Pathfinder
A pathfinding program using OpenStreetMaps

Using recursion it can detect dead-ends and back track far enough back to find a different path


*There is a noticeable performance decrease when used in an area with many nodes (ie, large cities)*


![demo](animation.gif)


*An example of a path with a minimum distance of 10k*


Parameters:
 - Output
    - True to show every step of the path (including animation), false to only show the final path
 - Origin
    - A point to serve as the starting location, the closest node (intersection) will be chosen as the origin
 - Distance
    - the minimum distance that the path must be (in metres)
