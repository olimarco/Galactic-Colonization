from DataStructures import HashTable, LinkedList

class GalacticCatalog:
    def __init__(self):
        self.visited_sectors = HashTable(100)
        self.known_routes = LinkedList()
        self.extracted_resources = 0
    
    def log_sector(self, s):
        self.visited_sectors.put(s.id, s)

    def log_route(self, r):
        self.known_routes.add(r)

    def log_resources(self, amount):
        self.extracted_resources += amount
    
    def display_catalog(self):
        print("\n--- Catalogo Galattico ---")
        print("Settori visitati:", self.visited_sectors.size)
        print("Risorse estratte:", self.extracted_resources)
        print("Rotte conosciute:", self.known_routes.size)
