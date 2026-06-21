import random
from DataStructures import Graph, LinkedList, MinPriorityQueue, DisjointSet


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

    def __init__ (self, capacity=100):
        self.core_graph = Graph(capacity)
        self.launch_point = None

    def add_sector(self, s):
        self.core_graph.add_vertex(s)

    def add_hyperspace_route(self, source, dest, fuel_cost):
        self.core_graph.add_edge(source, dest, fuel_cost)
        self.core_graph.add_edge(dest, source, fuel_cost)

    def are_connected(self, source, dest):
        connected = self.get_connected_sectors(source)
        return connected.contains(dest)

    def get_connected_sectors(self, s):
        edges = self.core_graph.get_adjacent_vertices(s)
        connected = LinkedList()
        if edges is None:
            return connected

        current = edges.head
        while current != None:
            connected.add(current.data.destination)
            current = current.next

        return connected

    def generate_procedural_universe(self, size):
        sectors = LinkedList()

        for i in range(size):
            if i == 0:
                sector = Sector("S0", 0, 0)
            else:
                sector = Sector(
                    "S" + str(i),
                    random.randint(0, 100),
                    random.randint(1, 100)
                )
            self.add_sector(sector)
            sectors.add(sector)

            if i == 0:
                self.launch_point = sector

        possible_edges = MinPriorityQueue(size * size)

        for i in range (size):
            for j in range(i + 1, size):
                source = sectors.get(i)
                dest = sectors.get(j)
                fuel_cost = random.randint(5, 30)
                possible_edges.insert((source, dest, fuel_cost), fuel_cost)

        disjoint_set = DisjointSet(size * 2)

        for i in range(size):
            disjoint_set.make_set(sectors.get(i))

        edges_added = 0

        while edges_added < size - 1:
            edge = possible_edges.extract_min()

            if edge is None:
                break

            source, dest, fuel_cost = edge

            if disjoint_set.find_set(source) != disjoint_set.find_set(dest):
                if self.count_connections(source) < 5 and self.count_connections(dest) < 5:
                    self.add_hyperspace_route(source, dest, fuel_cost)
                    disjoint_set.union(source, dest)
                    edges_added += 1

        extra_edges = size // 2
        attempts = 0
        max_attempts = size * size

        while extra_edges > 0 and attempts < max_attempts:
            source_index = random.randint(0, size - 1)
            dest_index = random.randint(0, size - 1)
            attempts += 1

            if source_index != dest_index:
                source = sectors.get(source_index)
                dest = sectors.get(dest_index)

                if not self.are_connected(source, dest):
                    if self.count_connections(source) < 5 and self.count_connections(dest) < 5:
                        fuel_cost = random.randint(5, 30)
                        self.add_hyperspace_route(source, dest, fuel_cost)
                        extra_edges -= 1
            
        self.enforce_max_connections()
        

    def count_connections(self, s):
        connected = self.get_connected_sectors(s)
        return connected.size

    def ensure_connectivity(self):
        vertices = self.core_graph.get_vertices()

        for i in range(vertices.size - 1):
            source = vertices.get(i)
            dest = vertices.get(i + 1)

            if not self.are_connected(source, dest):
                fuel_cost = random.randint(5, 30)
                self.add_hyperspace_route(source, dest, fuel_cost)

    def enforce_max_connections(self):
        vertices = self.core_graph.get_vertices()

        for i in range(vertices.size):
            sector = vertices.get(i)

            if self.count_connections(sector) > 5:
                raise ValueError("Sector has more than 5 connections")
