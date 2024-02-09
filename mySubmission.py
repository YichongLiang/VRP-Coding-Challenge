import math
import sys

# To run the code with problem set simply run: python mySubmission.py {./path/to/problem}
# For example: python mySubmission.py ./trainingProblems/problem1.txt
# For evaluation run: python3 evaluateShared.py --cmd "python3 mySubmission.py" --problemDir trainingProblems
# Training Set Mean Cost: 48941.53  Mean Run Time: 60.29ms

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
            return_time = distance(next_load[2], depot)  # Time for returning to the depot

            if (total_drive_time + trip_time + return_time) <= (max_time):
                # If not overtime update location and time
                total_drive_time += trip_time
                current_location = next_load[2]
                driver_loads.append(next_load[0])
                remaining_loads.remove(next_load)
            else:
                # See if potential load can add on the way back
                for potential_load in remaining_loads:
                    extra_trip_time = distance(current_location, potential_load[1]) + distance(potential_load[1], potential_load[2])
                    extra_return_time = distance(potential_load[2], depot)
                    if (total_drive_time + extra_trip_time + extra_return_time) <= (max_time):
                        total_drive_time += extra_trip_time
                        current_location = potential_load[2]
                        driver_loads.append(potential_load[0])
                        remaining_loads.remove(potential_load)
                        break 
                break  # This driver over time next one 

        if driver_loads:
            assignments.append(driver_loads)
        else:
            break  # If no loads were assigned exit

    return assignments

def main(file_path):
    loads = read_loads(file_path)
    assignments = assign_loads(loads)
    
    # Print the route of all the drivers
    for route in assignments:
        print(route)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    file_path = sys.argv[1]
    main(file_path)
