import numpy as np
from numpy.random import default_rng
from settings import *
import matplotlib.pyplot as plt


class Population(object):
    def __init__(self, x, y, food=0, sense=SENSE_VALUE):
        self.x = x
        self.y = y
        self.food = food
        self.sense = sense
        self.has_moved = 0

    def search_food(self, food_map):
        for i in range(self.x - self.sense, self.x + self.sense + 1):
            for j in range(self.y - self.sense, self.y + self.sense + 1):
                if 0 < i < WIDTH and 0 < j < HEIGHT:
                    if food_map[i, j] == 1:
                        return [i, j]
        return [-1, -1]


class Map(object):
    def __init__(self):
        self.food_map = self.create_food_map()
        self.pop_map = self.create_pop_map()

    def create_food_map(self):
        X_food = np.random.randint(0, WIDTH, FOOD_QUANTITY)
        Y_food = np.random.randint(0, HEIGHT, FOOD_QUANTITY)
        food_map = np.zeros([WIDTH, HEIGHT])
        food_map[X_food, Y_food] = FOOD_VALUE
        return food_map

    def create_pop_map(self):
        rng = default_rng()
        pop_map = np.ndarray([WIDTH, HEIGHT], dtype=object)
        # create random pos
        P = []
        for i in range(POP_SIZE):
            x = np.random.randint(0, WIDTH)
            y = np.random.randint(0, HEIGHT)
            #print("debug2")
            while [x, y] in P:
                x = np.random.randint(0, WIDTH)
                y = np.random.randint(0, HEIGHT)
            P.append([x, y])
        P = np.array(P)
        for i in range(POP_SIZE):
            pop_map[P[i, 0], P[i, 1]] = Population(P[i, 0], P[i, 1])
        return pop_map

    def find_empty_cell(self, x, y):
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if 0 < i < WIDTH and 0 < j < HEIGHT and map.pop_map[i, j] is None:
                    return [i, j]

def next_turn(map, last_turn = False):
    child_pos = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if map.pop_map[x, y] is not None:
                i, j = 0, 0
                current_pop = map.pop_map[x, y]
                if current_pop.has_moved == False:
                    current_pop.has_moved = True
                    direction = current_pop.search_food(map.food_map)
                    if direction != [-1, -1]:
                        i, j = direction
                    else:
                        dir_x, dir_y = np.random.randint(-1, 2, 2)
                        i, j = current_pop.x + dir_x, current_pop.y + dir_y
                        coord_good = False
                        #print("debug1")
                        count = 0
                        while coord_good == False:
                            count += 1
                            if 0 < i < WIDTH and 0 < j < HEIGHT and map.pop_map[i, j] is None:
                                coord_good = True
                            else:
                                dir_x, dir_y = np.random.randint(-1, 2, 2)
                                i, j = current_pop.x + dir_x, current_pop.y + dir_y
                            if count == 9:
                                coord_good = True
                                i, j = current_pop.x, current_pop.y

                    if map.food_map[i, j] == FOOD_VALUE:
                        map.food_map[i, j] = 0
                        current_pop.food += 1

                    if last_turn:
                        food = current_pop.food
                        #print("food: ", current_pop.food)
                        if food >= 2:
                            #print("debug2", i, j)
                            child_pos.append([i, j])
                        if food >= 1:
                            #print("debug1", i, j)
                            current_pop.food = 0
                            current_pop.x, current_pop.y = i, j
                        elif food == 0:
                            #print("debug0", food, food==0, i, j)
                            current_pop = None
                            #print(i, j )
                        map.pop_map[x, y] = None
                        #print("ij", i, j, "xy", x, y, current_pop, map.pop_map[i, j])
                        map.pop_map[i, j] = current_pop
                        #print(map.pop_map[i, j], current_pop)

                    else:
                        map.pop_map[x, y] = None
                        current_pop.x, current_pop.y = i, j
                        map.pop_map[i, j] = current_pop
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if map.pop_map[x, y] is not None:
                map.pop_map[x, y].has_moved = False
    if last_turn:
        return child_pos


def next_generation(map, food_q):
    for i in range(GENERATION-1):
        next_turn(map)
    child_pos = next_turn(map, True)
    #print(child_pos)
    #print("avants enfants")
    #print_map(map.pop_map)
    for pos in child_pos:
        #print(pos)
        parent = map.pop_map[pos[0], pos[1]]
        child_x, child_y = map.find_empty_cell(pos[0], pos[1])
        child = Population(child_x, child_y, food=0, sense=parent.sense)
        map.pop_map[child_x, child_y] = child
    #print("Après enfants")
    #print_map(map.pop_map)
    #renew food
    X_food = np.random.randint(0, WIDTH, food_q)
    Y_food = np.random.randint(0, HEIGHT, food_q)
    food_map = np.zeros([WIDTH, HEIGHT])
    food_map[X_food, Y_food] = FOOD_VALUE
    map.food_map[:] = food_map[:]

def print_map(map):
    X = []
    Y = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if map[x, y] is not None:
                X.append(x)
                Y.append(y)
    print("Population: ", len(X))
    plt.plot(X, Y, "o", label="ligne -")
    plt.xlim(-1, WIDTH + 1)
    plt.ylim(-1, HEIGHT + 1)
    plt.grid(linestyle='-', linewidth=1)
    plt.show()


def count_food(map):
    food_map = map.food_map
    s = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            s+= food_map[x, y]
    return s


def count_pop(map):
    s = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if map.pop_map[x, y] != None:
                s+= 1
    return s



def train(map, epochs):
    P = []
    E = [i for i in range(epochs)]
    food_q = FOOD_QUANTITY
    for e in range(epochs):
        P.append(count_pop(map))
        next_generation(map, food_q)
        #if food_q >= 5:
            #food_q -= 1
    print(E, P)
    plt.plot(E, P)
    plt.show()
    plt.grid(linestyle='-', linewidth=1)




if __name__ == '__main__':
    map = Map()
    print_map(map.pop_map)

