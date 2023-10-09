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
  l6 = Object("l6", Location)
  problem.add_object(l6)
  l7 = Object("l7", Location)
  problem.add_object(l7)
  l8 = Object("l8", Location)
  problem.add_object(l8)
  l9 = Object("l9", Location)
  problem.add_object(l9)
  l10 = Object("l10", Location)
  problem.add_object(l10)
  l11 = Object("l11", Location)
  problem.add_object(l11)
  l12 = Object("l12", Location)
  problem.add_object(l12)
  l13 = Object("l13", Location)
  problem.add_object(l13)
  l14 = Object("l14", Location)
  problem.add_object(l14)
  l15 = Object("l15", Location)
  problem.add_object(l15)
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
  f5 = Object("f5", Freight)
  problem.add_object(f5)
  f6 = Object("f6", Freight)
  problem.add_object(f6)
  f7 = Object("f7", Freight)
  problem.add_object(f7)
  f8 = Object("f8", Freight)
  problem.add_object(f8)
  f9 = Object("f9", Freight)
  problem.add_object(f9)
  f10 = Object("f10", Freight)
  problem.add_object(f10)
  f11 = Object("f11", Freight)
  problem.add_object(f11)
  f12 = Object("f12", Freight)
  problem.add_object(f12)
  f13 = Object("f13", Freight)
  problem.add_object(f13)
  f14 = Object("f14", Freight)
  problem.add_object(f14)
  f15 = Object("f15", Freight)
  problem.add_object(f15)

  ##########################################
  # STEP 5 - INITIALIZE LOCATION COORDINATES
  ##########################################

  problem.set_initial_value(x(l0), 40)
  problem.set_initial_value(y(l0), 50)
  problem.set_initial_value(x(l1), 5)
  problem.set_initial_value(y(l1), 35)
  problem.set_initial_value(x(l2), 5)
  problem.set_initial_value(y(l2), 45)
  problem.set_initial_value(x(l3), 8)
  problem.set_initial_value(y(l3), 40)
  problem.set_initial_value(x(l4), 8)
  problem.set_initial_value(y(l4), 45)
  problem.set_initial_value(x(l5), 0)
  problem.set_initial_value(y(l5), 45)
  problem.set_initial_value(x(l6), 2)
  problem.set_initial_value(y(l6), 40)
  problem.set_initial_value(x(l7), 0)
  problem.set_initial_value(y(l7), 40)
  problem.set_initial_value(x(l8), 33)
  problem.set_initial_value(y(l8), 35)
  problem.set_initial_value(x(l9), 33)
  problem.set_initial_value(y(l9), 32)
  problem.set_initial_value(x(l10), 35)
  problem.set_initial_value(y(l10), 32)
  problem.set_initial_value(x(l11), 35)
  problem.set_initial_value(y(l11), 30)
  problem.set_initial_value(x(l12), 28)
  problem.set_initial_value(y(l12), 52)
  problem.set_initial_value(x(l13), 28)
  problem.set_initial_value(y(l13), 55)
  problem.set_initial_value(x(l14), 25)
  problem.set_initial_value(y(l14), 50)
  problem.set_initial_value(x(l15), 30)
  problem.set_initial_value(y(l15), 55)
  problem.set_initial_value(x(l101), 25)
  problem.set_initial_value(y(l101), 52)

  ##########################################
  # STEP 6 DEFINE PROPERTY OF THE SHIPMENT
  #########################################

  problem.set_initial_value(weight(f1), 10)
  problem.set_initial_value(loadTime(f1), 90)
  problem.set_initial_value(t_earliest(f1), 283)
  problem.set_initial_value(t_latest(f1), 383)

  problem.set_initial_value(weight(f2), 90)
  problem.set_initial_value(loadTime(f2), 90)
  problem.set_initial_value(t_earliest(f2), 665)
  problem.set_initial_value(t_latest(f2), 716)

  problem.set_initial_value(weight(f3), 40)
  problem.set_initial_value(loadTime(f3), 90)
  problem.set_initial_value(t_earliest(f3), 87)
  problem.set_initial_value(t_latest(f3), 158)

  problem.set_initial_value(weight(f4), 10)
  problem.set_initial_value(loadTime(f4), 90)
  problem.set_initial_value(t_earliest(f4), 665)
  problem.set_initial_value(t_latest(f4), 716)

  problem.set_initial_value(weight(f5), 20)
  problem.set_initial_value(loadTime(f5), 90)
  problem.set_initial_value(t_earliest(f5), 567)
  problem.set_initial_value(t_latest(f5), 624)

  problem.set_initial_value(weight(f6), 30)
  problem.set_initial_value(loadTime(f6), 90)
  problem.set_initial_value(t_earliest(f6), 383)
  problem.set_initial_value(t_latest(f6), 434)

  problem.set_initial_value(weight(f7), 30)
  problem.set_initial_value(loadTime(f7), 90)
  problem.set_initial_value(t_earliest(f7), 479)
  problem.set_initial_value(t_latest(f7), 522)

  problem.set_initial_value(weight(f8), 10)
  problem.set_initial_value(loadTime(f8), 90)
  problem.set_initial_value(t_earliest(f8), 16)
  problem.set_initial_value(t_latest(f8), 80)

  problem.set_initial_value(weight(f9), 10)
  problem.set_initial_value(loadTime(f9), 90)
  problem.set_initial_value(t_earliest(f9), 166)
  problem.set_initial_value(t_latest(f9), 235)

  problem.set_initial_value(weight(f10), 10)
  problem.set_initial_value(loadTime(f10), 90)
  problem.set_initial_value(t_earliest(f10), 264)
  problem.set_initial_value(t_latest(f10), 321)

  problem.set_initial_value(weight(f11), 10)
  problem.set_initial_value(loadTime(f11), 90)
  problem.set_initial_value(t_earliest(f11), 264)
  problem.set_initial_value(t_latest(f11), 321)

  problem.set_initial_value(weight(f12), 20)
  problem.set_initial_value(loadTime(f12), 90)
  problem.set_initial_value(t_earliest(f12), 812)
  problem.set_initial_value(t_latest(f12), 883)

  problem.set_initial_value(weight(f13), 10)
  problem.set_initial_value(loadTime(f13), 90)
  problem.set_initial_value(t_earliest(f13), 732)
  problem.set_initial_value(t_latest(f13), 737)

  problem.set_initial_value(weight(f14), 10)
  problem.set_initial_value(loadTime(f14), 90)
  problem.set_initial_value(t_earliest(f14), 65)
  problem.set_initial_value(t_latest(f14), 144)

  problem.set_initial_value(weight(f15), 40)
  problem.set_initial_value(loadTime(f15), 90)
  problem.set_initial_value(t_earliest(f15), 169)
  problem.set_initial_value(t_latest(f15), 224)

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

  problem.set_initial_value(is_in(f1, l1), True) # in the conversion consider only where is set to TRUE
  problem.set_initial_value(is_in(f2, l2), True)
  problem.set_initial_value(is_in(f3, l3), True)
  problem.set_initial_value(is_in(f4, l4), True)
  problem.set_initial_value(is_in(f5, l5), True)
  problem.set_initial_value(is_in(f6, l6), True)
  problem.set_initial_value(is_in(f7, l7), True)
  problem.set_initial_value(is_in(f8, l8), True)
  problem.set_initial_value(is_in(f9, l9), True)
  problem.set_initial_value(is_in(f10, l10), True)
  problem.set_initial_value(is_in(f11, l11), True)
  problem.set_initial_value(is_in(f12, l12), True)
  problem.set_initial_value(is_in(f13, l13), True)
  problem.set_initial_value(is_in(f14, l14), True)
  problem.set_initial_value(is_in(f15, l15), True)

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
  problem.add_goal(is_in(f4, l101))
  problem.add_goal(is_in(f5, l101))
  problem.add_goal(is_in(f6, l101))
  problem.add_goal(is_in(f7, l101))
  problem.add_goal(is_in(f8, l101))
  problem.add_goal(is_in(f9, l101))
  problem.add_goal(is_in(f10, l101))
  problem.add_goal(is_in(f11, l101))
  problem.add_goal(is_in(f12, l101))
  problem.add_goal(is_in(f13, l101))
  problem.add_goal(is_in(f14, l101))
  problem.add_goal(is_in(f15, l101))

  ##########################################
  # STEP 12 a + b + c- DEFINE FINAL LOCATION OF VEHICLES - DEPOT
  ##########################################

  problem.add_goal(is_at(v1, l101))
  problem.add_goal(is_at(v2, l101))
  problem.add_goal(is_at(v3, l101))

  return problem
