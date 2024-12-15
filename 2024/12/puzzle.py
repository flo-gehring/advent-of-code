from enum import Enum

path = "2024/12/input.txt"
input = [[c for c in line.strip()] for line in open(path).readlines()]
types_of_plants = set([c for c in open(path).read().strip() if c != "\n"])


def add_tuples(lhs: tuple[int,int], rhs: tuple[int,int]) -> tuple[int,int]:
    return (lhs[0] + rhs[0], lhs[1]+ rhs[1])

class Direction(Enum):
    UP=(-1,0)
    DOWN=(1,0)
    RIGHT=(0,1)
    LEFT=(0,-1)


class Region:
    def __init__(self, plant, coordinates):
        self.coordinates = set(coordinates)
        self.plant = plant

    def add(self, coord:tuple[int,int] ):
        self.coordinates.add(coord)

    def __str__(self):
        return ", ".join([str(t) for t in self.coordinates])
    
    def calculate_price(self, map: list[list[str]]):
        fence_segments = sum(
            [Region.count_fence_segment(map, c, self.plant) for c in self.coordinates]
        )
        return fence_segments * len(self.coordinates)
    
    def calculate_price_part2(self, map:list[list[str]]):
        fence_segments_not_done_yet = self.get_all_fence_segments( map)
        number_faces = 0
        while fence_segments_not_done_yet:
            number_faces += 1
            (segment_coord, dir) = fence_segments_not_done_yet.pop()
            walking_directions = None
            if dir == Direction.DOWN or dir == Direction.UP:
                walking_directions = [Direction.LEFT, Direction.RIGHT]
            elif dir == Direction.RIGHT or dir == Direction.LEFT:
                walking_directions = [Direction.DOWN, Direction.UP]
            else:
                raise Exception("Unerwarteter Wert" + str(dir))
            for walking_dir in walking_directions:
                next_coor = add_tuples(segment_coord, walking_dir.value)
                while in_input(input, next_coor) and get_from(input, next_coor) == self.plant and \
                    (next_coor, dir) in fence_segments_not_done_yet:
                    fence_segments_not_done_yet.remove((next_coor, dir))
                    next_coor = add_tuples(next_coor, walking_dir.value)
        return number_faces * len(self.coordinates)
        

    def get_all_fence_segments(self, map:list[list[str]]) -> list[tuple[tuple[int,int], Direction]]:
        result = []
        for coord in self.coordinates:
            for dir in [Direction.DOWN, Direction.LEFT, Direction.RIGHT, Direction.UP]:
                neighbor =add_tuples(coord, dir.value)
                if not in_input(map, neighbor ) or get_from(map, neighbor) != self.plant:
                    result.append((coord, dir))
        return result

    staticmethod 
    def count_fence_segment( map: list[list[str]], coordinate: tuple[int,int], plant: str):
        return Region.add_fence_segment(map,add_tuples(coordinate, (-1,0)), plant)  +  \
                Region.add_fence_segment(map,add_tuples(coordinate, (1,0)), plant)  +  \
                Region.add_fence_segment(map,add_tuples(coordinate, (0,1)), plant)  +  \
                Region.add_fence_segment(map,add_tuples(coordinate, (0,-1)), plant)  
    
    staticmethod
    def add_fence_segment(
            map: list[list[str]], coordinate: tuple[int,int], plant: str
    ):
        if  not in_input(map, coordinate):
            return 1
        if get_from(map, coordinate) != plant:
            return 1
        return 0
        
def get_from(input, tuple):
    return input[tuple[0]][tuple[1]]

def in_input(input: list[list[str]], tuple: tuple[int,int]):
    return tuple[0] >= 0 and tuple[0] < len(input) and tuple[1] >= 0 and tuple[1] < len(input[tuple[0]])

def print_regions(input, regions: list[Region] ) -> str:
    result = ""
    for (y, row) in enumerate(input):
        for (x, cell) in enumerate(row):
            for r in regions:
                if (y,x) in  r.coordinates:
                    result += region.plant
                    break
            else:
                result += "_"
        result += "\n"
    return result


def get_adjacent(input, coord, plant):
    directions = [(1,0),(0,1),(-1,0),(0,-1)]
    result = []
    for dir in directions:
        if in_input(input, add_tuples(coord, dir)):
            p = get_from(input, add_tuples(coord, dir))
            if p == plant:
                result.append(add_tuples(coord, dir))
    return result

def create_region(input: list[str], coord: tuple[int,int]) -> Region:
    coords_to_add = [coord]
    already_added = set()
    already_added.add(coord)
    plant = get_from(input, coord)
    while coords_to_add:
        next_coord = coords_to_add.pop()
        next_adjacent = set(get_adjacent(input, next_coord, plant))
        new_adjacents= next_adjacent - already_added
        coords_to_add.extend(new_adjacents)
        already_added = already_added.union(new_adjacents)
    return Region(plant, already_added)
        

cost_per_plant = dict()
cost_per_plant_2 = dict()

all_regions: list[Region] = []
for type_of_plant in types_of_plants:
    regions: list[Region] = []
    region_map = dict()
    for (y, row) in enumerate(input):
        for (x, cell) in enumerate(row):
            current_coord = (y,x)
            if cell == type_of_plant and current_coord not in region_map:
                region = create_region(input, current_coord)
                regions.append(region)
                for c in region.coordinates:
                    region_map[c] = region         
    all_regions.extend(regions)
    cost_per_plant[type_of_plant] = sum([r.calculate_price(input) for r in regions])
    cost_per_plant_2[type_of_plant] = sum([r.calculate_price_part2(input) for r in regions])
    

print("Solution Part 1", sum(cost_per_plant.values())) 
print("Solution Part 2", sum(cost_per_plant_2.values())) 