import random
import jpype
from jpype import JClass
import jpype.imports
from jpype.types import *
import os
import io
import sys

from contextlib import redirect_stdout
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
        self.working_dir = options.get('working_dir', None)
        self.problem_filename = options.get('problem_filename', None)
        self.print_problem = options.get('print_problem', True)
        self.print_solution = options.get('print_solution', True)

   
    def extract_initial_values(self, working_directory, input_filename, output_filename):
        input_filepath = os.path.join(working_directory, input_filename)
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
        output_path = os.path.join(working_directory, output_filename)
    
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

    def extract_goals(self, working_directory, input_filename, output_filename):
        input_filepath = os.path.join(working_directory, input_filename)
        
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
        output_path = os.path.join(working_directory, output_filename)
    
        # Write the extracted lines to the new file in the specified directory
        with open(output_path, 'w') as outfile:
            outfile.writelines(extracted_lines)
    
        print(f"Goals have been extracted to {output_path}!")


    def parse_initial_values(self, working_dir, input_filename):
    
        filename = os.path.join(working_dir, input_filename)
        
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
                    print("FF1 ", shipment_name, location_name)
                    print(locations)
                    # Find the Location with the given name
                    target_location = next((l for l in locations if l.name == location_name), None)
                    if target_location:
                        print("FF2 ", shipment_name, location_name)
                        # Find the Shipment with the given name
                        target_shipment = next((f for f in shipments if f.name == shipment_name), None)
                        print("FF3 ", shipment_name, location_name)
                        #print(target_location.y, target_shipment)
                        if target_shipment:
                            # Assign the location's x and y values to the shipment's attributes
                            target_shipment.initial_location_x = target_location.x
                            target_shipment.initial_location_y = target_location.y
                            print("FF ", target_shipment.initial_location_x)
    
                elif line.startswith("is_at"):
                    vehicle_name, location_name = line.split('(')[1].split(')')[0].split(', ')
                
                    # Find the Location with the given name
                    target_location = next((l for l in locations if l.name == location_name), None)
                    if target_location:
                        # Find the Shipment with the given name
                        target_vehicle = next((f for f in vehicles if f.name == vehicle_name), None)
                        #print(target_location.y, target_shipment)
                        if target_vehicle:
                            # Assign the location's x and y values to the shipment's attributes
                            target_vehicle.initial_location_x = target_location.x
                            target_vehicle.initial_location_y = target_location.y
    
        
        # Printing out the objects and their properties:
        #print("Locations:")
        #for location in locations:
        #    print(location)
    
        #print("\nVehicle Types:")
        #for v_type in vehicle_types:
        #    print(v_type)
    
        #print("\nVehicles:")
        #for vehicle in vehicles:
        #    print(vehicle)
    
        # Printing out the objects and their properties
        #print("A - Shipments:")
        #for shipment in shipments:
        #    print(shipment)
    
        return locations, shipments, vehicles, vehicle_types

    def update_final_locations(self, working_dir, input_filename, locations, shipments, vehicles):
        
        filename = os.path.join(working_dir, input_filename)
        with open(filename, 'r') as file:
            lines = file.readlines()
    
        for line in lines:
            line = line.strip()
    
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
    
        # Printing the results
        #print("\nShipments:")
        #for s in shipments:
        #    print(f"{s.name}: Initial Location - ({s.initial_location_x}, {s.initial_location_y}), Final Location - ({s.final_location_x}, {s.final_location_y})")
    
        #print("\nVehicles:")
        #for v in vehicles:
        #    print(f"{v.name}: Final Location - ({v.final_location_x}, {v.final_location_y})")
        
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

        #jpype.shutdownJVM()
        if not jpype.isJVMStarted():
            # Start JVM
            jpype.startJVM('C:\\Program Files\\Java\\jdk-11.0.16.1\\bin\\server\\jvm.dll')
            print("JVM Started")
        if jpype.isJVMStarted():
            print("JVM already Started")
        
        # Add the path to the jsprit JAR file
        jpype.addClassPath("../jar/slf4j-api-1.7.32.jar")  # Add the path to SLF4J JAR
        jpype.addClassPath("../jar/jsprit-core-1.9.0-beta.11.jar")
        jpype.addClassPath("../jar/logback-core-1.0.11.jar")
        jpype.addClassPath("../jar/logback-classic-1.0.11.jar")
        jpype.addClassPath("../jar/jsprit-io-1.9.0-beta.4.jar")
        jpype.addClassPath("../jar/commons-configuration-1.9.jar")
        jpype.addClassPath("../jar/commons-lang-2.6.jar")
        jpype.addClassPath("../jar/commons-logging-1.1.1.jar")
        jpype.addClassPath("../jar/commons-math-2.1.jar")
        jpype.addClassPath("../jar/commons-math3-3.4.jar")
        jpype.addClassPath("../jar/gs-algo-1.3.jar")
        jpype.addClassPath("../jar/gs-core-1.3.jar")
        jpype.addClassPath("../jar/gs-ui-1.3.jar")
        jpype.addClassPath("../jar/hamcrest-core-1.3.jar")
        jpype.addClassPath("../jar/jcommon-1.0.23.jar")
        jpype.addClassPath("../jar/jfreechart-1.0.19.jar")
        jpype.addClassPath("../jar/jsprit-analysis-1.9.0-beta.11.jar")
        jpype.addClassPath("../jar/junit-4.12.jar")
        jpype.addClassPath("../jar/xml-apis-1.4.01.jar")
        jpype.addClassPath("../jar/mbox2-1.0.jar")
        jpype.addClassPath("../jar/pherd-1.0.jar")
        jpype.addClassPath("../jar/java-util-1.8.3.jar")
        jpype.addClassPath("../jar/scala-library-2.10.1.jar")
        jpype.addClassPath("../jar/xercesImpl-2.12.0.jar")
        jpype.addClassPath("../jar/xml-apis-1.4.01.jar")

        VehicleRoutingProblem = jpype.JClass("com.graphhopper.jsprit.core.problem.VehicleRoutingProblem")
        VehicleRoutingProblemSolution = jpype.JClass("com.graphhopper.jsprit.core.problem.solution.VehicleRoutingProblemSolution")

        #VrpXMLReader = jpype.JClass("com.graphhopper.jsprit.io.problem.VrpXMLReader")
        VehicleRoutingProblemBuilder = jpype.JClass("com.graphhopper.jsprit.core.problem.VehicleRoutingProblem$Builder")
        VehicleImpl = jpype.JClass("com.graphhopper.jsprit.core.problem.vehicle.VehicleImpl")
        VehicleType = jpype.JClass("com.graphhopper.jsprit.core.problem.vehicle.VehicleTypeImpl")
        Location = jpype.JClass("com.graphhopper.jsprit.core.problem.Location")
        LocationBuilder = jpype.JClass("com.graphhopper.jsprit.core.problem.Location$Builder")
        Service = jpype.JClass("com.graphhopper.jsprit.core.problem.job.Service")
        Shipment = jpype.JClass("com.graphhopper.jsprit.core.problem.job.Shipment")
        ShipmentBuilder = jpype.JClass("com.graphhopper.jsprit.core.problem.job.Shipment$Builder")
        Plotter = jpype.JClass("com.graphhopper.jsprit.analysis.toolbox.Plotter")
        vrp_xml = jpype.JClass("com.graphhopper.jsprit.io.problem.VrpXMLReader")
        
        SelectBest = jpype.JClass("com.graphhopper.jsprit.core.algorithm.selector.SelectBest")
        
        SolutionPrinter = jpype.JClass("com.graphhopper.jsprit.core.reporting.SolutionPrinter")
        PrintEnum = jpype.JClass("com.graphhopper.jsprit.core.reporting.SolutionPrinter$Print")

        GraphStreamViewer = jpype.JClass("com.graphhopper.jsprit.analysis.toolbox.GraphStreamViewer")
        
        AlgorithmSearchProgressChartListener = jpype.JClass("com.graphhopper.jsprit.analysis.toolbox.AlgorithmSearchProgressChartListener")
        Jsprit = jpype.JClass("com.graphhopper.jsprit.core.algorithm.box.Jsprit")
        # WaitingTimeCosts = jpype.JClass("com.graphhopper.jsprit.core.problem.cost.VehicleRoutingTransportCosts")
        #WaitingTimeCosts = jpype.JClass("com.graphhopper.jsprit.core.problem.cost.VehicleRoutingTransportCosts")
        Coordinate = jpype.JClass("com.graphhopper.jsprit.core.util.Coordinate")
        VehicleRoutingProblemSolution = jpype.JClass("com.graphhopper.jsprit.core.problem.solution.VehicleRoutingProblemSolution")

        p_locations = []
        p_vehicle_types = []
        p_vehicles = []
        p_shipments = []
        
        
        working_dir = '../test'
        initial_values_filename = "initial_values.txt"
        goals_filename = "goals.txt"

        # Extract Initial Values from the problem and save in a temporary file
        self.extract_initial_values(self.working_dir, self.problem_filename, initial_values_filename)

        # Extract Goals from the problem and save in a temporary file
        self.extract_goals(self.working_dir, self.problem_filename, goals_filename)
        
        # Call the function
        p_locations, p_shipments, p_vehicles, p_vehicle_types = self.parse_initial_values(working_dir, initial_values_filename)
                        
        p_vehicles, p_shipments = self.update_final_locations(working_dir, goals_filename, p_locations, p_shipments, p_vehicles)

        #STEP 0 - BUILD VEHICLE ROUTING PROBLEM
        vrpbuilder = VehicleRoutingProblem.Builder.newInstance()
        #vrpBuilder.setFleetSize(VehicleRoutingProblem.FleetSize.FINITE);

        
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

        
 
        vrp = vrpbuilder.build();
        #print(vrp)

        # Printing out the objects and their properties:

        vra = Jsprit.createAlgorithm(vrp)
        vra.setMaxIterations(self.max_iterations)

        #vra.getAlgorithmListeners().addListener(AlgorithmSearchProgressChartListener("output/sol_progress.png"))

        # Solve the problem
        solutions = vra.searchSolutions()

        # Retrieve the best solution
        bestSolution = SelectBest().selectSolution(solutions)

       
        # Call the print method
        #SolutionPrinter.print(bestSolution)

        viewer = GraphStreamViewer(vrp, bestSolution)
        viewer.labelWith(GraphStreamViewer.Label.ID).setRenderDelay(200).display()

        # Stop JVM
        jpype.shutdownJVM()


        status = up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING
        return up.engines.PlanGenerationResult(status, None, self.name)

    def destroy(self):
        pass
