🧠 Robot Explorer – Autonomous Exploration with Heuristics and Pygame

This project implements an autonomous robot agent capable of exploring a 2D grid-based world filled with obstacles, threats, and collectibles.
The agent uses heuristics, memory, pathfinding, and loop detection to fully explore the environment and reach the exit safely.

The entire behavior is visualized using Pygame.



🧩 Core Features
🔹 1. Heuristic-Based Decision Making

Instead of using Q-Learning or Reinforcement Learning, the robot uses a scoring system to choose the best move every step.

Some examples:

+2000 for moving into an unvisited tile

+1000 for reaching a present

+50000 for reaching the door after exploring everything

-600 for going back to the previous position

-400 for repeating recent moves

Heavy penalties for moving into known obstacles

This creates a dynamic agent that “learns” about the world as it moves.

🔹 2. Memory System

The robot maintains four types of memory:

visitadas → visited cells

conhecidas → seen (discovered) cells

bloqueios_conhecidos → rocks and zombies

presentes_coletados → collected presents

This allows the robot to build an internal model of the world.

🔹 3. Pathfinding (BFS) to Escape Loops

If the robot makes 10 moves without making progress, a loop is detected.

The robot then:

Runs BFS to find the nearest unvisited safe cell

Moves one step toward it

Resumes exploration normally

This prevents the robot from getting stuck walking in circles.

🔹 4. Reachability Detection (DFS)

A DFS is used to determine which cells are reachable given the obstacles discovered so far.

This is essential to know:

Whether the exploration is complete

Whether the exit can be reached safely

🔹 5. Obstacle Handling

Rocks (PD)

Small penalty

Become permanent obstacles

Zombies (Z)

Large penalty

Instantly kill the robot

Robot respawns at the original position

The zombie tile becomes a known obstacle

Prevents repeated deaths

🔹 6. Graphical Visualization with Pygame

Each element of the grid is drawn on screen:

Robot

Presents

Exit door

Zombies

Rocks

Empty tiles

Grid borders

You can optionally highlight unvisited cells (e.g., with a red overlay).

📦 Code Structure (High-Level)
gerar_grid()

Randomly generates the game map with presents, zombies, rocks, door, and robot.

mover_robo()

Main intelligence function – evaluates all possible moves and chooses the one with the highest heuristic score.

Performs:

Scoring

Memory updates

Obstacle handling

Present collection

Door validation

Loop detection

bfs_caminho()

Breadth-First Search to find paths to safe unexplored tiles.

dfs_mapear_alcancaveis()

Depth-First Search to discover all reachable positions.

aciona_morte_robo()

Handles robot death due to zombies.

🏁 End Condition

Game ends when the robot:

Has explored every reachable cell

Reaches the exit tile S

At the end, the program prints:

Final score

Total presents collected

Zombie deaths

Number of visited cells

Number of known cells

Total discovered obstacles
