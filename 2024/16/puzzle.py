from dataclasses import dataclass
from enum import Enum
import igraph as ig


path = "2024/16/input.txt"

class Direction(Enum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH ="SOUTH"
    WEST = "WEST"

    def get_offset(self):
        match self:
            case Direction.NORTH:
                return (-1,0)
            case Direction.EAST:
                return (0,1)
            case Direction.SOUTH:
                return (1,0)
            case Direction.WEST:
                return (0,-1)

    def get_opposite(self):
        match self:
            case Direction.NORTH: 
                return Direction.SOUTH
            case Direction.SOUTH:
                return Direction.NORTH
            case Direction.EAST:
                return Direction.WEST
            case Direction.WEST:
                return Direction.EAST
    
 

@dataclass
class Vertex:
    y: int
    x: int
    dir: Direction

    def __str__(self):
        return f"{self.y}_{self.x}_{self.dir}"


def add_vec(lhs: tuple[int,int], rhs:tuple[int,int]) -> tuple[int,int]:
    return (lhs[0] + rhs[0], lhs[1] + rhs[1])

def scalar_mult(v: tuple[int,int], s:int) -> tuple[int,int]:
    return (int(v[0] * s), (v[1] * s))
def is_in_input(input: list[list[str]], p: tuple[int,int]) -> bool:
    len_y = len(input)
    return len_y > p[0]  and p[0] >= 0 and len(input[0]) > p[1] and len(input[0]) >= 0


def get_from(input: list[list[str]], p: tuple[int,int]) -> str:
    return input[p[0]][p[1]]


def create_inner_maze_from_path(p):
    lines = open(path).readlines()
    inner_maze = [l.strip()[1:len(l.strip()) -1] for l in lines[1:len(lines)-1]]
    return [[char for char in line ] for line in inner_maze]

def create_graph_from_input(inner_maze) -> ig.Graph:
    """
    From Documentation  
     vertices = [{'name': 'apple'}, {'name': 'pear'}, {'name': 'peach'}]
    edges = [{'source': 'apple', 'target': 'pear', 'weight': 1.2},
             {'source': 'apple', 'target': 'peach', 'weight': 0.9}]
    g = Graph.DictList(vertices, edges)
    """
    vertices = []
    edges = []
    
    for (y, row) in enumerate(inner_maze):
        for (x , tile) in enumerate(row):
            if tile == "#":
                continue
            edges.extend([
                {"source": str(Vertex(y,x, Direction.NORTH)), "target": str(Vertex(y,x, Direction.SOUTH)), "weight": 0},
                {"source": str(Vertex(y,x, Direction.WEST)), "target": str(Vertex(y,x, Direction.EAST)), "weight": 0},
                {"source": str(Vertex(y,x, Direction.NORTH)), "target": str(Vertex(y,x, Direction.EAST)), "weight": 1000},
                {"source": str(Vertex(y,x, Direction.EAST)), "target": str(Vertex(y,x, Direction.SOUTH)), "weight": 1000},
                {"source": str(Vertex(y,x, Direction.SOUTH)), "target": str(Vertex(y,x, Direction.WEST)), "weight": 1000},
                {"source": str(Vertex(y,x, Direction.WEST)), "target": str(Vertex(y,x, Direction.NORTH)), "weight": 1000}
            ])
            for direction in list(Direction):
                vertex = Vertex(y,x, direction)

                vertices.append({"name": str(vertex)})
                next_pos = add_vec((y,x), direction.get_offset())
                if is_in_input(inner_maze, next_pos) and get_from(inner_maze, next_pos) != "#":
                    edges.append(
                        {
                            "source": str(Vertex(y,x, direction)), 
                            "target": str(Vertex(next_pos[0],next_pos[1], direction.get_opposite())),
                              "weight": 1
                              }
                        )
    
    return ig.Graph.DictList(vertices, edges)





def find(input: list[list[str]], to_search: str) -> tuple[int,int]:
    for (y, row) in enumerate(input):
        for (x, cell) in enumerate(row):
            if cell == to_search:
                return (y,x)



    


m = create_inner_maze_from_path(path)
g = create_graph_from_input(m)
start = find(m, "S")
start_vertex = str(Vertex(start[0], start[1], Direction.EAST))
end = find(m, "E")
end_vertices=[str(Vertex(end[0], end[1], d)) for d in list(Direction)]
dist_solution1 = g.distances(start_vertex, end_vertices, weights="weight")
print("Solution 1", min(*dist_solution1))
