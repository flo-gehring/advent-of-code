path = "2024/12/input_test.txt"
input = [[c for c in line.strip()] for line in open(path).readlines()]
types_of_plants = set([c for c in open(path).read().strip() if c != "\n"])



def add_tuples(lhs: tuple[int,int], rhs: tuple[int,int]) -> tuple[int,int]:
    return (lhs[0] + rhs[0], lhs[1]+ rhs[1])


class Region:
    def __init__(self, plant):
        self.coordinates = set()
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

def in_input(input, tuple):
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

cost_per_plant = dict()
all_regions: list[Region] = []
for type_of_plant in types_of_plants:
    regions: list[Region] = []
    region_map = dict()
    for (y, row) in enumerate(input):
        for (x, cell) in enumerate(row):
            current_coord = (y,x)
            if cell == type_of_plant:
                region = None
                down = add_tuples(current_coord, (1,0))
                right = add_tuples(current_coord, (0,1))
                up = add_tuples(current_coord, (-1,0))
                left = add_tuples(current_coord, (0,-1))
                if current_coord in region_map:
                    region = region_map[current_coord]
                elif in_input(input, down) and get_from(input, down) == type_of_plant and \
                    down in region_map:
                    region = region_map[down]
                    region_map[current_coord] = region
                    region.add(current_coord)
                elif in_input(input, right) and get_from(input, right) == type_of_plant and \
                    right in region_map:
                    region = region_map[right]
                    region_map[current_coord] = region
                    region.add(current_coord)
                elif in_input(input, left) and get_from(input, left) == type_of_plant and \
                    left in region_map:
                    region = region_map[left]
                    region_map[current_coord] = region
                    region.add(current_coord)
                elif  in_input(input, up) and get_from(input, up) == type_of_plant and \
                    up in region_map:
                    region = region_map[up]
                    region_map[current_coord] = region
                    region.add(current_coord)
                else:
                    region = Region(type_of_plant)
                    region_map[current_coord] = region
                    region.add(current_coord)
                    regions.append(region)
                if in_input(input, down) and get_from(input, down) == type_of_plant and not down in region_map :
                    region_map[down] = region
                    region.add(down)
                if in_input(input, right) and get_from(input, right) == type_of_plant and not right in region_map:
                    region_map[right] = region
                    region.add(right)
                if in_input(input, up) and get_from(input, up) == type_of_plant and not up in region_map:
                    region_map[up] = region
                    region.add(up)
                if in_input(input, left) and get_from(input, left) == type_of_plant and not left in region_map:
                    region_map[left] = region
                    region.add(left)

    if type_of_plant == "F":
            for r in regions:
                print("Region", str(r), "len", len(r.coordinates), r.calculate_price(input))
            print(print_regions(input, regions))
    all_regions.extend(regions)
    cost_per_plant[type_of_plant] = sum([r.calculate_price(input) for r in regions])
    
print(cost_per_plant)
print(sum(cost_per_plant.values())) 
for r in all_regions:
    print(r.plant, r.calculate_price(input))


    