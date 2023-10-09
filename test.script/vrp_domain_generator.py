import unified_planning as up
from unified_planning.shortcuts import *

def define_vrp_domain():
  
  ###########################################
  # DEFINE DOMAIN
  ##########################################

  #USERTYPEs
  Place = UserType("place")
  VehicleType = UserType("VehicleType")
  Locatable = UserType("Locatable")

  Freight = UserType("Freight", Locatable)
  Vehicle = UserType("Vehicle", Locatable)
  Location = UserType("Location", Locatable)


  #FLUENTs
  #at = Fluent("at", BoolType(), f=Freight, l=Location)
  is_in = Fluent("is_in", BoolType(), f=Freight, l=Location)
  is_at = Fluent("is_at", BoolType(), v=Vehicle, l=Location)
  is_on = Fluent("is_on", BoolType(), f=Freight, v=Vehicle)
  is_of = Fluent("is_of", BoolType(), v=Vehicle, vT=VehicleType)
  using = Fluent("using", BoolType(), v=Vehicle)
  t_earliest = Fluent("t_earliest", IntType(), f=Freight)
  t_latest = Fluent("t_latest", IntType(), f=Freight)
  x = Fluent('x', RealType(), l=Location)
  y = Fluent('y', RealType(), l=Location)
  #value_weight = Fluent('value', RealType(), w=Weight)
  #value_maxLoad = Fluent('value_maxLoad', RealType(), m=MaxLoad)

  # DEFINE FLUENTS FOR SERVICE - PICKUP OR DELIVERY
  weight = Fluent("weight", RealType(), f=Freight)
  loadTime = Fluent("loadTime", RealType(), f=Freight)

  # DEFINE FLUENTS FOR VEHICLE TYPE
  maxLoad = Fluent("maxLoad", RealType(), v=VehicleType)
  fixedCost = Fluent("fixedCost", RealType(), vT=VehicleType)
  variableCost = Fluent("variableCost", RealType(), vT=VehicleType)


  # DEFINE ACTIONS
  drive = InstantaneousAction("drive", v=Vehicle, l_from=Location, l_to=Location)
  v = drive.parameter("v")
  l_from = drive.parameter("l_from")
  l_to = drive.parameter("l_to")

  drive.add_precondition(is_at(v, l_from))

  drive.add_effect(is_at(v, l_to), True)
  drive.add_effect(is_at(v, l_from), False)

  pickup = DurativeAction('pickup', f=Freight, l_from=Location, v=Vehicle, vt=VehicleType) 
  f = pickup.parameter('f')
  l_from = pickup.parameter('l_from')
  v = pickup.parameter('v')
  vt = pickup.parameter('vt')


  pickup.set_fixed_duration(loadTime(f))
  pickup.add_condition(StartTiming(), LE(weight(f), maxLoad(vt)))
  #drive.add_precondition(is_in(f, l_from))

  pickup.add_condition(StartTiming(), is_at(v, l_from))
  pickup.add_condition(StartTiming(), is_in(f, l_from))
  pickup.add_condition(StartTiming(), LE (t_earliest(f), StartTiming()))
  pickup.add_condition(StartTiming(), GE (t_latest(f), StartTiming()))

  #pickup.add_increase_effect(EndTiming(), value_weight(l), value_maxLoad(mL))
  pickup.add_increase_effect(EndTiming(), weight(f), maxLoad(vt))
  pickup.add_effect(EndTiming(), is_in(f, l_from), False)
  pickup.add_effect(EndTiming(), is_on(f, v), True)


  delivery = DurativeAction('delivery', f=Freight, l_to=Location, v=Vehicle, vt=VehicleType)
  f = delivery.parameter('f')
  l_to = delivery.parameter('l_to')
  v = delivery.parameter('v')
  vt = delivery.parameter('vt')


  delivery.set_fixed_duration(loadTime(f))
  #drive.add_precondition(is_in(f, l_from))

  delivery.add_condition(StartTiming(), is_at(v, l_to))
  delivery.add_condition(StartTiming(), not (is_in(f, l_to)))
  delivery.add_condition(StartTiming(), LE (t_earliest(f), StartTiming()))
  delivery.add_condition(StartTiming(), GE (t_latest(f), StartTiming()))
  #delivery.add_condition(StartTiming(), available(f, l_to, t_earliest, t_lastest))

  delivery.add_decrease_effect(EndTiming(), weight(f), maxLoad(vt))
  delivery.add_effect(EndTiming(), is_in(f, l_to), True)
  delivery.add_effect(EndTiming(), is_on(f, v), False)


  return {
        'Place': Place,
        'VehicleType': VehicleType,
        'Locatable': Locatable,
        'Freight': Freight,
        'Vehicle': Vehicle,
        'Location': Location,
        'is_in': is_in,
        'is_at': is_at,
        'is_on': is_on,
        'is_of': is_of,
        'using': using,
        't_earliest': t_earliest,
        't_latest': t_latest,
        'x': x,
        'y': y,
        'weight': weight,
        'loadTime': loadTime,
        'maxLoad': maxLoad,
        'fixedCost': fixedCost,
        'variableCost': variableCost,
        'drive': drive,
        'pickup': pickup,
        'delivery': delivery
    }



