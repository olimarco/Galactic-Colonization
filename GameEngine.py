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

    def start_game(self):
        self.universe.generate_procedural_universe(self.universe_size)
        self.ship = Spaceship(self.universe.launch_point, self.initial_fuel)
        self.handle_arrival_events(self.ship.current_sector)
        self.turn_loop()

    def turn_loop(self):
        while True:
            print("\n--- Turno di gioco ---")
            print("Settore attuale:", self.ship.current_sector.id)
            print("Carburante:", self.ship.fuel)
            print("Risorse raccolte:", self.ship.collected_resources)

            if not self.ship.is_operational():
                print("\nCarburante esaurito! Puoi consultare il catalogo o terminare.")

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
            if not self.ship.is_operational():
                print("Carburante esaurito, impossibile scansionare.")
            else:
                self.display_scan_report()
        elif choice == "3":
            if not self.ship.is_operational():
                print("Carburante esaurito, impossibile muoversi.")
            else:
                self.move_with_autopilot()
        elif choice == "4":
            return False
        else:
            print("Scelta non valida.")

        return True

    def move_with_autopilot(self):
        percorso = [self.ship.current_sector.id]

        while self.ship.is_operational():
            current = self.ship.current_sector
            next_sector = self.auto_pilot.calculate_next_move(current, self.ship.fuel)

            if next_sector is None:
                break

            route_cost = self.get_route_cost(current, next_sector)

            if route_cost is None:
                break

            self.ship.move_to(next_sector, route_cost)
            self.catalog.log_route(Route(next_sector, route_cost))
            self.handle_arrival_events(next_sector)
            percorso.append(next_sector.id)

        if len(percorso) == 1:
            print("Nessuna mossa disponibile.")
            self.ship.deduct_fuel(self.ship.fuel)
            return

        print(f"\n{'=' * 50}")
        print("  PERCORSO DELL'AUTOPILOT")
        print("=" * 50)
        print(f"\n  {' → '.join(percorso)}")

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
            extra_fuel_cost = random.randint(1, max(1, danger_probability // 5))
            self.ship.deduct_fuel(extra_fuel_cost)
            print("Imprevisto nel settore:", sector.id)
            print("Carburante perso:", extra_fuel_cost)

    def display_scan_report(self):
        current = self.ship.current_sector
        connected = self.universe.get_connected_sectors(current)

        print("\nScansione settore", current.id)
        if connected.size == 0:
            print("Nessun settore confinante rilevato.")
            return

        for i in range(connected.size):
            sector = connected.get(i)
            print(
                sector.id,
                "- pericolo:",
                sector.danger_level,
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
