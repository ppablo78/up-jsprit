import os

import argparse
from importlib import import_module
import importlib.util
import unified_planning as up
from unified_planning import engines
from unified_planning.shortcuts import OneshotPlanner
from unified_planning.shortcuts import *
from up_jsprit import config



def load_module_from_path(module_name, path_to_file):
    spec = importlib.util.spec_from_file_location(module_name, path_to_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Execute a planning problem.')
    parser.add_argument('-output_dir', '--output_dir', type=str, default='.\\output', help='Directory where are saved the output')
    parser.add_argument('-output', '--output', type=str, default='bestSolution.txt', help='File name containing the best Solution')
    parser.add_argument('-input', '--input', type=str, default='vrp_problem_generator_1', help='Path to the problem file')
    parser.add_argument('-iter', '--iterations', type=int, default=400, help='Max number of iterations')
    parser.add_argument('-geo', '--geocoordinates', type=bool, default=False, help='Specify if Distance Matrix and Time MAtrix shall be evaluated using georeferenced coordinates')
    parser.add_argument('-debug', '--debug', type=bool, default=False, help="Enable debug mode")
    parser.add_argument('-api', '--api', type=str, default='', help="API KEY for Graphopper")
    parser.add_argument('-view', '--view', type=bool, default=False, help="Plot Solution on Viewer")

    args = parser.parse_args()
    
    
    # Define the directory where the results are saved
    if args.output_dir:
        config.OUTPUT_DIRECTORY = args.output_dir
    else:
        config.OUTPUT_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')
    
    # Check if the directory exists, and if not, create it
    if not os.path.exists(config.OUTPUT_DIRECTORY):
         os.makedirs(config.OUTPUT_DIRECTORY)

    module_name = os.path.splitext(os.path.basename(args.input))[0]
    module = load_module_from_path(module_name, args.input)

    # Generate the VRP problem
    problem = module.generate_vrp_problem()
   
    # Save the parsed problem in a text file
    with open(os.path.join(config.OUTPUT_DIRECTORY, 'parsed_problem.txt'), 'w') as file:
        file.write(str(problem))

    # Set the environment
    env = up.environment.get_environment()
    env.factory.add_engine('jspritplanner', 'up_jsprit', 'JSpritSolver')

    # Execute the planning code
    # SUBSTITUTE THE API_KEY VALUE
    with OneshotPlanner(name='jspritplanner', params={'max_iterations': args.iterations, 'output_dir': args.output_dir, 'problem_filename': 'parsed_problem.txt', 'solution_filename': args.output, 'geocoordinates': args.geocoordinates, 'debug': args.debug, 'api' : 'XXX', 'view' : args.view}) as p:
        result = p.solve(problem)
        if result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING:
            print(f'{p.name} found a valid plan!')
            print(result.plan)
        else:
            print('No plan found!')

if __name__ == '__main__':
    main()
