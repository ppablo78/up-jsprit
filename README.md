# UP-JSPRIT

The up-jsprit library is a Python package developed in the frame of the [AIRoutePlan](https://www.ai4europe.eu/research/ai-catalog/airouteplan) projet for solving vehicle routing problems integrating the [Unified Planning Library](https://github.com/aiplan4eu/unified-planning) with the [JSprit](https://github.com/graphhopper/jsprit) toolkit. The library provides a seamless interface to work with JSprit functionalities and offers additional utilities to enhance the user experience.
In particular, the library allows to solve VRP problem providing locations coordinates in term of latitude and longitude. Moreovere the optimization is performed using real distances and travel times

## Features

Define and manage locations, vehicles, and shipments.
Extract and parse initial values and goals from input files.
Integrate with the JSprit library using the jpype interface.
(Add any other features or functionalities you have.)

## Installation
To install the package run the command
```bash
pip install up-jsprit
```
The installation includes all the java package needed to execute Jsprit commands
The installation has been successfully tested on following environments:
- Windows 11, python 3.11
- Linux Ubuntu, python 3.11

## Usage

Here's two different basic examples of how to use up-jsprit:
(https:///github.com/aiplan4eu/unified-planning/blob/master/docs/notebooks/01-basic-example.ipynb)
(https://colab.research.google.com/github/aiplan4eu/unified-planning/blob/master/docs/notebooks/01-basic-example.ipynb)

The package is distributed with two examples that shows in details the steps of the processing going through the following main steps:

- Definition of a Vehicle Routing Problem using the unified-planning-library
- Parsing of the Problem to extract features to be translated in the JSprit library formalism
- Call the ip-jsprit Solution Planner for solve the VRP
- Show VRP Solution

The first example is provided as a jupyter notebook available here [![Open In GitHub](https://img.shields.io/badge/see-Github-579aca?logo=github)](https://github.com/ppablo78/up-jsprit/blob/main/test.script/up-jsprit-xy-example.ipynb) and here [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]() and it concerns a VRP where locations coordinates are provided in terms of x and y.

The second example is provided as a jupyter notebook available here [![Open In GitHub](https://img.shields.io/badge/see-Github-579aca?logo=github)](https://github.com/ppablo78/up-jsprit/blob/main/test.script/up-jsprit-geo-example.ipynb) and here [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]() and it concerns a VRP where locations coordinates are provided in terms of latitude and longitude.

The library can be used also running python command through the following step:
1) Create a python file [vrp_domain_generator.py](https://github.com/ppablo78/up-jsprit/blob/main/test.script/vrp_domain_generator.py) that defines the problem domain using the Unified Plannin Library formalism. This file does not need to be changed and it represents the problem domain representation of Vehicle Routing Problems that can be solved by the JSprit engine.
2) Create a python file that represents the VRP. Two examples are provided
   a) [Example 1 - vrp_problem_generator_geo.py](https://github.com/ppablo78/up-jsprit/blob/main/test.script/vrp_problem_generator_xy.py) where the coordinates of locations are provided in terms of x, Y and the distance is calculated as an Euclidean distance
   b) [Example 2 - vrp_problem_generator_geo.py](https://github.com/ppablo78/up-jsprit/blob/main/test.script/vrp_problem_generator_geo) where the coordinates of locations are provided in terms of latitude and longitude. In this case, the distance and the travel time are calculated query, thorugh API, the GraphHopper engine on the basis of real maps and data.
3) Create a file [solve_vrp_problem.py](https://github.com/ppablo78/up-jsprit/blob/main/test.script/solve_vrp_problem.py) that solves the problem  parsing the VRP defined before and using the up-jpsrit library
4) Run the command as follow

```bash
python 
```
The command can be run specifying with following parameters:
- 



## Results

## Testing
To run the tests, navigate to the root directory and use your preferred testing tool:

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

Please make sure to update tests as appropriate.

## License

[GNU General Public License v3.0](https://github.com/ppablo78/up-jsprit/blob/main/LICENSE)

## Contact
Contact
For questions, issues, or feedback, please contact [Paolo Petrinca] at paolo.petrinca@gmail.com
