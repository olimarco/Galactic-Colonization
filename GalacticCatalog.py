from DataStructures import HashTable, LinkedList

class GalacticCatalog:
    def __init__(self):
        self.visited_sectors = HashTable(100)
        self.known_routes = LinkedList()
        self.extracted_resources = 0
    
    def log_sector(self, s):
        self.visited_sectors.put(s)

    def log_route(self, r):
        self.known_routes.add(r)
    
    def display_catalog(self):
        print("blabla")
        # Sistemare Display catalog per fargli stampare il tutto in modo ordinato #