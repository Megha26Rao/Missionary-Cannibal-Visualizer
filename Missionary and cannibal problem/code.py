import pygame
import os
from collections import deque

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 600  # Adjusted screen size to 5x6 inches
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load and Resize Images
def load_and_resize(image_path, size=(80, 80)):  # Set images to 80x80 pixels
    if os.path.exists(image_path):
        img = pygame.image.load(image_path)
        img = pygame.transform.scale(img, size)  # Resize image
        return img
    else:
        print(f"Error: {image_path} not found!")
        return None

missionary_img = load_and_resize("images/missionary.png")
cannibal_img = load_and_resize("images/cannibal.png")
boat_img = load_and_resize("images/boat.png", (100, 60))  # Boat slightly wider

# Pygame Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Missionary and Cannibal Problem")

# Game Variables
M, C = 3, 3  # Total missionaries and cannibals
start = (M, C, 1)  # Initial state: all on the left bank
goal = (0, 0, 0)  # Goal state: all safely on the right bank
visited = set()

# Possible moves
MOVES = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

def is_valid(state):
    m_left, c_left, boat = state
    m_right, c_right = M - m_left, C - c_left
    
    # Check for out-of-bounds values
    if not (0 <= m_left <= M and 0 <= c_left <= C):
        return False
    
    # Ensure missionaries are never outnumbered by cannibals
    if (m_left < c_left and m_left > 0) or (m_right < c_right and m_right > 0):
        return False

    return True

def bfs():
    queue = deque([(start, [])])  # (current state, path taken)
    visited.add(start)

    while queue:
        state, path = queue.popleft()

        if state == goal:
            return path  # Solution found

        m_left, c_left, boat = state
        for m, c in MOVES:
            if boat == 1:  # Boat on left side
                new_state = (m_left - m, c_left - c, 0)
            else:  # Boat on right side
                new_state = (m_left + m, c_left + c, 1)

            if new_state not in visited and is_valid(new_state):
                queue.append((new_state, path + [new_state]))
                visited.add(new_state)

    return None  # No solution found

solution = bfs()

def draw_scene(state):
    screen.fill((173, 216, 230))  # Set background to blue (water)

    m_left, c_left, boat = state
    m_right, c_right = M - m_left, C - c_left

    # Draw green land on both sides
    pygame.draw.rect(screen, (34, 139, 34), (0, HEIGHT - 300, WIDTH // 2.5, 300))  # Left land
    pygame.draw.rect(screen, (34, 139, 34), (WIDTH - WIDTH // 2.5, HEIGHT - 300, WIDTH // 2.5, 300))  # Right land

    # Draw boat
    boat_x = 50 if boat == 1 else WIDTH - 150
    screen.blit(boat_img, (boat_x, HEIGHT - 150))

    # Draw missionaries (left side)
    for i in range(m_left):
        screen.blit(missionary_img, (50, HEIGHT - (i + 2) * 80))

    # Draw cannibals (left side)
    for i in range(c_left):
        screen.blit(cannibal_img, (150, HEIGHT - (i + 2) * 80))

    # Draw missionaries (right side)
    for i in range(m_right):
        screen.blit(missionary_img, (WIDTH - 200, HEIGHT - (i + 2) * 80))

    # Draw cannibals (right side)
    for i in range(c_right):
        screen.blit(cannibal_img, (WIDTH - 100, HEIGHT - (i + 2) * 80))

    pygame.display.flip()  # Refresh screen

def main():
    if not solution:
        print("No solution found!")
        return

    running = True
    clock = pygame.time.Clock()
    state_index = 0

    while running:
        clock.tick(0.5)  # 1 FPS to slow down transitions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if state_index < len(solution):
            draw_scene(solution[state_index])
            state_index += 1

    pygame.quit()

if __name__ == "__main__":
    main()
