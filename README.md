# A-star-pathfinding-algorithm
## Introduction
This is an implementation of the A star pathfinding algorithm using Python. This project was inspired by both the YouTube channel 'Tech with Tim' and a medium article by Nicolas Swift on the topic. 

## Operation
The program draws a grid of 'nodes' (squares) on the window, with a barrier around the edge of the grid. The user can then click the left mouse button to choose a 'start' node, and then click it again to choose an 'end' node. Further clicks will create 'barriers' (non-traversable nodes). When the spacebar is pressed, the algorithm will run, showing the pathfinding process in real time. Nodes change colour to indicate membership of the 'open' or 'closed' set. If the end node is found, the path back to the start is traced. If no path is found "Failed to find path" is printed to the console. The following screenshots show the program in action.  

<p align="center">
<img src="https://i.imgur.com/ylWKRqS.png" width="300" height="300">
<img src="https://i.imgur.com/mlBN6wQ.png" width="300" height="300">
<img src="https://i.imgur.com/zbVBvam.png" width="300" height="300">
  </p>
    
## Heuristic
In this implementation, diagonal movement is not allowed. The heuristic used for calculating the distance between two nodes is Manhattan distance, as opposed to Euclidian distance.

Feedback is welcome.
