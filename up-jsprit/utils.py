import requests
import folium
import polyline
from . import config #for package distribuition
#import config #for local distribution

def get_route_from_graphhopper(start, end, api_key):
    url = f"https://graphhopper.com/api/1/route?point={start[0]},{start[1]}&point={end[0]},{end[1]}&vehicle=car&locale=en&key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "paths" in data and len(data["paths"]) > 0 and "points" in data["paths"][0]:
            # Decode the polyline
            coords = polyline.decode(data["paths"][0]["points"])
            return coords
        else:
            print("Unexpected response format or no paths found.")
            return None
    else:
        print(f"GraphHopper API returned a {response.status_code} status.")
        return None

def get_distance_and_time_from_graphhopper(API_KEY, point1, point2):
    base_url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{point1['latitude']},{point1['longitude']}", f"{point2['latitude']},{point2['longitude']}"],
        "vehicle": "car",
        "type": "json",
        "key": API_KEY
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()

    # Extract distance and time from the response
    distance = data["paths"][0]["distance"]
    time = data["paths"][0]["time"]

    return distance, time

def generate_map(bestSolution):

    results = []
    i = 1
    for r in bestSolution.getRoutes():
        activities = r.getActivities()
        j = 1


        # Get Coordinates of the start location of the Route (depot at start)
        depot_start = r.getStart()
        depot_start_location = depot_start.getLocation()
        depot_start_coordinates = depot_start_location.getCoordinate()
        depot_start_x = depot_start_coordinates.getX()
        depot_start_y = depot_start_coordinates.getY()

        # Get Coordinates of the end location of the Route (depot at end)
        depot_end = r.getEnd()
        depot_end_location = depot_end.getLocation()
        depot_end_coordinates = depot_end_location.getCoordinate()
        depot_end_x = depot_end_coordinates.getX()
        depot_end_y = depot_end_coordinates.getY()

        print("DEPOT 1 x ", depot_start_x, " Y ", depot_start_y)

        # build an n-tuple for storing main information: N. route, N. Activity, Latitude, Longitude, Is Depot, Vehicle, Activity, Job, Arrival Time, Departure Time
        result_tuple = (i, 0, depot_start_x/10000, depot_start_y/10000, True,  r.getVehicle(), r.getStart().getName(), '-', '-', '-')
        results.append(result_tuple)
        
        for act in activities:
            location = act.getLocation()
            print("Location ", j, " Route n. ", i, " ", location, ' Name ', location.getName())

            coordinate = location.getCoordinate()
            x_value = coordinate.getX()
            y_value = coordinate.getY()

            # Create the n-tuple containing latitude and longitude
            result_tuple = (i, j, x_value/10000, y_value/10000, False, r.getVehicle(), act.getName(), act.getJob().getId(), act.getArrTime(), act.getEndTime())
            results.append(result_tuple)
            j += 1

        
        result_tuple = (i, j, depot_end_x/10000, depot_end_y/10000, True, r.getVehicle(), r.getEnd().getName(), '-', r.getEnd().getArrTime(), '-')
        results.append(result_tuple)
        #print(results[2], " ", results[3])
        i += 1

    #if config.DEBUG:
        # Print all the tuples
        #for result in results:
            #print(result)
    if config.DEBUG==1:
        print("All results:", results)

    # Assuming your waypoints are around a certain area, you can take an average for initial centering
    avg_x = sum([result[2] for result in results]) / len(results)
    avg_y = sum([result[3] for result in results]) / len(results)

    # Create the map
    m = folium.Map(location=[avg_x, avg_y], zoom_start=13)

    # Create a dictionary to store feature groups for each route
    feature_groups = {}

    for idx, result in enumerate(results):
        i, j, lat, lon, isdepot, vehicle, activity, job, arrival_time, departure_time = result
        color = "red" if isdepot == True  else config.COLOR_MAP[i-1]

        # Create a feature group for the route if it doesn't exist
        if i not in feature_groups:
            feature_groups[i] = folium.FeatureGroup(name=f"Route {i}")
        
        # Create Different type of Icons for Pickup and Shipment
        if activity == "pickupShipment":
            icon_type = "arrow-up"
        elif activity == "deliverShipment":
            icon_type = "arrow-down"
        elif activity == "start":
            icon_type = "play"
        elif activity == "end":
            icon_type = "stop"
        else:
            icon_type = "cloud"  # default icon"

        folium.Marker(
            location=[lat, lon],
            popup=f"Route {i}, Activity {j}, Job {job}, Type {activity}, Depot {isdepot}, Arrival Time {arrival_time}, Departure Time {departure_time}",
            icon=folium.Icon(color=color, icon=icon_type),
        ).add_to(feature_groups[i])

        if idx < len(results) - 1:
            start = (lat, lon)
            end = (results[idx+1][2], results[idx+1][3])
            
            #if config.DEBUG:
            #    print(f"Checking connection between {start} and {end}")  # Debugging print

            if start != end and i == results[idx+1][0]:  # Ensure start and end are not the same and they belong to the same route

                route_coords = get_route_from_graphhopper(start, end, config.API_KEY)
                
            #    if config.DEBUG:
            #        print("Route Coords:", route_coords)  # Print the coordinates for debugging
                
                if route_coords:
                    polyline_color = config.COLOR_MAP[i-1]
                    polyline = folium.PolyLine([(coord[0], coord[1]) for coord in route_coords], color=polyline_color, opacity=1.0)
                    # Add Polyline to the FeatureGroup
                    polyline.add_to(feature_groups[i])

    # Add all feature groups to the map
    for i, group in feature_groups.items():
        group.add_to(m)

    # Add a LayerControl
    folium.LayerControl().add_to(m)

    # Save the map on an html page
    #m.save(os.path.join(config.OUTPUT_DIRECTORY, "routes_map.html"))
    return m