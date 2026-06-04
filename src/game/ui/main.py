# ==========================================
# Team Number: 3
# Variant Name: main.py
# Student Names: Ivan Lopez, Maria Ortiz, Jenny Leon
# ==========================================

#library imports
import pygame, sys, os

#import other modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import bridge
from algorithms.backtracking import backtracking_algorithm
from algorithms.greedy import greedy_algorithm

#display
window = 400
hud_width = 240
grass = (107, 179, 108)
street = (224, 224, 224)
hud_bg =(45, 45, 48)
text = (240, 240, 240)
textmuted = (150, 150, 150)
blue_btn = (0, 122, 204)
green_btn = (46, 139, 87)
orange_btn = (210, 105, 30)
pygame.font.init()
font_small = pygame.font.SysFont("Arial", 12)
font_medium = pygame.font.SysFont("Arial", 12, bold=True)
font_bold = pygame.font.SysFont("Arial", 13, bold=True)

# Structural Asset
building_options = [
    {"name": "House", "happiness": 50, "color": (70, 130, 180)},
    {"name": "School", "happiness": 75, "color": (218, 165, 32)},
    {"name": "Park", "happiness": 90, "color": (34, 139, 34)},
    {"name": "Hospital", "happiness": 85, "color": (178, 34, 34)}
]

rows = 8
cols = 8
blockSize = 50

grid_data = [[None for _ in range(cols)] for _ in range(rows)]
engine_stats = None

greedy_btn_rect = pygame.Rect(window + 20, 120, hud_width - 40, 35)
backtrack_btn_rect = pygame.Rect(window + 20, 165, hud_width - 40, 35)
sync_btn_rect = pygame.Rect(window + 20, window - 55, hud_width - 40, 35)

#grid
def drawGrid():
    
    for r in range(rows):
        for c in range(cols):
            x = c * blockSize
            y = r * blockSize
            rect = pygame.Rect(x, y, blockSize, blockSize)
            
            cell = grid_data[r][c]
            if cell:
                pygame.draw.rect(screen, cell["color"], rect)
                lbl = font_small.render(cell["name"][:5], True, (255, 255, 255))
                screen.blit(lbl, (x + 4, y + 18))
            else:
                pygame.draw.rect(screen, grass, rect)
                
            pygame.draw.rect(screen, street, rect, 1)

def drawHUD():
    pygame.draw.rect(screen, hud_bg, (window, 0, hud_width, window))
    
    title = font_bold.render("PROJECT HUD CONSOLE", True, text)
    screen.blit(title, (window + 15, 15))
    pygame.draw.line(screen, street, (window + 15, 40), (window + hud_width - 15, 40), 1)
    
    hint = font_small.render("Click cells to cycle items manually.", True, textmuted)
    screen.blit(hint, (window + 15, 50))
    
    # --- PROURAL GENERATION ACTION OPTION LAYOUTS ---
    algo_lbl = font_bold.render("Procedural Generators:", True, text)
    screen.blit(algo_lbl, (window + 15, 95))
    
    pygame.draw.rect(screen, orange_btn, greedy_btn_rect, border_radius=4)
    lbl_g = font_medium.render("RUN GREEDY", True, text)
    screen.blit(lbl_g, lbl_g.get_rect(center=greedy_btn_rect.center))
    
    pygame.draw.rect(screen, green_btn, backtrack_btn_rect, border_radius=4)
    lbl_b = font_medium.render("RUN BACKTRACKING", True, text)
    screen.blit(lbl_b, lbl_b.get_rect(center=backtrack_btn_rect.center))
    
    # --- LIVE DATA STREAM METRIC RENDERS FROM C++ BINARY ---
    pygame.draw.line(screen, street, (window + 15, 220), (window + hud_width - 15, 220), 1)
    cpp_lbl = font_bold.render("C++ Structure Engine:", True, text)
    screen.blit(cpp_lbl, (window + 15, 230))
    
    if engine_stats:
        total_nodes = engine_stats.get("totalBuildings", 0)
        happiest_b = engine_stats.get("happiestBuilding", {})
        h_name = happiest_b.get("name", "N/A")
        h_score = happiest_b.get("happiness", 0)
        
        lbl_nodes = font_small.render(f"Linked List Size: {total_nodes}", True, text)
        lbl_tree = font_small.render(f"BST Max Element: {h_name}", True, text)
        lbl_val = font_small.render(f"-> Happiness Score: {h_score} pts", True, (120, 240, 120))
        
        screen.blit(lbl_nodes, (window + 15, 255))
        screen.blit(lbl_tree, (window + 15, 275))
        screen.blit(lbl_val, (window + 15, 293))
    else:
        lbl_empty = font_small.render("No synchronized metrics tracked.", True, textmuted)
        screen.blit(lbl_empty, (window + 15, 255))
        
    pygame.draw.rect(screen, blue_btn, sync_btn_rect, border_radius=4)
    lbl_s = font_bold.render("SYNC WITH C++", True, text)
    screen.blit(lbl_s, lbl_s.get_rect(center=sync_btn_rect.center))

def compile_map_payload():
    """
    Compiles building configurations along with the live 8x8 structural city 
    grid matrix to send to the C++ backend.
    """
    grid_layout = []
    for r in range(rows):
        row_data = []
        for c in range(cols):
            cell = grid_data[r][c]
            # Write the building's name if a spot is taken, otherwise write "empty"
            row_data.append(cell["name"] if cell else "empty")
        grid_layout.append(row_data)

    # Combine everything into a unified JSON structure
    payload = {
        "building_options": building_options,
        "grid_layout": grid_layout
    }
    return payload

#game loop
def gameLoop():
    global screen, clock, grid_data, engine_stats
    pygame.init()

    screen = pygame.display.set_mode((window, window))
    pygame.display.set_caption("City Builder")
    clock = pygame.time.Clock()

    while True:
        screen.fill(grass)
        drawGrid()
        drawHUD()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                
                # Screen event filter targeting grid space matrix coordinate selections
                if mx < window:
                    c = mx // blockSize
                    r = my // blockSize
                    
                    if grid_data[r][c] is None:
                        grid_data[r][c] = building_options[0]
                    else:
                        idx = building_options.index(grid_data[r][c])
                        if idx + 1 < len(building_options):
                            grid_data[r][c] = building_options[idx + 1]
                        else:
                            grid_data[r][c] = None
                            
                # Screen event filter targeting backtracking layout matrix triggers
                elif backtrack_btn_rect.collidepoint(event.pos):
                    # 1. Get the 2D matrix of strings/"empty" from backtracking algorithm
                    string_layout = backtracking_algorithm(building_options, rows, cols)
                    
                    if string_layout:
                        # 2. Map the strings back to the building option dictionaries for Pygame
                        new_grid = [[None for _ in range(cols)] for _ in range(rows)]
                        for r in range(rows):
                            for c in range(cols):
                                name = string_layout[r][c]
                                if name != "empty":
                                    match = next((b for b in building_options if b["name"] == name), None)
                                    new_grid[r][c] = match
                                else:
                                    new_grid[r][c] = None
                                    
                        grid_data = new_grid
                        
                # Screen event filter targeting backend cross-language data stream sync sync ops
                elif sync_btn_rect.collidepoint(event.pos):
                    building_payload = compile_map_payload()
                    bridge.write_input(building_payload)
                    
                    if bridge.run_engine():
                        engine_stats = bridge.read_state()
                        
        pygame.display.update()
        clock.tick(30)

gameLoop()