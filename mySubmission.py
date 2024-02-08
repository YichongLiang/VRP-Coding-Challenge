import math
import sys

def distance(p1, p2):
    # Calculate the distance (time)
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def read_loads(file_path):
    # Read input
    loads = []
    with open(file_path, 'r') as f:
        next(f) 
        for line in f:
            parts = line.split()
            load_number = int(parts[0])
            pickup = tuple(map(float, parts[1].strip("()").split(',')))
            dropoff = tuple(map(float, parts[2].strip("()").split(',')))
            loads.append((load_number, pickup, dropoff))
    return loads


def assign_loads(loads):
    # Assign the load to drivers based on the distance
    max_time = 720  
    assignments = []
    remaining_loads = loads.copy()
    depot = (0, 0)  

    while remaining_loads:
        # Looping the loads till no loads 
        driver_loads = []
        current_location = depot
        total_drive_time = 0

        while remaining_loads:
            # Looping the till the current driver is over time 
            next_load = min(remaining_loads, key=lambda load: distance(current_location, load[1]))
            trip_time = distance(current_location, next_load[1])+ distance(next_load[1], next_load[2])
            return_time = distance(next_load[2], depot)  # Time to return to depot

            if (total_drive_time + trip_time + return_time) <= (max_time):
                # If not overtime update location and time
                total_drive_time += trip_time
                current_location = next_load[2]
                driver_loads.append(next_load[0])
                remaining_loads.remove(next_load)
            else:
                break  # This driver over time next one 

        if driver_loads:
            assignments.append(driver_loads)
        else:
            break  # If no loads were assigned exit

    return assignments


def main(file_path):
    loads = read_loads(file_path)
    assignments = assign_loads(loads)
    
    # Print the route of all the driers
    for route in assignments:
        print(route)




if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    file_path = sys.argv[1]
    main(file_path)