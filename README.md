[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://vscode.dev/github/olimarco/Galactic-Colonization)
# Algorithms and Data Structures Project

## Galactic Colonization: Deep Space Explorer

## Project Description
The student is required to implement a space exploration simulator in which a Hero commanding a spaceship must colonize galactic sectors to gather resources. The mission takes place in a vast and unknown universe where fuel management is the main constraint for survival. The student will have to handle:
 * Implementing the creation of the Universe in a procedural and random manner, ensuring that each simulation presents a different sector topology.
 * Implementing a discovery log (Galactic Catalog) that allows monitoring of extracted resources, visited sectors, and known hyperspace routes.
 * Implementing the random placement of resources and galaxies within the generated sectors, balancing the difficulty based on the available fuel.
 * Implementing the turn-based game system and the related interactions between the user and the game environment, including the management of environmental unforeseen events.

## Turn Structure and Unforeseen Events
The game takes place in a sequence of turns. In each turn, the spaceship makes a move to an adjacent sector (consuming the relative fuel).
### Management of Unforeseen Events:
 * Upon entering a new sector, the system must calculate whether an unforeseen event occurs based on the "Danger Level" of the sector itself.
 * Unforeseen events are created at the students' discretion (e.g., solar storms, space pirates, gravitational anomalies).
 * Each unforeseen event must result in an additional loss of fuel, reducing the spaceship's autonomy beyond the standard cost of the move.
At the end of the move (and any unforeseen event), the system must allow the user to choose among the following actions:
 * Consult the Galactic Catalog: View the list of already visited galaxies, accumulated resources, and discovered routes.
 * Sector Scan: Perform an analysis of the hyperspace connections of the current sector to know the number of connected, unvisited galaxies and their relative danger level.
 * Continue Exploration: Automatically choose (It must be determined by an algorithm and not a user choice) the next sector to move to among the connected ones.

## Generation Constraints
The generation of the galactic system must take into account the factors described below:
### Creation of the Universe
The universe must be created at each game startup in a random manner but with some structural constraints:
 * Connectivity: Each generated sector must have from 1 to 5 hyperspace connections to other sectors.
 * Reachability: Isolated sectors cannot exist; there must always be at least one path between any pair of sectors.
 * Danger Level: Each sector must be associated with a value from 0 to 100 representing the percentage probability of an unforeseen event occurring when entering that sector.
 * Movement Costs: Each hyperspace connection must be associated with a variable fuel cost, which affects path planning.
 * Starting Sector: Only one galaxy must be indicated as the initial "Launch Point".
 * Colonization Objective: Total resources are distributed randomly (value 0-100 per galaxy). The goal is to maximize resource recovery before the spaceship runs out of its initially assigned fuel quota.

## Project Management Instructions
The game can be implemented either with a graphical user interface or in terminal text mode at the student's choice.
The use of data structures already implemented in Python libraries is not allowed; for every Data Structure required and covered in the course, an object-oriented implementation will be necessary.
The student has to use GitHub tools for project management (Issues, Branches, Commits, Pull Requests) and must produce a technical report containing a description of the architectural choices and algorithms adopted to be submitted 5 days before the written exam. 
