from DataStructures import Graph, LinkedList


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


class Spaceship:
    def __init__(self, current_sector, fuel):
        self.current_sector = current_sector
        self.fuel = fuel
        self.collected_resources = 0

    def move_to(self, s, cost):
        self.deduct_fuel(cost)
        self.current_sector = s
    
    def deduct_fuel(self, amount):
        self.fuel -= amount
    
    def add_resources(self, amount):
        self.collected_resources += amount

    def is_operational(self):
        return self.fuel > 0


class UniverseGraph:

    def __init__ (self, capacity = 100):
        self.core_graph = Graph(capacity)
        self.launch_point = None

    def add_sector(self, s):
        self.core_graph.add_vertex(s)

    def add_hyperspace_route(self, source, dest, fuel_cost):
        self.core_graph.add_edge(source, dest, fuel_cost)
        self.core_graph.add_edge(dest, source, fuel_cost)

    def get_connected_sectors(self, s):
        edges = self.core_graph.get_adjacent_vertices (s)
        connected = LinkedList()

        if edges is None:
            return connected

        current = edges.head
        while current != None:
            connected.add(current.data.destination)
            current = current.next

        return connected

    def generate_procedural_universe(self, size):
        pass

    def ensure_connectivity(self):
        pass

    def enforce_max_connections(self):
        pass