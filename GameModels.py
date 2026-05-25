class Sector:
    def __init__(self, id, danger_level, resources):
        self.id = id
        self.danger_level = danger_level
        self.resources = resources
        self.is_visited = False

    def scan(self):
        self.is_visited = True

    def extract_resources(self):
        extracted = self.resources
        self.resources = 0
        return extracted

    def get_danger_probability(self):
        return self.danger_level

class Route:
    def __init__(self, destination, fuel_cost):
        self.destination = destination
        self.fuel_cost = fuel_cost
    
    def get_cost(self):
        return self.fuel_cost

    def get_destination(self):
        return self.destination
