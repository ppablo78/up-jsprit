# UP-JSPRIT

The up-jsprit library is a Python package developed in the frame of the [AIRoutePlan](https://www.ai4europe.eu/research/ai-catalog/airouteplan) project for solving vehicle routing problems integrating the [Unified Planning Library](https://github.com/aiplan4eu/unified-planning) with the [JSprit](https://github.com/graphhopper/jsprit) toolkit. The library provides a seamless interface to work with JSprit functionalities and offers additional utilities to enhance the user experience.
In particular, the library allows to solve VRP problem providing locations coordinates in term of latitude and longitude. Moreover, the optimization is performed using real distances and travel times.
The package is distributed at the following [link](https://pypi.org/project/up-jsprit) in the PiPy repository.

## Features

The up-jsprit library allows to define a wide range of Vehicle Route Problems specifying:
- locations using latitude and longitude coordinates or x and y coordinates
- characteristics of the key actions:
  - pickup: it represents the load of a good from a customer placed at a certain location to the vehicle
  - delivery: it represents the unload of a good from a vehicle to the Customer placed in a certain location
- characteristics of vehicles:
  - load capacity: the maximum capacity that can be loaded on a vehicle
  - fixed cost: cost that does not depend on the travel distance
  - variable cost: cost that depend on the travel distance
- characteristics of the item to be served:
   - time window availability
   - weight of each item
   - time needed for completing the service (delivery or pickup)

The results can be visualized  as text files or georeferenced maps

Opportunely combining these elements it is possible to build complex examples like: 
- **CVRP** (Capacitated Vehicle Routing Problem): it is a VRP in which Vehicles have a limited carrying capacity of the goods that must be delivered
- **DVRP** (Durative Vehicle Routing Problem): a classic VRP in which a duration is assigned to each action
- **VRPTW** (Vehicle Routing Problem with Time Window): it is a generalization of the VRP where the service at any customer starts within a given time interval, called a time window
- **MDVRP** (Multi Depot Vehicle Routing Problem): is a route optimization problem that involves selecting the most-effective route to deliver goods or services from multiple depots to a group of clients.
- **VRPD** (Vehiclei Routing with Pickups and Deliveries) is a VRP in which the possibility that customers return some commodities is contemplated. In VRPPD it’s needed to take into account that the goods that customers return to the delivery vehicle must fit into
- **VRPBTW** (Vehicle Routing Problem with Backhauls and Time Windows): involves the pickup and delivery of goods at different customer locations, with earliest and latest time deadlines, and varying demands. The demands are serviced using capacitated vehicles with limited route time. Moreover, all deliveries (linehauls) must be done before the pickups (backhauls)

## Installation
To install the package run the command
```bash
pip install up-jsprit
```
The installation includes all the java package needed to execute Jsprit commands
The installation has been successfully tested on following environments:
- Windows 11, python 3.11
- Linux Ubuntu 22.04, python 3.11

## Usage

The [up-jsprit](https://pypi.org/project/up-jsprit/) library has been created as a python package available on the PiPy repository.
The package is composed by following files:
-	[up-jsprit.py](https://github.com/ppablo78/up-jsprit/blob/main/up-jsprit/up-jsprit.py): this file defines the main content of the library and extends the “solve” function of the Unified Planning Library to interface the planning engine of the Jsprit toolkit. The class includes also functionalities to parse VRP problems defined using unified-planning-library formalism and ingest them to the Jsprit planning engine
-	[utils.py](https://github.com/ppablo78/up-jsprit/blob/main/up-jsprit/utils.py): this file defines additional functionalities needed to interface the GraphHopper routing services through API. These functionalities are needed when the VRP is defined using geocoordinates (latitude and longitude) and the solution is based on real values of distance and travel time between location. For using these functionalities, the User must provide its own API_KEY (https://www.graphhopper.com/)

The package is distributed with two examples (Jupyter and Google Colab notebook) that detail the steps of the processing going through the following main steps:
- Definition of a Vehicle Routing Problem using the unified-planning-library
- Parsing of the Problem to extract features to be translated in the JSprit library formalism
- Call the ip-jsprit Solution Planner for solve the VRP
- Show VRP Solution

The first example is provided as a jupyter notebook available here [![Open In GitHub](https://img.shields.io/badge/see-Github-579aca?logo=github)](https://github.com/ppablo78/up-jsprit/blob/main/test.script/up-jsprit-xy-example.ipynb) and here [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1F9G96iv9TFssabA17mNlfn-tDPbngTY-?usp=drive_link) and it concerns a VRP where locations coordinates are provided in terms of x and y.

The second example is provided as a jupyter notebook available here [![Open In GitHub](https://img.shields.io/badge/see-Github-579aca?logo=github)](https://github.com/ppablo78/up-jsprit/blob/main/test.script/up-jsprit-geo-example.ipynb) and here [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1sPsYICO3MTLgl_0dCI444e1miBZGhy6H?usp=drive_link) and it concerns a VRP where locations coordinates are provided in terms of latitude and longitude.

The library can be used also running python command through the following step:
1) Create a python file [vrp_domain_generator.py](https://github.com/ppablo78/up-jsprit/blob/main/test.script/vrp_domain_generator.py) that defines the problem domain using the Unified Planning Library formalism. This file does not need to be changed and it represents the problem domain representation of Vehicle Routing Problems that can be solved by the JSprit engine.
2) Create a python file that represents the VRP. Two examples are provided:
   - [Example 1 - vrp_problem_generator_geo.py](https://github.com/ppablo78/up-jsprit/blob/main/test.script/vrp_problem_generator_xy.py) where the coordinates of locations are provided in terms of x, Y and the distance is calculated as an Euclidean distance
   -  [Example 2 - vrp_problem_generator_geo.py](https://github.com/ppablo78/up-jsprit/blob/main/test.script/vrp_problem_generator_geo) where the coordinates of locations are provided in terms of latitude and longitude. In this case, the distance and the travel time are calculated query, through API, the GraphHopper engine on the basis of real maps and data.
4) Create a file [solve_vrp_problem.py](https://github.com/ppablo78/up-jsprit/blob/main/test.script/solve_vrp_problem.py) that solves the problem  parsing the VRP defined before and using the up-jpsrit library
5) Executing the solve_vrp_problem.py providing an input file as follow

```bash
python solve_vrp_problem.py -input .\vrp_problem_generator_xy.py
```

The command can be run specifying following options:
- -input specify the VRP problem to be analyzed. The problem shall be defined using the unified-planning-library conventions and following the examples provided.
- -iter: set the maximum number of iterations of the JSprit engine. Default value: 2000
- -debug: boolean input to define if additional info are printed out during the execution. Default value: False.
- -geo: boolean input to define if the problem shall be solved interpreting the coordinates of locations as latitude and longitude. If set to True, the API_KEY for GraphHopper services is needed to calculate the real values for distance and travel time. Moreover, the API_KEY is needed to calculate the routes of the solution and visualize them on a georeferenced map. Default value: False.
-  -api: the API_KEY for GraphHopper services needed to enable search of solution using georeferenced data.
-  -view: boolean input to define if the viewer used by JSprit to visualize the solution at the end of the process is enabled or not. Default value: True.

An example is shown below

```bash
python solve_vrp_problem.py -iter 200 -input .\vrp_problem_generator_geo.py --debug False --geo True -api 36d16024-8b24-4091-bb89-7adef7632a20 -view True
```

## Results

The up-jsprit library generates, at the end of the process, following files as output: 
- [routes_map.html](https://github.com/ppablo78/up-jsprit/blob/main/output/routes_map.html) is an html page that show the routes planned
- [BestSolution.txt](https://github.com/ppablo78/up-jsprit/blob/main/output/bestSolution.txt) is the solution. For each route it is specified
  - the type of activity (start, pickup, deliver, end)
  - the arrival time
  - the departure time costs
- [SolutionPlot.png](https://github.com/ppablo78/up-jsprit/blob/main/output/solutionPlot.png) shows the solution on a simple graph. It is automatically produced by the JSprit library
- [solution_progress.png](https://github.com/ppablo78/up-jsprit/blob/main/output/solution_progress.png) shows the progress of the solution as function of the iterations

Other text files are produced when parsing the problem:

- [goals.txt](https://github.com/ppablo78/up-jsprit/blob/main/output/goals.txt) contains the info related to the goals to achieve. This file is further parsed by the up-jpsrit library and injested to th Jsprit engine solver
- [initial values.txt](https://github.com/ppablo78/up-jsprit/blob/main/output/initial_values.txt) contains the info related to the intial values of the VRP. This file is further parsed by the up-jpsrit library and injested to th Jsprit engine solver

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

Please make sure to update tests as appropriate.

## License

[GNU General Public License v3.0](https://github.com/ppablo78/up-jsprit/blob/main/LICENSE)

## Contact
Contact
For questions, issues, or feedback, please contact [Paolo Petrinca] at paolo.petrinca@gmail.com
