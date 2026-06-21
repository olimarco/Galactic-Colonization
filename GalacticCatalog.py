from DataStructures import HashTable, LinkedList

class GalacticCatalog:
    def __init__(self):
        self.visited_sectors = HashTable(100)
        self.known_routes = LinkedList()
        self.extracted_resources = 0
    
    def log_sector(self, s):
        self.visited_sectors.put(s.id, s)

    def log_route(self, r, source=None):
        r.source = source
        self.known_routes.add(r)

    def log_resources(self, amount):
        self.extracted_resources += amount
    
    def display_catalog(self):
        print("\n--- Catalogo Galattico ---")
        print("Settori visitati:", self.visited_sectors.size)
        print("Risorse estratte:", self.extracted_resources)
        print("Rotte conosciute:", self.known_routes.size)
        self.display_visited_sectors()
        self.display_known_routes()
        self.display_path_summary()

    def display_visited_sectors(self):
        print("\nSettori visitati:")
        if self.visited_sectors.size == 0:
            print("Nessun settore visitato.")
            return

        for i in range(self.visited_sectors.capacity):
            bucket = self.visited_sectors.buckets.get(i)
            current = bucket.head

            while current is not None:
                sector = current.data.value
                print(
                    sector.id,
                    "- pericolo:",
                    sector.danger_level,
                    "- risorse residue:",
                    sector.resources
                )
                current = current.next

    def display_known_routes(self):
        print("\nRotte percorse:")
        if self.known_routes.size == 0:
            print("Nessuna rotta percorsa.")
            return

        current = self.known_routes.head
        while current is not None:
            route = current.data
            source = getattr(route, "source", None)
            source_id = source.id if source is not None else "?"
            print(
                source_id,
                "->",
                route.get_destination().id,
                "- costo carburante:",
                route.get_cost()
            )
            current = current.next

    def display_path_summary(self):
        print("\nPercorso:")
        if self.known_routes.size == 0:
            print("Percorso non ancora iniziato.")
            return

        first_route = self.known_routes.get(0)
        source = getattr(first_route, "source", None)
        if source is None:
            print("Percorso non disponibile.")
            return

        path = source.id
        current = self.known_routes.head
        while current is not None:
            route = current.data
            path += " -> " + route.get_destination().id
            current = current.next

        print(path)
