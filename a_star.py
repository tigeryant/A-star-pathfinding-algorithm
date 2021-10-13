import pygame
import time

HEIGHT= 600 
WIDTH = 600 
ROWS = 50 
COLS = 50 
DELAY_TIME = float("0.001")
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding - A star algorithm")

WHITE = (255, 255, 255)
TURQUOISE = (64, 224, 208)
GREY = (128, 128, 128)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165 ,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Node:
    height = HEIGHT // ROWS
    width = WIDTH // COLS

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = None
        self.parent = None
        self.g = None
        self.h = None
        self.f = None
        self.is_barrier = False

        if self.x == 0 or self.x == (COLS - 1):
            self.make_barrier()
        elif self.y == 0 or self.y == (ROWS - 1):
            self.make_barrier()
        else:
            self.colour = WHITE

    def __repr__(self):
        return f"x:{self.x}y:{self.y}"

    def make_start(self):
        self.colour = TURQUOISE
    
    def make_end(self):
        self.colour = ORANGE

    def make_barrier(self):
        self.colour = BLACK
        self.is_barrier = True 

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x * self.width, self.y * self.height, self.height, self.width))

def distance_between(node_a, node_b):
    x_distance = abs(node_a.x - node_b.x)
    y_distance = abs(node_a.y - node_b.y)
    distance = x_distance + y_distance
    return distance

def mouse_to_grid(x, y):
    node_height = WIDTH // ROWS
    node_width = WIDTH // COLS
    column = (y - 1) // node_height
    row = (x - 1) // node_width
    return row, column

def draw_window():
    WIN.fill(WHITE)
    draw_grid()
    draw_gridlines()
    pygame.display.update()

def draw_grid():
    for row in grid:
        for node in row:
            node.draw(WIN)

def make_grid():
    grid = []
    for i in range(ROWS):
        grid.append([])
        for j in range(COLS):
            node = Node(i, j)
            grid[i].append(node)
    return grid

def draw_gridlines():
    for i in range(ROWS):
       pygame.draw.line(WIN, GREY, (0, (i * Node.height)), (WIDTH, (i * Node.height)))
    
    for i in range(COLS):
       pygame.draw.line(WIN, GREY, ((i * Node.width), 0), ((i * Node.width), HEIGHT))

def assign_node_type(mouse_x, mouse_y, type):
    grid_pos = mouse_to_grid(mouse_x, mouse_y)
    node = grid[grid_pos[0]][grid_pos[1]]

    if node.x == 0 or node.x == (COLS - 1) or node.y == 0 or node.y == (ROWS - 1):
        pass

    elif type == "start":
        global start 
        start = node
        node.make_start()

    elif type == "end":
        global end
        end = node
        node.make_end()

    elif type == "barrier":
        if node != start and node != end:
            node.make_barrier()

        pass

def get_neighbours(node):
    neighbours = []
    i = node.x
    j = node.y

    neighbours.append(grid[i][j-1]) #above
    neighbours.append(grid[i][j+1]) #below
    neighbours.append(grid[i-1][j]) #left
    neighbours.append(grid[i+1][j]) #right
    return neighbours

def colour_list(list):
    if list == open:
        colour = GREEN
    elif list == closed:
        colour = RED
    elif list == path:
        colour = PURPLE

    for node in list:
        if node == start or node == end:
            continue

        node.colour = colour

def construct_path():
    global path
    path = []

    pathnode = end
    while pathnode.parent != None:
        path.append(pathnode)
        pathnode = pathnode.parent
        colour_list(path)
        time.sleep(0.04)
        draw_window()

def algorithm(): 
    global open
    global closed
    open = []
    closed = []
    finished = False

    start.g = 0
    start.f = 0
    open.append(start)

    while finished == False:
        
        def node_sort(node):
            return node.f

        open = sorted(open, key = node_sort)
        current = open[0]

        closed.append(current)
        colour_list(closed)
        time.sleep(DELAY_TIME)
        draw_window()

        del open[0]
        colour_list(open)
        time.sleep(DELAY_TIME)
        draw_window()

        if current == end:
            construct_path()
            finished = True
            break
    
        neighbours = get_neighbours(current)

        def is_in_closed(neighbour):
            for closed_node in closed:
                if closed_node == neighbour:
                    return True
            return False

        for neighbour in neighbours:

            is_in_closed(neighbour)
            if neighbour.is_barrier == True or is_in_closed(neighbour) == True:
                continue

            def is_in_open(neighbour):
                for open_node in open:
                    if open_node == neighbour:
                        return True
                return False

            is_in_open(neighbour)

            if is_in_open(neighbour) == False:
                open.append(neighbour)
                colour_list(open)
                time.sleep(DELAY_TIME)
                draw_window()
                neighbour.parent = current

            neighbour.g = current.g + 1
            neighbour.h = distance_between(neighbour, end)
            neighbour.f = neighbour.g + neighbour.h

            if is_in_open(neighbour) == True:
                if (current.g + 1) < neighbour.g:
                    neighbour.g = (current.g + 1)
                    neighbour.parent = current
                    neighbour.f = neighbour.g + neighbour.h

                    def node_sort(node):
                        return node.f

                    open = sorted(open, key = node_sort)

        if current != end and len(open) == 0: 
            print ("Failed to find path")
            finished = True

def main():
    global grid
    grid = make_grid()

    global start
    global end
    start = None
    end = None

    run = True
    pathfinding = False
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0] and pathfinding == False:
                mouse_pos = pygame.mouse.get_pos()

                if start == None and end == None:
                    assign_node_type(mouse_pos[0], mouse_pos[1], "start")

                elif start != None and end == None:
                    assign_node_type(mouse_pos[0], mouse_pos[1], "end")

                elif start and end:
                    assign_node_type(mouse_pos[0], mouse_pos[1], "barrier")
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    pathfinding = True
                    algorithm()

        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()