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
from algorithms import backtracking, greedy

window = 400
hud_width = 240
total_width = window + hud_width

grass = (107, 179, 108)
street = (224, 224, 224)
hud_bg = (45, 45, 48)
text = (240, 240, 240)
textmuted = (150, 150, 150)
warning_red = (220, 60, 60)

pygame.font.init()
font_small = pygame.font.SysFont("Arial", 11)
font_medium = pygame.font.SysFont("Arial", 12, bold=True)
font_bold = pygame.font.SysFont("Arial", 13, bold=True)

TYPE_COLORS = {
    "Residential": (70, 130, 180),
    "Commercial": (218, 165, 32),
    "Industrial": (120, 120, 120)
}

rows = 8
cols = 8
blockSize = 50

grid_data = [[None for _ in range(cols)] for _ in range(rows)]
building_options = []
engine_stats = None
show_factory_warning = False

def drawGrid():
    for r in range(rows):
        for c in range(cols):
            x = c * blockSize
            y = r * blockSize
            rect = pygame.Rect(x, y, blockSize, blockSize)
            
            cell = grid_data[r][c]
            if cell:
                color = TYPE_COLORS.get(cell["type"], (255, 255, 255))
                pygame.draw.rect(screen, color, rect)
                lbl = font_small.render(f"{cell['name'][:5]} S:{cell['size']}", True, (255, 255, 255))
                screen.blit(lbl, (x + 2, y + 18))
            else:
                pygame.draw.rect(screen, grass, rect)
                
            pygame.draw.rect(screen, street, rect, 1)

def drawHUD():
    pygame.draw.rect(screen, hud_bg, (window, 0, hud_width, window))
    
    title = font_bold.render("City Builder", True, text)
    screen.blit(title, (window + 15, 15))
    pygame.draw.line(screen, street, (window + 15, 40), (window + hud_width - 15, 40), 1)
    
    hint = font_small.render("Click cells to cycle items manually.", True, textmuted)
    screen.blit(hint, (window + 15, 50))
    
    status_lbl = font_bold.render("Engine State: REACTIVE", True, (100, 255, 100))
    screen.blit(status_lbl, (window + 15, 95))
    
    hint_auto = font_small.render("Analysis triggers on every click.", True, textmuted)
    screen.blit(hint_auto, (window + 15, 115))
    
    pygame.draw.line(screen, street, (window + 15, 220), (window + hud_width - 15, 220), 1)
    cpp_lbl = font_bold.render("Real-Time C++ Analysis:", True, text)
    screen.blit(cpp_lbl, (window + 15, 230))
    
    if show_factory_warning:
        warn_lbl1 = font_small.render("WARNING: Layout contains only", True, warning_red)
        warn_lbl2 = font_small.render("factories. No happiness index.", True, warning_red)
        screen.blit(warn_lbl1, (window + 15, 255))
        screen.blit(warn_lbl2, (window + 15, 273))
    elif engine_stats:
        total_nodes = engine_stats.get("totalBuildings", 0)
        happiest_b = engine_stats.get("happiestBuilding", {})
        h_name = happiest_b.get("name", "N/A")
        h_score = happiest_b.get("happiness", 0)
        
        lbl_nodes = font_small.render(f"Graph Links Extracted: {total_nodes}", True, text)
        lbl_tree = font_small.render(f"BST Peak Element: {h_name}", True, text)
        lbl_val = font_small.render(f"-> Happiness: {h_score} pts", True, (120, 240, 120))
        
        screen.blit(lbl_nodes, (window + 15, 255))
        screen.blit(lbl_tree, (window + 15, 275))
        screen.blit(lbl_val, (window + 15, 293))
    else:
        lbl_empty = font_small.render("Awaiting city structures...", True, textmuted)
        screen.blit(lbl_empty, (window + 15, 255))

def check_only_factories():
    found_any = False
    for r in range(rows):
        for c in range(cols):
            cell = grid_data[r][c]
            if cell:
                if cell["type"] != "Industrial":
                    return False
                found_any = True
    return found_any

def run_automated_backend_sync():
    global show_factory_warning, engine_stats
    if check_only_factories():
        show_factory_warning = True
        engine_stats = None
    else:
        show_factory_warning = False
        
        flat_names = []
        flat_types = []
        for r in range(rows):
            for c in range(cols):
                flat_names.append(grid_data[r][c]["name"] if grid_data[r][c] else "empty")
                flat_types.append(grid_data[r][c]["type"] if grid_data[r][c] else "empty")
        
        payload = {
            "buildings": building_options,
            "grid_layout": flat_names,
            "grid_types": flat_types
        }
        
        import json
        with open(os.path.join(bridge.url, 'input.json'), 'w') as f:
            json.dump(payload, f, indent=2)
        
        # Absolute Hardware Path Configurations
        base_dir = os.path.dirname(os.path.abspath(__file__))
        engine_dir = os.path.normpath(os.path.join(base_dir, "../../engine"))
        data_dir = os.path.normpath(os.path.join(base_dir, "../../data"))
        
        cpp_file = os.path.join(engine_dir, "main.cpp")
        exe_file = os.path.join(engine_dir, "engine.exe")
        input_json = os.path.join(data_dir, "input.json")
        state_json = os.path.join(data_dir, "state.json")

        import shutil, subprocess
        if not os.path.exists(exe_file):
            gxx_compiler = "g++"
            if shutil.which(gxx_compiler):
                try:
                    subprocess.run([gxx_compiler, "-std=c++11", cpp_file, "-o", exe_file], check=True)
                except Exception as e:
                    print(f"Compilation failed: {e}")
            else:
                print("Note: 'g++' not found. Ensure 'engine.exe' is pre-compiled.")

        if os.path.exists(exe_file):
            try:
                # Use normalized paths for Windows compatibility
                subprocess.run([os.path.normpath(exe_file), os.path.normpath(input_json), os.path.normpath(state_json)], check=True)
            except Exception as e:
                print(f"Backend Execution Error: {e}")
        else:
            print(f"Sync Aborted! Engine executable missing at: {exe_file}")
        
        try:
            engine_stats = bridge.load_states()
        except Exception:
            engine_stats = None

def gameLoop():
    global screen, clock, grid_data, engine_stats, show_factory_warning, building_options
    pygame.init()

    try:
        building_options = bridge.load_buildings()
    except Exception:
        building_options = []
        
    if not building_options:
        building_options = [
            {"name": "House", "type": "Residential", "size": 1, "happiness": 50},
            {"name": "School", "type": "Commercial", "size": 2, "happiness": 75},
            {"name": "Park", "type": "Commercial", "size": 3, "happiness": 90},
            {"name": "Hospital", "type": "Commercial", "size": 4, "happiness": 85},
            {"name": "Factory", "type": "Industrial", "size": 3, "happiness": -40},
            {"name": "Landfill", "type": "Industrial", "size": 2, "happiness": -60}
        ]

    screen = pygame.display.set_mode((total_width, window))
    pygame.display.set_caption("City Builder Engine - Variant 4 (Automated)")
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
                
                if mx < window:
                    c = mx // blockSize
                    r = my // blockSize
                    
                    total_options = len(building_options)
                    
                    if grid_data[r][c] is None:
                        grid_data[r][c] = building_options[0].copy()
                        grid_data[r][c]["option_idx"] = 0
                    else:
                        next_idx = (grid_data[r][c].get("option_idx", 0) + 1) % (total_options + 1)
                        if next_idx == total_options:
                            grid_data[r][c] = None
                        else:
                            grid_data[r][c] = building_options[next_idx].copy()
                            grid_data[r][c]["option_idx"] = next_idx
                    
                    try:
                        run_automated_backend_sync()
                    except Exception as e:
                        print(f"Sync issue managed: {e}")
                            
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    gameLoop()