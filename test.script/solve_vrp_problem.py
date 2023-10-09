import sys
import os
# Add the ../test directory to the Python path
#sys.path.append('..\\test')
#sys.path.append('C:\\Users\\paolo\\AI4Planning\\up_jsprit')
import argparse
from importlib import import_module
import importlib.util
import up_jsprit  
import unified_planning as up
from unified_planning import engines
from unified_planning.shortcuts import OneshotPlanner
from unified_planning.shortcuts import *
from up_jsprit import config


# Set the OUTPUT_DIRECTORY immediately after imports
config.OUTPUT_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')
#config.API_KEY = YOUR_API_KEY
config.API_KEY = "36d16024-8b24-4091-bb89-7adef7632a20"

# Check if the directory exists, and if not, create it
if not os.path.exists(config.OUTPUT_DIRECTORY):
    os.makedirs(config.OUTPUT_DIRECTORY)


def load_module_from_path(module_name, path_to_file):
    spec = importlib.util.spec_from_file_location(module_name, path_to_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Execute a planning problem.')
    parser.add_argument('-output', '--output', type=str, default='..\\output\\bestSolution.txt', help='File name containing the best Solution')
    parser.add_argument('-input', '--input', type=str, default='vrp_problem_generator_1', help='Path to the problem file')
    parser.add_argument('-iter', '--iterations', type=int, default=400, help='Max number of iterations')
    parser.add_argument('-geo', '--geocoordinates', type=bool, default=False, help='Specify if Distance Matrix and Time MAtrix shall be evaluated using georeferenced coordinates')
    parser.add_argument('--debug', action='store_true', help="Enable debug mode")
    

    args = parser.parse_args()
    
    if args.debug:
        config.DEBUG = True
    
    module_name = os.path.splitext(os.path.basename(args.input))[0]
    module = load_module_from_path(module_name, args.input)

    # Generate the VRP problem
    problem = module.generate_vrp_problem()
   
    # Save the parsed problem in a text file
    #with open("./output/parsed_problem.txt", 'w') as file:
    with open(os.path.join(config.OUTPUT_DIRECTORY, 'parsed_problem.txt'), 'w') as file:
        file.write(str(problem))

    # Set the environment
    env = up.environment.get_environment()
    env.factory.add_engine('jspritplanner', 'up_jsprit', 'JSpritSolver')

    # Execute the planning code
    with OneshotPlanner(name='jspritplanner', params={'max_iterations': args.iterations, 'working_dir': config.OUTPUT_DIRECTORY, 'problem_filename': 'parsed_problem.txt', 'solution_filename': args.output, 'geocoordinates': args.geocoordinates}) as p:
        result = p.solve(problem)
        if result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING:
            print(f'{p.name} found a valid plan!')
            print(result.plan)
        else:
            print('No plan found!')

if __name__ == '__main__':
    main()
