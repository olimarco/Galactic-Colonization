import math
import os
import sys
import random
from pathlib import Path

import pygame

ROOT_DIR = Path(__file__).resolve().parent.parent
RESOURCE_DIR = Path(__file__).resolve().parent / "resources"
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from AutoPilotAI import AutoPilotAI
from GalacticCatalog import GalacticCatalog
from GameModels import Route, Spaceship, UniverseGraph


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 760
FPS = 30
AUTO_STEP_MS = 1400

BLACK = (12, 12, 18)
PANEL = (25, 28, 40)
PANEL_DARK = (15, 17, 26)
WHITE = (235, 238, 220)
GREEN = (90, 220, 120)
CYAN = (80, 210, 230)
YELLOW = (245, 210, 90)
RED = (230, 80, 90)
PURPLE = (160, 110, 240)
GRAY = (105, 115, 130)


class PixelButton:
    def __init__(self, rect, label, action):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.action = action

    def draw(self, screen, font, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)
        color = CYAN if hovered else PANEL
        border = WHITE if hovered else GRAY
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, border, self.rect, 3)
        text = font.render(self.label, False, BLACK if hovered else WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


class GalacticColonizationUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Galactic Colonization")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier New", 18, bold=True)
        self.small_font = pygame.font.SysFont("Courier New", 14, bold=True)
        self.big_font = pygame.font.SysFont("Courier New", 30, bold=True)
        self.buttons = [
            PixelButton((840, 665, 190, 34), "AVVIA", self.start_simulation),
            PixelButton((1050, 665, 190, 34), "PAUSA", self.pause_simulation),
            PixelButton((840, 710, 190, 34), "NUOVA", self.new_game),
            PixelButton((1050, 710, 190, 34), "RIEPILOGO", self.toggle_catalog),
        ]
        self.start_button = PixelButton((520, 625, 240, 52), "AVVIA", self.start_from_cover)
        self.screen_mode = "cover"
        self.cover_image = self.load_cover_image()
        self.show_catalog = False
        self.positions = {}
        self.demo_mode = os.environ.get("GALACTIC_DEMO") == "1"
        self.demo_started_at = pygame.time.get_ticks()
        self.demo_step = 0
        self.start_soundtrack()
        self.new_game()

    def load_cover_image(self):
        image_path = RESOURCE_DIR / "image.png"
        if not image_path.exists():
            return None

        image = pygame.image.load(str(image_path)).convert()
        return pygame.transform.smoothscale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def start_soundtrack(self):
        soundtrack_path = RESOURCE_DIR / "Hyperspace_Gateway.mp3"
        if not soundtrack_path.exists():
            return

        try:
            pygame.mixer.music.load(str(soundtrack_path))
            pygame.mixer.music.set_volume(0.45)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    def start_from_cover(self):
        self.screen_mode = "game"
        self.start_simulation()

    def new_game(self):
        self.universe = UniverseGraph(100)
        self.universe.generate_procedural_universe(10)
        self.ship = Spaceship(self.universe.launch_point, 100)
        self.catalog = GalacticCatalog()
        self.auto_pilot = AutoPilotAI(self.universe)
        self.events = []
        self.scan_results = []
        self.resources_by_sector = {}
        self.is_running = False
        self.finished = False
        self.summary_opened = False
        self.show_catalog = False
        self.last_step_time = 0
        self.total_turns = 0
        self.last_route = None
        self.hazard_events = [
            ("TEMPESTA SOLARE", "Scudi ionizzati", (5, 15), (0, 0)),
            ("PIRATI SPAZIALI", "Carico sotto assalto", (3, 10), (5, 20)),
            ("ANOMALIA GRAV", "Rotta corretta a mano", (8, 18), (0, 0)),
            ("ASTEROIDI", "Manovre evasive", (2, 8), (3, 12)),
        ]
        self.calculate_positions()
        self.handle_arrival(self.ship.current_sector)
        self.scan_sector(add_log=False)
        self.log("Pronto. Premi AVVIA per iniziare la simulazione.")

    def start_simulation(self):
        if not self.finished:
            self.show_catalog = False
            self.is_running = True
            self.last_step_time = 0
            self.log("Simulazione avviata.")

    def pause_simulation(self):
        self.is_running = False
        self.log("Simulazione in pausa.")

    def calculate_positions(self):
        vertices = self.universe.core_graph.get_vertices()
        center_x = 510
        center_y = 360
        radius = 205
        self.positions = {}

        for i in range(vertices.size):
            sector = vertices.get(i)
            angle = (2 * math.pi * i) / max(1, vertices.size)
            x = center_x + int(math.cos(angle) * radius)
            y = center_y + int(math.sin(angle) * radius)
            self.positions[sector.id] = (x, y)

    def handle_arrival(self, sector):
        sector.scan()
        self.catalog.log_sector(sector)
        resources = sector.extract_resources()

        if resources > 0:
            self.ship.add_resources(resources)
            self.catalog.log_resources(resources)
            previous_resources = self.resources_by_sector.get(sector.id, 0)
            self.resources_by_sector[sector.id] = previous_resources + resources
            self.log("+" + str(resources) + " RISORSE DA " + sector.id)

        self.trigger_hazard(sector)

    def trigger_hazard(self, sector):
        if random.randint(1, 100) > sector.get_danger_probability():
            return

        name, description, fuel_range, resource_range = random.choice(self.hazard_events)
        fuel_loss = random.randint(fuel_range[0], fuel_range[1])
        resource_loss = random.randint(resource_range[0], resource_range[1])
        actual_resource_loss = min(resource_loss, self.ship.collected_resources)

        self.ship.deduct_fuel(fuel_loss)
        self.ship.collected_resources -= actual_resource_loss
        self.log(name + " IN " + sector.id)
        self.log(description + " | -" + str(fuel_loss) + " fuel")

        if actual_resource_loss > 0:
            self.log("-" + str(actual_resource_loss) + " risorse")

    def scan_sector(self, add_log=True):
        current = self.ship.current_sector
        connected = self.universe.get_connected_sectors(current)
        self.scan_results = []

        for i in range(connected.size):
            sector = connected.get(i)
            self.scan_results.append((sector, self.get_route_cost(current, sector)))

        if add_log:
            self.log("Analisi rotte da " + current.id + " completata.")

    def autopilot_step(self):
        if not self.ship.is_operational():
            self.finished = True
            self.is_running = False
            self.open_summary_once()
            self.log("Simulazione terminata: carburante esaurito.")
            return

        current = self.ship.current_sector
        next_sector = self.auto_pilot.calculate_next_move(current, self.ship.fuel)

        if next_sector is None:
            self.ship.deduct_fuel(self.ship.fuel)
            self.finished = True
            self.is_running = False
            self.open_summary_once()
            self.log("Simulazione terminata: nessuna rotta sostenibile.")
            return

        route_cost = self.get_route_cost(current, next_sector)
        if route_cost is None:
            self.finished = True
            self.is_running = False
            self.open_summary_once()
            self.log("Simulazione terminata: rotta non trovata.")
            return

        self.ship.move_to(next_sector, route_cost)
        self.catalog.log_route(Route(next_sector, route_cost), current)
        self.last_route = (current.id, next_sector.id)
        self.total_turns += 1
        self.log("Turno " + str(self.total_turns) + ": " + current.id + " -> " + next_sector.id)
        self.log("Consumo rotta: -" + str(route_cost) + " carburante")
        self.handle_arrival(next_sector)
        self.scan_sector(add_log=False)

        if not self.ship.is_operational():
            self.finished = True
            self.is_running = False
            self.open_summary_once()
            self.log("Simulazione terminata: carburante esaurito.")

    def open_summary_once(self):
        if not self.summary_opened:
            self.show_catalog = True
            self.summary_opened = True

    def toggle_catalog(self):
        self.show_catalog = not self.show_catalog

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

    def log(self, message):
        self.events.insert(0, message)
        self.events = self.events[:10]

    def run(self):
        running = True

        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.screen_mode == "cover":
                        if self.start_button.rect.collidepoint(mouse_pos):
                            self.start_button.action()
                    else:
                        for button in self.buttons:
                            if button.rect.collidepoint(mouse_pos):
                                button.action()

            if self.screen_mode == "game":
                self.update_demo_mode()
                self.update_auto_simulation()
                self.draw(mouse_pos)
            else:
                self.update_demo_mode()
                self.draw_cover(mouse_pos)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.mixer.music.stop()
        pygame.quit()

    def update_auto_simulation(self):
        if not self.is_running or self.finished:
            return

        now = pygame.time.get_ticks()
        if self.last_step_time == 0 or now - self.last_step_time >= AUTO_STEP_MS:
            self.last_step_time = now
            self.autopilot_step()

    def update_demo_mode(self):
        if not self.demo_mode:
            return

        elapsed = pygame.time.get_ticks() - self.demo_started_at

        if self.demo_step == 0 and elapsed > 1200:
            self.start_from_cover()
            self.demo_step = 1
        elif self.demo_step == 1 and elapsed > 4500:
            self.new_game()
            self.start_simulation()
            self.demo_step = 2
        elif self.demo_step == 2 and elapsed > 7500:
            self.new_game()
            self.start_simulation()
            self.demo_step = 3
        elif self.demo_step == 3 and elapsed > 10500:
            self.new_game()
            self.start_simulation()
            self.demo_step = 4

    def handle_key(self, key):
        if self.screen_mode == "cover":
            if key in (pygame.K_SPACE, pygame.K_RETURN):
                self.start_from_cover()
            return

        if key == pygame.K_n:
            self.new_game()
        elif key == pygame.K_SPACE:
            if self.is_running:
                self.pause_simulation()
            else:
                self.start_simulation()
        elif key == pygame.K_c:
            self.toggle_catalog()

    def draw_cover(self, mouse_pos):
        if self.cover_image is not None:
            self.screen.blit(self.cover_image, (0, 0))
        else:
            self.screen.fill(BLACK)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 70))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render("GALACTIC COLONIZATION", False, GREEN)
        subtitle = self.font.render("Simulazione automatica di esplorazione", False, WHITE)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 520)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 570)))
        self.start_button.draw(self.screen, self.font, mouse_pos)

    def draw(self, mouse_pos):
        self.screen.fill(BLACK)
        self.draw_header()
        self.draw_map()
        self.draw_side_panel()
        self.draw_event_panel()
        self.draw_bottom_panel(mouse_pos)

        if self.show_catalog:
            self.draw_catalog_overlay()

    def draw_header(self):
        title = self.big_font.render("GALACTIC COLONIZATION", False, GREEN)
        self.screen.blit(title, (30, 22))
        subtitle = self.small_font.render("Simulazione automatica di esplorazione galattica", False, CYAN)
        self.screen.blit(subtitle, (34, 58))

    def draw_map(self):
        area = pygame.Rect(25, 90, 790, 560)
        pygame.draw.rect(self.screen, PANEL_DARK, area)
        pygame.draw.rect(self.screen, GRAY, area, 3)

        vertices = self.universe.core_graph.get_vertices()
        for i in range(vertices.size):
            sector = vertices.get(i)
            edges = self.universe.core_graph.get_adjacent_vertices(sector)
            if edges is not None:
                current = edges.head
                while current is not None:
                    edge = current.data
                    if sector.id < edge.destination.id:
                        line_color = GRAY
                        line_width = 2
                        if self.last_route is not None:
                            route_a, route_b = self.last_route
                            if (
                                route_a == sector.id and route_b == edge.destination.id
                            ) or (
                                route_b == sector.id and route_a == edge.destination.id
                            ):
                                line_color = YELLOW
                                line_width = 5

                        pygame.draw.line(
                            self.screen,
                            line_color,
                            self.positions[sector.id],
                            self.positions[edge.destination.id],
                            line_width
                        )
                    current = current.next

        for i in range(vertices.size):
            sector = vertices.get(i)
            x, y = self.positions[sector.id]
            color = GREEN if sector.is_visited else PURPLE
            if sector == self.ship.current_sector:
                color = YELLOW
            pygame.draw.rect(self.screen, color, (x - 14, y - 14, 28, 28))
            pygame.draw.rect(self.screen, BLACK, (x - 14, y - 14, 28, 28), 3)
            label = self.small_font.render(sector.id, False, WHITE)
            self.screen.blit(label, (x - 13, y + 20))

        self.draw_legend(45, 105)

    def draw_legend(self, x, y):
        self.text("Legenda", x, y, YELLOW, self.small_font)
        self.legend_item(x, y + 28, GREEN, "visitato")
        self.legend_item(x, y + 52, PURPLE, "non visitato")
        self.legend_item(x, y + 76, YELLOW, "nave / ultima rotta")

    def legend_item(self, x, y, color, label):
        pygame.draw.rect(self.screen, color, (x, y + 4, 14, 14))
        pygame.draw.rect(self.screen, BLACK, (x, y + 4, 14, 14), 2)
        self.text(label, x + 24, y, WHITE, self.small_font)

    def draw_side_panel(self):
        panel = pygame.Rect(840, 90, 410, 560)
        pygame.draw.rect(self.screen, PANEL, panel)
        pygame.draw.rect(self.screen, GRAY, panel, 3)

        self.text("NAVICELLA", 865, 112, YELLOW)
        self.text("SETTORE: " + self.ship.current_sector.id, 865, 150, WHITE)
        self.text("CARBURANTE: " + str(self.ship.fuel), 865, 182, GREEN if self.ship.fuel > 20 else RED)
        self.text("RISORSE: " + str(self.ship.collected_resources), 865, 214, CYAN)
        if self.finished:
            status = "TERMINATA"
            status_color = RED
        elif self.is_running:
            status = "IN CORSO"
            status_color = GREEN
        else:
            status = "IN ATTESA"
            status_color = YELLOW
        self.text("STATO: " + status, 865, 246, status_color)
        self.text("TURNI: " + str(self.total_turns), 865, 278, WHITE)

        pygame.draw.line(self.screen, GRAY, (865, 322), (1225, 322), 2)
        self.text("ROTTE DISPONIBILI", 865, 345, YELLOW)
        y = 385
        if len(self.scan_results) == 0:
            self.text("Nessun dato.", 865, y, GRAY)
        else:
            for sector, cost in self.scan_results[:4]:
                color = GREEN if sector.is_visited else WHITE
                row = sector.id + "  fuel " + str(cost) + "  pericolo " + str(sector.danger_level)
                self.text(row, 865, y, color, self.small_font)
                y += 26
                self.text("risorse disponibili: " + str(sector.resources), 890, y, CYAN, self.small_font)
                y += 24

    def draw_event_panel(self):
        panel = pygame.Rect(25, 660, 790, 88)
        pygame.draw.rect(self.screen, PANEL, panel)
        pygame.draw.rect(self.screen, GRAY, panel, 3)
        self.text("EVENTI", 45, 675, YELLOW, self.small_font)

        x = 45
        y = 704
        for message in self.events[:2]:
            self.text(message[:58], x, y, WHITE, self.small_font)
            y += 22

    def draw_bottom_panel(self, mouse_pos):
        for button in self.buttons:
            button.draw(self.screen, self.font, mouse_pos)

        hint = self.small_font.render("Spazio avvia/pausa | N nuova | C riepilogo", False, GRAY)
        self.screen.blit(hint, (845, 748))

    def draw_catalog_overlay(self):
        overlay = pygame.Rect(250, 115, 780, 520)
        pygame.draw.rect(self.screen, BLACK, overlay)
        pygame.draw.rect(self.screen, CYAN, overlay, 4)
        self.text("RIEPILOGO PARTITA", 285, 145, YELLOW)
        self.text("Turni: " + str(self.total_turns), 285, 185, WHITE)
        self.text("Risorse a bordo: " + str(self.ship.collected_resources), 430, 185, CYAN)
        self.text("Carburante finale: " + str(self.ship.fuel), 695, 185, RED if self.ship.fuel <= 0 else GREEN)
        self.text("Totale estratte: " + str(sum(self.resources_by_sector.values())), 285, 220, CYAN, self.small_font)
        self.text("Percorso: " + self.path_summary()[:68], 285, 245, GREEN, self.small_font)

        self.text("SETTORI VISITATI", 285, 295, CYAN)
        y = 325
        for sector in self.visited_sectors()[:7]:
            collected = self.resources_by_sector.get(sector.id, 0)
            row = sector.id + " | pericolo " + str(sector.danger_level) + " | raccolte " + str(collected)
            self.text(row, 285, y, WHITE, self.small_font)
            y += 28

        self.text("ROTTE PERCORSE", 645, 295, CYAN)
        y = 325
        current = self.catalog.known_routes.head
        shown = 0
        while current is not None and shown < 7:
            route = current.data
            source = getattr(route, "source", None)
            source_id = source.id if source is not None else "?"
            row = source_id + " -> " + route.get_destination().id + " | " + str(route.get_cost())
            self.text(row, 645, y, WHITE, self.small_font)
            y += 28
            shown += 1
            current = current.next

        self.text("Premi NUOVA per generare un'altra simulazione.", 285, 590, GRAY, self.small_font)

    def visited_sectors(self):
        sectors = []
        for i in range(self.catalog.visited_sectors.capacity):
            bucket = self.catalog.visited_sectors.buckets.get(i)
            current = bucket.head
            while current is not None:
                sectors.append(current.data.value)
                current = current.next
        return sectors

    def path_summary(self):
        if self.catalog.known_routes.size == 0:
            return self.ship.current_sector.id

        first_route = self.catalog.known_routes.get(0)
        source = getattr(first_route, "source", None)
        path = source.id if source is not None else "?"
        current = self.catalog.known_routes.head

        while current is not None:
            path += " -> " + current.data.get_destination().id
            current = current.next

        return path

    def text(self, content, x, y, color, font=None):
        if font is None:
            font = self.font
        rendered = font.render(content, False, color)
        self.screen.blit(rendered, (x, y))


if __name__ == "__main__":
    GalacticColonizationUI().run()
