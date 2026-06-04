# 🚀 fly-in 🚀
*This project has been created as part of the 42 curriculum by alluengo*

## **Description**
Welcome to the fly-in project!

This is a pathfinding-algorithm and mapping project from the 42 cursus. The goal is to make a program that, takes a .txt file, such as:
```
nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

and makes the x number of drones reach the goal in the best way possible.

This exercise requires a medium/high python comprehension level, but, overall, big patience and motivation.

## **Instructions**

This programs needs some extrenal libraries for execution.
In the Makefile there are some rules for **installation purposes**:

```
make install
```
This command creates the enviroment file and installs all dependencies needed.
After making make install, execute the next command in the command line:
```
source env/bin/activate
```
This command activates the enviroment. After this step you are ready to execute the program.

There are more rules for **checking purposes**:
```
make lint
```
This command executes ***flake8*** and ***mypy***.

**Flake8** checks the code is following Flake8's international python standards.

**mypy** checks the code is following typing annotations correctly, as the code can have bugs if the definitions are not correct. Type annotations are strictly checked, even though, in almost every case, it is for documentation and code comprehension purposes.

For cleaning purposes, you can execute
```
make clean
```
This cleans the cache and all residual files.

Now, the fun part:
### **Execution**

Write
```
make run
```

***or***

```
make
```
for the program execution.

When the program is executed, it can happen two things:

 - **The program fails.** Errors are captured in try/except blocks, and raised to the terminal for easy debugging. The *parser.py* file is in charge of all errors.

 - **The program runs correctly.** In this case, you will be shown a full resume of the turns needed for the map completion, and the movement of each drone has done in every turn, with colors shown in the terminal.

 You can change the map selection in the Makefile, changing the route of the file in the MAP declaration.

 ## **Resources**

 - Dijkstra algorithm Wiki: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

 - Dijkstra algorithm video explanation: https://www.youtube.com/watch?v=bZkzH5x0SKU

 - Colorama documentation(spanish): https://recursospython.com/guias-y-manuales/colorama-texto-fondo-coloreados-la-consola/

 ### **AI Usage**

 In this project, the AI usage was very restricted for my learning purposes.
 The principal usage was:
 - Documentation on the algorithm creation and implementation
 - Debugging
 - Flake8 and mypy error fixing
 - Optimization

 The code has been originally written by me, and some optimization resources and details where provided by my classmates.

 ## **And now...**

 I am ready to move on! This project was really interesting, as i really like algorithms implementations and visual solutions. This project helped me to improve on python, as i see everything clearer now that i have done it. Drones are interesting, as its starting to replace a lot of things in the daily life, such as delivery, exploration or shows. The map algorithms are also a very important thing in the programming world, as GPS in all type of devices use this kind of code for perfect pathfinding.

 It was really fun, hope you liked this program as much as i did!

 Signed:
 *Alvaro Luengo*