import json


def calculate_euclidean_distance(point1,point2):
    """
    Calculates Euclidean distance between two points
    Formula : sqrt((x2-x1)^2 + (y2-y1)^2)
    """ 
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    return ( (x2-x1)**2 + (y2-y1)**2 ) **0.5

def load_data():
    """
    Reads the data from json input file
    """
    with open("base_case.json") as file:
        data = json.load(file)
        return data


data = load_data()

# gets the attribute values from input
warehouses = data['warehouses']
agents = data['agents']
packages = data['packages']

# mapping of warehouse id to nearest agent id 
warehouse_agent_mapping = {}
warehouse_id_location_mapping = {}
# loop to find nearest agent for each warehouse
for warehouse in warehouses:
    warehouse_location = warehouse['location']
    warehouse_id_location_mapping[warehouse['id']] = warehouse_location
    min_distance = None
    nearest_agent = None
    for agent in agents:
        agent_location = agent['location']
        current_distance = calculate_euclidean_distance(
            agent_location,
            warehouse_location
        )
        if (min_distance is None) or (current_distance < min_distance) : 
            min_distance = current_distance
            nearest_agent = agent

    warehouse_agent_mapping[warehouse['id']] = nearest_agent['id']

# agent to package mapping
agent_package_mapping = {}
agent_id_location_mapping = {}
for agent in agents:
    agent_id = agent['id']
    agent_id_location_mapping[agent_id] = agent['location']
    agent_package_mapping[agent_id] = []

for package in packages:
    warehouse_id = package['warehouse_id']
    agent_id = warehouse_agent_mapping[warehouse_id]
    package_id = package['id']
    agent_package_mapping[agent_id].append(package_id)



# Now we have agent to package mapping
# start delivering packages 

delivery_report = {}

for agent in agents:
    agent_id = agent['id']
    delivery_report[agent_id] = {
        "packages_delivered" : 0,
        "total_distance":0,
        "efficiency":0
    }


for agent_id,report in delivery_report.items():
    warehouse_id = None
    for key,value in warehouse_agent_mapping.items():
        if value == agent_id:
            warehouse_id = key
            break
    warehouse_location = warehouse_id_location_mapping[warehouse_id]
    agent_location = agent_id_location_mapping[agent_id]
    # initial travel of agent to warehouse
    initial_distance = calculate_euclidean_distance(agent_location,warehouse_location)
    delivery_report[agent_id]["total_distance"] = initial_distance
    current_location = warehouse_location
    for package_id in agent_package_mapping[agent_id]:
        for package in packages:
            if package["id"] == package_id:
                destination = package["destination"]
                break
        package_distance = calculate_euclidean_distance(
            current_location,
            destination
        )
        delivery_report[agent_id]["total_distance"] += package_distance
        current_location = destination
        delivery_report[agent_id]["packages_delivered"] += 1

best_agent = None
best_efficiency = float("inf")
for agent_id, report in delivery_report.items():
    if report["packages_delivered"] > 0:
        report["total_distance"] = round(
            report["total_distance"], 2
        )
        report["efficiency"] = round(
            report["total_distance"] / report["packages_delivered"],
            2
        )
        if report["efficiency"] < best_efficiency:
            best_efficiency = report["efficiency"]
            best_agent = agent_id

delivery_report["best_agent"] = best_agent


# Save report to JSON
with open("report.json", "w") as file:
    json.dump(delivery_report, file, indent=4)

print("Report saved successfully to report.json")
