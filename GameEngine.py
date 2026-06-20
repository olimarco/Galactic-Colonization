import random

from AutoPilotAI import AutoPilotAI
from GalacticCatalog import GalacticCatalog
from GameModels import Route, Spaceship, UniverseGraph


class GameEngine:
    def __init__(self, universe_size=10, initial_fuel=100):
        self.universe_size = universe_size
        self.initial_fuel = initial_fuel
        self.universe = UniverseGraph(universe_size * universe_size)
        self.ship = None
        self.catalog = GalacticCatalog()
        self.auto_pilot = AutoPilotAI(self.universe)
        self.hazard_events = [
            {
                "name": "Tempesta solare",
                "description": "Le radiazioni danneggiano gli scudi e consumano carburante.",
                "fuel_loss_range": (5, 15),
                "resource_loss_range": (0, 0)
            },
            {
                "name": "Pirati spaziali",
                "description": "Un assalto improvviso causa perdita di carburante e risorse.",
                "fuel_loss_range": (3, 10),
                "resource_loss_range": (5, 20)
            },
            {
                "name": "Anomalia gravitazionale",
                "description": "La nave corregge la rotta consumando carburante extra.",
                "fuel_loss_range": (8, 18),
                "resource_loss_range": (0, 0)
            },
            {
                "name": "Campo di asteroidi",
                "description": "Le manovre evasive disperdono parte del carico raccolto.",
                "fuel_loss_range": (2, 8),
                "resource_loss_range": (3, 12)
            }
        ]

    def start_game(self):
        self.universe.generate_procedural_universe(self.universe_size)
        self.ship = Spaceship(self.universe.launch_point, self.initial_fuel)
        self.handle_arrival_events(self.ship.current_sector)
        self.turn_loop()

    def turn_loop(self):
        while self.ship.is_operational():
            print("\n--- Turno di gioco ---")
            print("Settore attuale:", self.ship.current_sector.id)
            print("Carburante:", self.ship.fuel)
            print("Risorse raccolte:", self.ship.collected_resources)

            should_continue = self.execute_user_action()
            if not should_continue:
                break

        print("\nPartita terminata.")
        print("Risorse totali raccolte:", self.ship.collected_resources)

    def execute_user_action(self):
        print("\n1. Consulta catalogo")
        print("2. Scansiona settore")
        print("3. Procedi con autopilota")
        print("4. Termina partita")

        choice = input("Scegli un'azione: ")

        if choice == "1":
            self.catalog.display_catalog()
        elif choice == "2":
            self.display_scan_report()
        elif choice == "3":
            self.move_with_autopilot()
        elif choice == "4":
            return False
        else:
            print("Scelta non valida.")

        return True

    def print_path(self):
        print(f"\n{'=' * 50}")
        print("  PERCORSO DELL'AUTOPILOT")
        print("=" * 50)

        percorso = [self.ship.current_sector.id]

        while self.ship.is_operational():
            current_sector = self.ship.current_sector
            next_sector = self.auto_pilot.calculate_next_move(current_sector, self.ship.fuel)

            if next_sector is None:
                break

            # Trova costo arco
            edges = self.universe.core_graph.get_adjacent_vertices(current_sector)
            edge = edges.head
            fuel_cost = None
            while edge is not None:
                if edge.data.destination == next_sector:
                    fuel_cost = edge.data.weight
                    break
                edge = edge.next

            if fuel_cost is None:
                break

            self.ship.move_to(next_sector, fuel_cost)
            next_sector.scan()
            extracted = next_sector.extract_resources()
            self.ship.add_resources(extracted)
            percorso.append(next_sector.id)

        # Stampa percorso
        print(f"\n  {' → '.join(percorso)}")

    def move_with_autopilot(self):
        current = self.ship.current_sector
        next_sector = self.auto_pilot.calculate_next_move(current, self.ship.fuel)

        if next_sector is None:
            print("Nessuna mossa disponibile.")
            self.ship.deduct_fuel(self.ship.fuel)
            return

        route_cost = self.get_route_cost(current, next_sector)

        if route_cost is None:
            print("Errore: il settore scelto non è collegato a quello attuale.")
            return

        self.ship.move_to(next_sector, route_cost)
        self.catalog.log_route(Route(next_sector, route_cost), current)
        self.handle_arrival_events(next_sector)
        self.print_path()

    def handle_arrival_events(self, sector):
        sector.scan()
        self.catalog.log_sector(sector)

        extracted = sector.extract_resources()
        if extracted > 0:
            self.ship.add_resources(extracted)
            self.catalog.log_resources(extracted)
            print("Risorse estratte:", extracted)

        self.trigger_hazard(sector)

    def trigger_hazard(self, sector):
        danger_probability = sector.get_danger_probability()
        hazard_roll = random.randint(1, 100)

        if hazard_roll <= danger_probability:
            event = random.choice(self.hazard_events)
            fuel_loss = random.randint(
                event["fuel_loss_range"][0],
                event["fuel_loss_range"][1]
            )
            resource_loss = random.randint(
                event["resource_loss_range"][0],
                event["resource_loss_range"][1]
            )

            self.ship.deduct_fuel(fuel_loss)
            actual_resource_loss = min(resource_loss, self.ship.collected_resources)
            self.ship.collected_resources -= actual_resource_loss

            print("Imprevisto nel settore:", sector.id)
            print("Evento:", event["name"])
            print(event["description"])
            print("Carburante perso:", fuel_loss)
            if actual_resource_loss > 0:
                print("Risorse perse:", actual_resource_loss)

    def display_scan_report(self):
        current = self.ship.current_sector
        connected = self.universe.get_connected_sectors(current)

        print("\nScansione settore", current.id)
        if connected.size == 0:
            print("Nessun settore confinante rilevato.")
            return

        for i in range(connected.size):
            sector = connected.get(i)
            route_cost = self.get_route_cost(current, sector)
            print(
                sector.id,
                "- pericolo:",
                sector.danger_level,
                "- carburante necessario:",
                route_cost,
                "- risorse disponibili:",
                sector.resources,
                "- visitato:",
                sector.is_visited
            )

    def get_route_cost(self, source, destination):
        edges = self.universe.core_graph.get_adjacent_vertices(source)

        if edges is None:
            return None

        current = edges.head
        while current is not None:
            edge = current.data
            if edge.destination == destination:
                return edge.weight
            current = current.next

        return None
