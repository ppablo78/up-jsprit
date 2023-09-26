# UP-JSPRIT

up-jsprit is a Python package for solving vehicle routing problems using the JSprit library. It provides a seamless interface to work with JSprit functionalities and offers additional utilities to enhance the user experience.

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

## Usage

Here's a basic example of how to use up-jsprit:

```python
from up_jsprit import JSpritSolver

# Define your problem, locations, vehicles, etc.
# ...

# Create a solver instance
solver = JSpritSolver()

# Solve the problem
solution = solver.solve()
```
## Testing
To run the tests, navigate to the root directory and use your preferred testing tool:

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact
Contact
For questions, issues, or feedback, please contact [Your Name] at your.email@example.com.
