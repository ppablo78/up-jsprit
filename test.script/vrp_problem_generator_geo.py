import unified_planning as up
from unified_planning.shortcuts import *
from vrp_domain_generator import define_vrp_domain

def generate_vrp_problem():
  
  domain = define_vrp_domain()

  is_in = domain['is_in']
  is_on = domain['is_on']
  is_at = domain['is_at']
  t_earliest = domain['t_earliest']
  t_latest = domain['t_latest']
  weight = domain['weight']
  maxLoad = domain['maxLoad']
  drive = domain['drive']
  delivery = domain['delivery']
  pickup = domain['pickup']
  VehicleType = domain['VehicleType']
  Vehicle = domain['Vehicle']
  Location = domain['Location']
  Freight = domain['Freight']
  loadTime = domain['loadTime']
  fixedCost = domain['fixedCost']
  variableCost = domain['variableCost']
  is_of = domain['is_of']
  x = domain['x']
  y = domain['y']

  ###################################
  # DEFINE PROBLEM
  #####################################

  problem = Problem('VehicleRoutingProblem')

  #problem.add_fluent(at)
  problem.add_fluent(is_in, default_initial_value=False)
  problem.add_fluent(is_on, default_initial_value=False)
  problem.add_fluent(is_at, default_initial_value=False)
  problem.add_fluent(t_earliest, default_initial_value=0)
  problem.add_fluent(t_latest, default_initial_value=100000)

  problem.add_fluent(weight, default_initial_value=0)
  problem.add_fluent(maxLoad, default_initial_value=0)

  problem.add_action(drive)
  problem.add_action(delivery)
  problem.add_action(pickup)

  ##########################################
  # STEP 1 - DEFINE VEHICLE TYPE
  ##########################################

  vt1 = Object("vt1", VehicleType)
  problem.add_object(vt1)

  ##########################################
  # STEP 2 - DEFINE VEHICLE NAME
  ##########################################

  v1 = Object("v1", Vehicle)
  problem.add_object(v1)
  v2 = Object("v2", Vehicle)
  problem.add_object(v2)
  v3 = Object("v3", Vehicle)
  problem.add_object(v3)

  ##########################################
  # STEP 3 - DEFINE LOCATIONS - COORDINATES
  ##########################################

  l0 = Object("l0", Location)
  problem.add_object(l0)
  l1 = Object("l1", Location)
  problem.add_object(l1)
  l2 = Object("l2", Location)
  problem.add_object(l2)
  l3 = Object("l3", Location)
  problem.add_object(l3)
  l4 = Object("l4", Location)
  problem.add_object(l4)
  l5 = Object("l5", Location)
  problem.add_object(l5)
  l101 = Object("l101", Location)
  problem.add_object(l101)

  ##########################################
  # STEP 4 - DEFINE FREIGHT  PARTICIPATING TO DELIVERY OR PICKUP
  ##########################################

  f1 = Object("f1", Freight)
  problem.add_object(f1)
  f2 = Object("f2", Freight)
  problem.add_object(f2)
  f3 = Object("f3", Freight)
  problem.add_object(f3)
  f4 = Object("f4", Freight)
  problem.add_object(f4)
  
  ##########################################
  # STEP 5 - INITIALIZE LOCATION COORDINATES
  ##########################################

  problem.set_initial_value(x(l0), 419028)
  problem.set_initial_value(y(l0), 124964)  
  problem.set_initial_value(x(l1), 418986)
  problem.set_initial_value(y(l1), 124739) 
  problem.set_initial_value(x(l2), 419009)
  problem.set_initial_value(y(l2), 125025)
  problem.set_initial_value(x(l3), 419183)
  problem.set_initial_value(y(l3), 124667)
  problem.set_initial_value(x(l4), 418902)
  problem.set_initial_value(y(l4), 124923)
  problem.set_initial_value(x(l5), 418833)
  problem.set_initial_value(y(l5), 124541)
  problem.set_initial_value(x(l101), 419361) 
  problem.set_initial_value(y(l101), 124690)

  ##########################################
  # STEP 6 DEFINE PROPERTY OF THE SHIPMENT
  #########################################

  problem.set_initial_value(weight(f1), 10)
  problem.set_initial_value(loadTime(f1), 90)
  problem.set_initial_value(t_earliest(f1), 283000)
  problem.set_initial_value(t_latest(f1), 883000)

  problem.set_initial_value(weight(f2), 90)
  problem.set_initial_value(loadTime(f2), 90)
  problem.set_initial_value(t_earliest(f2), 15000)
  problem.set_initial_value(t_latest(f2), 716000)

  problem.set_initial_value(weight(f3), 40)
  problem.set_initial_value(loadTime(f3), 90)
  problem.set_initial_value(t_earliest(f3), 87000)
  problem.set_initial_value(t_latest(f3), 900000)

  problem.set_initial_value(weight(f4), 10)
  problem.set_initial_value(loadTime(f4), 90)
  problem.set_initial_value(t_earliest(f4), 65000)
  problem.set_initial_value(t_latest(f4), 716000)

  
  ##########################################
  # STEP 7 - INITIALIZE MAX CAPACITY OF VEHICLES
  ##########################################

  problem.set_initial_value(maxLoad(vt1),1000)

  ##########################################
  # STEP 8a - INITIALIZE FIXED COSTS AND COST PER SERVICE TIME FOR VEHICLE TYPE
  ##########################################

  problem.set_initial_value(fixedCost(vt1),22)
  problem.set_initial_value(variableCost(vt1),3)

  ##########################################
  # STEP 8b- ASSIGN VEHICLE TYPE TO VEHICLE
  ##########################################

  problem.set_initial_value(is_of(v1, vt1), True)
  problem.set_initial_value(is_of(v2, vt1), True)
  problem.set_initial_value(is_of(v3, vt1), True)

  #######################################################
  # STEP 9- DEFINE INITIAL LOCATION OF SHIPMENTS - PICKUP
  #######################################################

  problem.set_initial_value(is_in(f1, l1), True)
  problem.set_initial_value(is_in(f2, l2), True)
  problem.set_initial_value(is_in(f3, l3), True)
  problem.set_initial_value(is_in(f4, l4), True)

  ##########################################
  # STEP 10 - DEFINE INITIAL LOCATION OF VEHICLES
  ##########################################
  problem.set_initial_value(is_at(v1, l0), True)
  problem.set_initial_value(is_at(v2, l0), True)
  problem.set_initial_value(is_at(v3, l0), True)

  ##########################################
  # STEP 11 a + b + c - DEFINE FINAL LOCATION OF SHIPMENT - DELIVERY
  ##########################################

  problem.add_goal(is_in(f1, l101))
  problem.add_goal(is_in(f2, l101))
  problem.add_goal(is_in(f3, l101))
  problem.add_goal(is_in(f4, l5))

  ##########################################
  # STEP 12 a + b + c- DEFINE FINAL LOCATION OF VEHICLES - DEPOT
  ##########################################

  problem.add_goal(is_at(v1, l101))
  problem.add_goal(is_at(v2, l101))
  problem.add_goal(is_at(v3, l101))

  return problem
