import jpype
import jpype.imports
from jpype.types import *
import os
from up_jsprit import config #for local distibution
from up_jsprit.utils import generate_map, get_distance_and_time_from_graphhopper #for local distibution
from typing import Callable, IO, Optional
import unified_planning as up
from unified_planning import engines

class Location_tmp:
    def __init__(self, name):
        self.name = name
        self.x : float = None
        self.y : float = None

    def __repr__(self):
        return f"Location_tmp(Name: {self.name}, X: {self.x}, Y: {self.y})"

class VehicleType_tmp:
    def __init__(self, name):
        self.name = name
        self.max_size = None
        self.fixed_cost = None
        self.variable_cost = None

    def __repr__(self):
        return f"VehicleType_tmp(Name: {self.name}, Max Size: {self.max_size}, Fixed Cost: {self.fixed_cost}, Variable Cost: {self.variable_cost})"

class Vehicle_tmp:
    def __init__(self, name):
        self.name = name
        self.vehicle_type = None
        self.initial_location_x = None
        self.initial_location_y = None
        self.final_location_x = None
        self.final_location_y = None

    def __repr__(self):
        return f"Vehicle_tmp(Name: {self.name}, Vehicle Type: {self.vehicle_type}, Initial Location(X: {self.initial_location_x}, Y: {self.initial_location_y}), Final Location(X: {self.final_location_x}, Y: {self.final_location_y}))"

class Shipment_tmp:
    def __init__(self, name):
        self.name = name
        self.weight: int = None
        self.loadTime: int = None
        self.t_earliest: int = None
        self.t_latest: int = None
        self.initial_location_x: float = None
        self.initial_location_y: float = None
        self.final_location_x: float = None
        self.final_location_y: float = None

    def __repr__(self):
        return f"Shipment_tmp(Name: {self.name}, Weight: {self.weight}, LoadTime: {self.loadTime}, T_earliest: {self.t_earliest}, T_latest: {self.t_latest}, Initial Location(X: {self.initial_location_x}, Y: {self.initial_location_y}), Final Location(X: {self.final_location_x}, Y: {self.final_location_y}))"

# DEFINE A SPECIFIC VEHICLE TYPE REGISTRY TO ASSIGN THE VEHICLE TYPE TO VEHICLE
class VehicleTypeRegistry:
    vehicle_type_map = {}

    @classmethod
    def register_vehicle_type(cls, vehicle_type):
        cls.vehicle_type_map[vehicle_type.getTypeId()] = vehicle_type

    @classmethod
    def get_vehicle_type_by_id(cls, type_id):
        return cls.vehicle_type_map.get(type_id)


class JSpritSolver(up.engines.Engine,
                   up.engines.mixins.OneshotPlannerMixin):
    def __init__(self, **options):
        # Read known user-options and store them for using in the `solve` method
        up.engines.Engine.__init__(self)
        up.engines.mixins.OneshotPlannerMixin.__init__(self)
        self.max_iterations = options.get('max_iterations', 2000)
        self.output_dir = options.get('output_dir', '')
        self.problem_filename = options.get('problem_filename', None)
        self.print_problem = options.get('print_problem', True)
        self.solution_filename = options.get('solution_filename', None)
        self.geocoordinates = options.get('geocoordinates', None)
        self.debug = options.get('debug', False)
        self.api = options.get('api', '')
        self.view = options.get('view', False)

        # Check if DEBUG option is set to TRUE
        if self.debug:
            config.DEBUG = True
        
        # Define the directory where the results are saved
        if self.output_dir:
            config.OUTPUT_DIRECTORY = self.output_dir
        else:
            config.OUTPUT_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')
        
        # Check if the directory exists, and if not, create it
        if not os.path.exists(config.OUTPUT_DIRECTORY):
            os.makedirs(config.OUTPUT_DIRECTORY)

        # Set up the Graphopper API KEY 
        if self.api:
            config.API_KEY = self.api

   
    def extract_initial_values(self, input_filename, output_filename, output_directory=None,):
        
        if output_directory is None:
            output_directory = config.OUTPUT_DIRECTORY

        input_filepath = os.path.join(output_directory, input_filename)
        print(input_filepath)
        with open(input_filepath, 'r') as infile:
            lines = infile.readlines()
    
        # Define start and end markers 1
        start_marker = "Freight - Locatable: ["
        end_marker = "]"
    
        # Find the start and end markers in the file
        start_index = next((i for i, line in enumerate(lines) if start_marker in line), None)
        end_index = next((i for i, line in enumerate(lines) if end_marker in line and i > start_index), None)
    
        if start_index is None or end_index is None:
            print("Markers for Freight not found or in unexpected order.")
            return
    
        # Extract the lines between the markers (including the markers)
        extracted_lines = lines[start_index:end_index + 1]
    
        # Define start and end markers 2
        start_marker2 = "Location - Locatable: ["
        end_marker2 = "]"
    
         # Find the start and end markers in the file
        start_index2 = next((i for i, line in enumerate(lines) if start_marker2 in line), None)
        end_index2 = next((i for i, line in enumerate(lines) if end_marker2 in line and i > start_index2), None)
    
        if start_index2 is None or end_index2 is None:
            print("Markers for Location not found or in unexpected order.")
            return
    
        # Extract the lines between the markers (including the markers)
        extracted_lines2 = lines[start_index2:end_index2 + 1]
        
        # Define start and end markers 3
        start_marker3 = "Vehicle - Locatable: ["
        end_marker3 = "]"
    
         # Find the start and end markers in the file
        start_index3 = next((i for i, line in enumerate(lines) if start_marker3 in line), None)
        end_index3 = next((i for i, line in enumerate(lines) if end_marker3 in line and i > start_index3), None)
    
        if start_index3 is None or end_index3 is None:
            print("Markers for Vehicle not found or in unexpected order.")
            return
    
        # Extract the lines between the markers (including the markers)
        extracted_lines3 = lines[start_index3:end_index3 + 1]
    
     # Define start and end markers 4
        start_marker4= "VehicleType: ["
        end_marker4 = "]"
    
         # Find the start and end markers in the file
        start_index4 = next((i for i, line in enumerate(lines) if start_marker4 in line), None)
        end_index4 = next((i for i, line in enumerate(lines) if end_marker4 in line and i > start_index4), None)
    
        if start_index4 is None or end_index4 is None:
            print("Markers for Vehicle Type not found or in unexpected order.")
            return
    
        # Extract the lines between the markers (including the markers)
        extracted_lines4 = lines[start_index4:end_index4 + 1]
    
    
        # Define start and end markers 5
        start_marker5 = "initial values = ["
        end_marker5 = "]"
    
        # Find the start and end markers in the file
        start_index5 = next((i for i, line in enumerate(lines) if start_marker5 in line), None)
        end_index5 = next((i for i, line in enumerate(lines) if end_marker5 in line and i > start_index5), None)
    
        if start_index5 is None or end_index5 is None:
            print("Markers for Initial Values not found or in unexpected order.")
            return
    
        # Extract the lines between the markers (including the markers)
        extracted_lines5 = lines[start_index5:end_index5 + 1]
        
        # Create the full path for the output file
        output_path = os.path.join(config.OUTPUT_DIRECTORY, output_filename)
    
        # Write the extracted lines to the new file in the specified directory
        with open(output_path, 'w') as outfile:
            outfile.writelines("objects = [\n")
            outfile.writelines(extracted_lines)
            #outfile.writelines(extracted_lines2)
            outfile.writelines(extracted_lines3)
            #outfile.writelines(extracted_lines4)
            outfile.writelines("]\n")
            outfile.writelines(extracted_lines5)
            
        print(f"Initial values have been extracted to {output_path}!")

    def extract_goals(self, input_filename, output_filename, output_directory=None):
        
        if output_directory is None:
            output_directory = config.OUTPUT_DIRECTORY
        
        input_filepath = os.path.join(output_directory, input_filename)
        
        with open(input_filepath, 'r') as infile:
            lines = infile.readlines()
    
        # Define start and end markers
        start_marker = "goals = ["
        end_marker = "]"
    
        # Find the start and end markers in the file
        start_index = next((i for i, line in enumerate(lines) if start_marker in line), None)
        end_index = next((i for i, line in enumerate(lines) if end_marker in line and i > start_index), None)
    
        if start_index is None or end_index is None:
            print("Markers not found or in unexpected order.")
            return
    
        # Extract the lines between the markers (including the markers)
        extracted_lines = lines[start_index:end_index + 1]
    
        # Create the full path for the output file
        output_path = os.path.join(config.OUTPUT_DIRECTORY, output_filename)
    
        # Write the extracted lines to the new file in the specified directory
        with open(output_path, 'w') as outfile:
            outfile.writelines(extracted_lines)
    
        print(f"Goals have been extracted to {output_path}!")


    def parse_initial_values(self, input_filename, output_directory=None):
    
        if output_directory is None:
            output_directory = config.OUTPUT_DIRECTORY

        filename = os.path.join(output_directory, input_filename)
        
        locations = []
        vehicle_types = []
        vehicles = []
        shipments = []
        
        with open(filename, 'r') as file:
            lines = file.readlines()
        
            within_initial_values = False
        
            for line in lines:
                line = line.strip()
    
                if "Location - Locatable:" in line:
                    names = line.split('[')[-1].split(']')[0].split(',')
                    for name in names:
                        locations.append(Location_tmp(name.strip()))
    
                elif "VehicleType:" in line:
                    names = line.split('[')[-1].split(']')[0].split(',')
                    for name in names:
                        vehicle_types.append(VehicleType_tmp(name.strip()))
    
                elif "Vehicle - Locatable:" in line:
                    names = line.split('[')[-1].split(']')[0].split(',')
                    for name in names:
                        vehicles.append(Vehicle_tmp(name.strip()))
                
                elif line.startswith("Freight - Locatable:"):
                    names = line.split('[')[1].split(']')[0].split(', ')
                    for name in names:
                        if not any(s.name == name for s in shipments):  # Avoid duplicate creation
                            shipments.append(Shipment_tmp(name))
    
                elif line.startswith("x("):
                    name = line.split('(')[1].split(')')[0]
                    value = float(line.split(':=')[-1])
                    for location in locations:
                        if location.name == name:
                            location.x = value
    
                elif line.startswith("y("):
                    name = line.split('(')[1].split(')')[0]
                    value = float(line.split(':=')[-1])
                    for location in locations:
                        if location.name == name:
                            location.y = value
    
                elif line.startswith("maxLoad("):
                    name = line.split('(')[1].split(')')[0]
                    value = float(line.split(':=')[-1])
                    for vt in vehicle_types:
                        if vt.name == name:
                            vt.max_size = round(value)
    
                elif line.startswith("fixedCost("):
                    name = line.split('(')[1].split(')')[0]
                    value = float(line.split(':=')[-1])
                    for vt in vehicle_types:
                        if vt.name == name:
                            vt.fixed_cost = value
    
                elif line.startswith("variableCost("):
                    name = line.split('(')[1].split(')')[0]
                    value = float(line.split(':=')[-1])
                    for vt in vehicle_types:
                        if vt.name == name:
                            vt.variable_cost = value
    
                elif line.startswith("weight("):
                    name = line.split('(')[1].split(')')[0]
                    value = float(line.split(':=')[-1])
                    # Check if shipment object exists or create new
                    shipment = next((s for s in shipments if s.name == name), None)
                    if not shipment:
                        shipment = Shipment(name)
                        shipments.append(shipment)
                    shipment.weight = round(value)
    
                elif line.startswith("loadTime("):
                    name = line.split('(')[1].split(')')[0]
                    value = float(line.split(':=')[-1])
                    shipment = next((s for s in shipments if s.name == name), None)
                    if not shipment:
                        shipment = Shipment(name)
                        shipments.append(shipment)
                    shipment.loadTime = value
    
                elif line.startswith("t_earliest("):
                    name = line.split('(')[1].split(')')[0]
                    value = int(line.split(':=')[-1])
                    shipment = next((s for s in shipments if s.name == name), None)
                    if not shipment:
                        shipment = Shipment(name)
                        shipments.append(shipment)
                    shipment.t_earliest = value
    
                elif line.startswith("t_latest("):
                    name = line.split('(')[1].split(')')[0]
                    value = int(line.split(':=')[-1])
                    shipment = next((s for s in shipments if s.name == name), None)
                    if not shipment:
                        shipment = Shipment(name)
                        shipments.append(shipment)
                    shipment.t_latest = value
    
                elif line.startswith("is_of"):
                    vehicle_name, veh_type_name = line.split('(')[1].split(')')[0].split(', ')
                    # Find the Vehicle with the given name
                    target_vehicle = next((v for v in vehicles if v.name == vehicle_name), None)
                    if target_vehicle:
                        target_vehicle.vehicle_type = veh_type_name
    
                elif line.startswith("is_in"):
                    shipment_name, location_name = line.split('(')[1].split(')')[0].split(', ')
                    # Find the Location with the given name
                    target_location = next((l for l in locations if l.name == location_name), None)
                    if target_location:
                        # Find the Shipment with the given name
                        target_shipment = next((f for f in shipments if f.name == shipment_name), None)
                        if target_shipment:
                            # Assign the location's x and y values to the shipment's attributes
                            target_shipment.initial_location_x = target_location.x
                            target_shipment.initial_location_y = target_location.y
    
                elif line.startswith("is_at"):
                    vehicle_name, location_name = line.split('(')[1].split(')')[0].split(', ')
                
                    # Find the Location with the given name
                    target_location = next((l for l in locations if l.name == location_name), None)
                    if target_location:
                        # Find the Shipment with the given name
                        target_vehicle = next((f for f in vehicles if f.name == vehicle_name), None)
                        if target_vehicle:
                            # Assign the location's x and y values to the shipment's attributes
                            target_vehicle.initial_location_x = target_location.x
                            target_vehicle.initial_location_y = target_location.y
    

        if config.DEBUG:
            # Printing out the objects and their properties:
            print("Locations:")
            for location in locations:
                print(location)
        
            print("\nVehicle Types:")
            for v_type in vehicle_types:
                print(v_type)
        
            print("\nVehicles:")
            for vehicle in vehicles:
                print(vehicle)

            print("\nShipments:")
            for shipment in shipments:
                print(shipment)
        
        return locations, shipments, vehicles, vehicle_types

    def update_final_locations(self,  input_filename, locations, shipments, vehicles, output_directory=None):
        
        if output_directory is None:
            output_directory = config.OUTPUT_DIRECTORY
        
        filename = os.path.join(output_directory, input_filename)
        with open(filename, 'r') as file:
            lines = file.readlines()
    
        for line in lines:
            line = line.strip()
    
            # RULE 16
            if line.startswith("is_in"):
                shipment_name, location_name = line.split('(')[1].split(')')[0].split(', ')
                
                # Find the Location with the given name
                target_location = next((l for l in locations if l.name == location_name), None)
                if target_location:
                    # Find the Shipment with the given name
                    target_shipment = next((f for f in shipments if f.name == shipment_name), None)
                    if target_shipment:
                        # Assign the location's x and y values to the shipment's final location attributes
                        target_shipment.final_location_x = target_location.x
                        target_shipment.final_location_y = target_location.y
    
            # RULE 17
            if line.startswith("is_at"):
                vehicle_name, location_name = line.split('(')[1].split(')')[0].split(', ')
                
                # Find the Location with the given name
                target_location = next((l for l in locations if l.name == location_name), None)
                if target_location:
                    # Find the Vehicle with the given name
                    target_vehicle = next((v for v in vehicles if v.name == vehicle_name), None)
                    if target_vehicle:
                        # Assign the location's x and y values to the vehicle's final location attributes
                        target_vehicle.final_location_x = target_location.x
                        target_vehicle.final_location_y = target_location.y
    
        if config.DEBUG:
            # Printing the results of definition of goals
            print("\nShipments:")
            for s in shipments:
                print(f"{s.name}: Initial Location - ({s.initial_location_x}, {s.initial_location_y}), Final Location - ({s.final_location_x}, {s.final_location_y})")
        
            print("\nVehicles:")
            for v in vehicles:
                print(f"{v.name}: Final Location - ({v.final_location_x}, {v.final_location_y})")
            
        return vehicles, shipments

    
    @property
    def name(self) -> str:
        return "JSpritPlanner"

    @staticmethod
    def supported_kind():
        # For this demo we limit ourselves to numeric planning.
        # Other kinds of problems can be modeled in the UP library,
        # see unified_planning.model.problem_kind.
        supported_kind = up.model.ProblemKind()
        supported_kind.set_problem_class("ACTION_BASED")
        supported_kind.set_problem_type("GENERAL_NUMERIC_PLANNING")
        supported_kind.set_typing('FLAT_TYPING')
        supported_kind.set_typing('HIERARCHICAL_TYPING')
        supported_kind.set_numbers('CONTINUOUS_NUMBERS')
        supported_kind.set_numbers('DISCRETE_NUMBERS')
        supported_kind.set_fluents_type('NUMERIC_FLUENTS')
        supported_kind.set_numbers('BOUNDED_TYPES')
        supported_kind.set_fluents_type('OBJECT_FLUENTS')
        supported_kind.set_conditions_kind('NEGATIVE_CONDITIONS')
        supported_kind.set_conditions_kind('DISJUNCTIVE_CONDITIONS')
        supported_kind.set_conditions_kind('EQUALITIES')
        supported_kind.set_conditions_kind('EXISTENTIAL_CONDITIONS')
        supported_kind.set_conditions_kind('UNIVERSAL_CONDITIONS')
        supported_kind.set_effects_kind('CONDITIONAL_EFFECTS')
        supported_kind.set_effects_kind('INCREASE_EFFECTS')
        supported_kind.set_effects_kind('DECREASE_EFFECTS')
        supported_kind.set_effects_kind('FLUENTS_IN_NUMERIC_ASSIGNMENTS')

        return supported_kind

    @staticmethod
    def supports(problem_kind):
        return problem_kind <= JSpritSolver.supported_kind()


    def _solve(self, problem: 'up.model.Problem',
              callback: Optional[Callable[['up.engines.PlanGenerationResult'], None]] = None,
              timeout: Optional[float] = None,
              output_stream: Optional[IO[str]] = None) -> 'up.engines.PlanGenerationResult':
        env = problem.environment

        # Start the JVM and set classpaths
        jpype.getDefaultJVMPath()

        if not jpype.isJVMStarted():
            jpype.startJVM()
            print("JVM Started")
        if jpype.isJVMStarted():
            print("JVM already started")

        # Add the paths to the JAR files
        for jar_file in config.JAR_FILES:
            jpype.addClassPath(jar_file)

        #Import necessary Java From Jsprit classes using JClass
        VehicleRoutingProblem = jpype.JClass("com.graphhopper.jsprit.core.problem.VehicleRoutingProblem")
        VehicleImpl = jpype.JClass("com.graphhopper.jsprit.core.problem.vehicle.VehicleImpl")
        VehicleType = jpype.JClass("com.graphhopper.jsprit.core.problem.vehicle.VehicleTypeImpl")
        Location = jpype.JClass("com.graphhopper.jsprit.core.problem.Location")
        Shipment = jpype.JClass("com.graphhopper.jsprit.core.problem.job.Shipment")
        Plotter = jpype.JClass("com.graphhopper.jsprit.analysis.toolbox.Plotter")
        SelectBest = jpype.JClass("com.graphhopper.jsprit.core.algorithm.selector.SelectBest")
        SolutionPrinter = jpype.JClass("com.graphhopper.jsprit.core.reporting.SolutionPrinter")
        GraphStreamViewer = jpype.JClass("com.graphhopper.jsprit.analysis.toolbox.GraphStreamViewer") 
        AlgorithmSearchProgressChartListener = jpype.JClass("com.graphhopper.jsprit.analysis.toolbox.AlgorithmSearchProgressChartListener")
        Jsprit = jpype.JClass("com.graphhopper.jsprit.core.algorithm.box.Jsprit")
        Coordinate = jpype.JClass("com.graphhopper.jsprit.core.util.Coordinate")
        VehicleRoutingTransportCostsMatrix = jpype.JClass("com.graphhopper.jsprit.core.util.VehicleRoutingTransportCostsMatrix")
        
        # Import necessary Java classes for printing the solution
        PrintWriter = jpype.JClass('java.io.PrintWriter')
        File = jpype.JClass('java.io.File')

        p_locations = []
        p_vehicle_types = []
        p_vehicles = []
        p_shipments = []
        
        # Set file name for saving initial values and goals in two separate text file
        # Get current working directory
        cwd = os.getcwd()

        # Construct path for output directory relative to the test script
        output_directory = config.OUTPUT_DIRECTORY
        initial_values_filename = "initial_values.txt"
        goals_filename = "goals.txt"
        problem_filename = "parsed_problem.txt"

        # Extract Initial Values from the Parsed Problem
        self.extract_initial_values(self.problem_filename, initial_values_filename, output_directory)
        
        # Extract Goals from the Parsed Problem
        self.extract_goals(self.problem_filename, goals_filename, output_directory)

        # Transfer Initial Values to Jsprit Vehicle Routing Problem Definition
        p_locations, p_shipments, p_vehicles, p_vehicle_types = self.parse_initial_values(initial_values_filename, output_directory)

        # Transfer Goals to Jsprit Vehicle Routing Problem Definition
        p_vehicles, p_shipments = self.update_final_locations(goals_filename, p_locations, p_shipments, p_vehicles, output_directory)

        #STEP 0 - BUILD VEHICLE ROUTING PROBLEM
        vrpbuilder = VehicleRoutingProblem.Builder.newInstance()
               
        #STEP 1 - DEFINE VEHICLE TYPES
        for vt in p_vehicle_types:
            vehicle_type_builder = VehicleType.Builder.newInstance(vt.name);
            vehicle_type_builder.addCapacityDimension(vt.max_size, 0);
            vehicle_type_builder.setFixedCost(vt.fixed_cost);
            vehicle_type_builder.setCostPerServiceTime(vt.variable_cost);
            VehicleTypeRegistry.register_vehicle_type(vehicle_type_builder.build())
    
        #STEP 2 - DEFINE VEHICLE
        for v in p_vehicles:
            vehicle_builder = VehicleImpl.Builder.newInstance(v.name)
            vehicle_builder.setStartLocation(Location.newInstance(v.initial_location_x, v.initial_location_y))
            vehicle_builder.setEndLocation(Location.newInstance(v.final_location_x, v.final_location_y))
            vehicle_builder.setType(VehicleTypeRegistry.get_vehicle_type_by_id(v.vehicle_type))
            vrpbuilder.addVehicle(vehicle_builder.build())
            
        #STEP 3 - DEFINE LOCATIONS - COORDINATES   & STEP 5 - INITIALIZE LOCATION COORDINATES
        for l in p_locations:
            location_builder = Location.Builder().setName(l.name)
            coord = Coordinate.newInstance(l.x, l.y)
        
        #STEP 4 - DEFINE FREIGHT PARTICIPATING TO DELIVERY OR PICKUP
        for s in p_shipments:
            shipment_builder = Shipment.Builder.newInstance(s.name)
            shipment_builder.setPickupLocation(Location.newInstance(s.initial_location_x, s.initial_location_y))
            shipment_builder.setDeliveryLocation(Location.newInstance(s.final_location_x, s.final_location_y))
            shipment_builder.addSizeDimension(s.weight,0);
            shipment_builder.setPickupServiceTime(s.loadTime);
            shipment_builder.addPickupTimeWindow(s.t_earliest, s.t_latest);
            vrpbuilder.addJob(shipment_builder.build())
        
        #IF ROUTING COST IS DEFINED to TRUE
        if self.geocoordinates == True:
            
            # Convert x and Y in Latitude and Logitude
            locations = [{"latitude": loc.x/10000, "longitude": loc.y/10000} for loc in p_locations]
            if config.DEBUG:
                print(locations)
    
            costMatrixBuilder = VehicleRoutingTransportCostsMatrix.Builder.newInstance(True)

            # Fill the Distance and Time Matrices:
            for i, loc1 in enumerate(locations):
                for j, loc2 in enumerate(locations):
                    if i < j:  # Only compute for the upper triangle
                        distance, time = get_distance_and_time_from_graphhopper(loc1, loc2)
                        # Format the location dictionaries into the desired string format
                        loc1_str = f"[x={loc1['latitude']*10000:.1f}][y={loc1['longitude']*10000:.1f}]"
                        loc2_str = f"[x={loc2['latitude']*10000:.1f}][y={loc2['longitude']*10000:.1f}]"
                        
                        if config.DEBUG:
                            print(f"{loc1_str}, {loc2_str}, {distance}, {time}")
                        
                        costMatrixBuilder.addTransportDistance(loc1_str, loc2_str, distance)
                        costMatrixBuilder.addTransportTime(loc1_str, loc2_str, time)

            # Build the Cost Matrix
            costMatrix = costMatrixBuilder.build()

            # Set the custom routing costs
            vrpbuilder.setRoutingCost(costMatrix)

        vrp = vrpbuilder.build()
       
        vra = Jsprit.createAlgorithm(vrp)

        # Set the maximum number of iterations
        vra.setMaxIterations(self.max_iterations)

        
        # Print the solution progress as function of the iteration
        vra.getAlgorithmListeners().addListener(AlgorithmSearchProgressChartListener(os.path.join(config.OUTPUT_DIRECTORY, "solution_progress.png")))

        # Solve the problem
        solutions = vra.searchSolutions()

        # Retrieve the best solution
        bestSolution = SelectBest().selectSolution(solutions)
        
        # Create a PrintWriter that writes directly to a file
        with PrintWriter(File(os.path.join(config.OUTPUT_DIRECTORY, self.solution_filename))) as writer:
            SolutionPrinter.print_(writer, vrp, bestSolution, SolutionPrinter.Print.VERBOSE)
        
        # Call the print_ method to capture its output
        SolutionPrinter.print_(vrp, bestSolution, SolutionPrinter.Print.VERBOSE)  # Using the corrected print_ method

        # Plot the solution
        solutionPlot = Plotter(vrp, bestSolution);
        solutionPlot.plot(os.path.join(config.OUTPUT_DIRECTORY, "solutionPlot.png"), "Best Solution");

        # View the solution
        if self.view:
            viewer = GraphStreamViewer(vrp, bestSolution)
            viewer.labelWith(GraphStreamViewer.Label.ID).setRenderDelay(200).display()

        # Get the number of unassigned jobs
        unassigned_jobs = bestSolution.getUnassignedJobs().size()
        # Get the total number of jobs 
        assigned_jobs = vrp.getJobs().values().size()

        # Evaluate the status
        if unassigned_jobs == 0:
            status = up.engines.PlanGenerationResultStatus.SOLVED_OPTIMALLY
        elif unassigned_jobs / assigned_jobs < 0.1:
            status = up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING
        else:
            status = up.engines.PlanGenerationResultStatus.UNSOLVED

        # IF THE PROBLEM TO SOLVE USE GEO COORDINATES GENERATE A GEOREFERENCE MAP
        if self.geocoordinates == True:
            m = generate_map(bestSolution)
            m.save(os.path.join(config.OUTPUT_DIRECTORY, "routes_map.html"))

        # Stop JVM
        jpype.shutdownJVM()

        return up.engines.PlanGenerationResult(status, None, self.name)

    def destroy(self):
        pass
