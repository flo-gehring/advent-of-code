"""Explanation to the Solution

For each tile in the maze (except walls) there are 8 verices in the Graph.
 -> North IN / North OUT, East IN / East OUT etc
 This allows the construction of edges, that model the cost and possibilities of turning more effectively than if there would only be 
 four vertices (North, South, East, Wert) and we can turn the Graph into a directed one.
 This allows the algorithms to run much faster than on an undirected Graph with fewer Nodes / Edges but the possibility to do "round trips"
 in a single tile on the map. 

Also, there seems to be a bug in the Implementation of find_all_shortest_paths of the igraph library.
"""

from dataclasses import dataclass
from enum import Flag, auto
import igraph as ig
import networkx as nx
path = "2024/16/input.txt"

class Direction(Flag):
    NORTH = auto()
    EAST = auto()
    SOUTH =auto()
    WEST = auto()

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

ALL_DIRECTIONS = Direction.NORTH |Direction.EAST |Direction.WEST |Direction.SOUTH

@dataclass
class Vertex:
    y: int
    x: int
    dir: Direction
    flow: str

    def __str__(self):
        return f"{self.y}_{self.x}_{self.dir.name if self.dir != None else "None"}_{self.flow}"

def add_vec(lhs: tuple[int,int], rhs:tuple[int,int]) -> tuple[int,int]:
    return (lhs[0] + rhs[0], lhs[1] + rhs[1])

def scalar_mult(v: tuple[int,int], s:int) -> tuple[int,int]:
    return (int(v[0] * s), (v[1] * s))

def is_in_input(input: list[list[str]], p: tuple[int,int]) -> bool:
    len_y = len(input)
    (y,x) = p
    return len_y > y  and y >= 0 and len(input[y]) > x and x >= 0

def get_from(input: list[list[str]], p: tuple[int,int]) -> str:
    return input[p[0]][p[1]]

def create_inner_maze_from_path(p):
    lines = open(p).readlines()
    inner_maze = [l.strip()[1:len(l.strip()) -1] for l in lines[1:len(lines)-1]]
    return [[char for char in line ] for line in inner_maze]


def create_edge_directed(source: Vertex, target: Vertex, weight: int) -> dict:
    return {
                    "source": 
                    str(source),
                      "target": str(target), 
                      "weight": weight,
                      }


def create_graph_from_input(inner_maze) -> tuple[ig.Graph, ig.Vertex]:
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
            for direction in ALL_DIRECTIONS:
                edges.extend([create_edge_directed(
                                        Vertex(y,x, direction, "in"),
                                        Vertex(y,x, other_dir, "out"), 
                                        0 if direction.get_opposite() == other_dir else 1000
                                    ) 
                                    for other_dir in ~direction
                ])
                vertex_out = Vertex(y,x, direction, "out")
                vertex_in = Vertex(y,x, direction, "in")
                vertices.append({"name": str(vertex_in), "vertex": vertex_in})
                vertices.append({"name": str(vertex_out), "vertex": vertex_out})
                next_pos = add_vec((y,x), direction.get_offset())
                if is_in_input(inner_maze, next_pos) and get_from(inner_maze, next_pos) != "#":
                    edges.append(
                        create_edge_directed(vertex_out, Vertex(next_pos[0], next_pos[1], direction.get_opposite(), "in"), 1)
                    )
    end = find(inner_maze, "E")
    inner_end_vertex = Vertex(end[0], end[1], None, "INNER")
    edges.extend([
        create_edge_directed(Vertex(end[0], end[1],direction, "in"), inner_end_vertex, 0)
        for direction in list(Direction)
        ]) 
    vertices.append({"name": str(inner_end_vertex), "vertex": inner_end_vertex})
    return (ig.Graph.DictList(vertices, edges, directed=True), inner_end_vertex)

def find(input: list[list[str]], to_search: str) -> tuple[int,int]:
    for (y, row) in enumerate(input):
        for (x, cell) in enumerate(row):
            if cell == to_search:
                return (y,x)

m = create_inner_maze_from_path(path)
(graph, end_vertex) = create_graph_from_input(m)
start = find(m, "S")
start_vertex = str(Vertex(start[0], start[1], Direction.WEST, "in"))

def get_node_with_name(graph: nx.Graph, name: str) -> int:
    for (node, nodedata) in graph.nodes.items():
        if nodedata["name"] == name:
            return node
    raise Exception("Not Found")

want_solution_1 = True
if want_solution_1:
    dist_solution1 = graph.distances(start_vertex, str(end_vertex), weights="weight")
    # Solution was 103512
    print("Solution 1", min(*dist_solution1))

def print_map(input: list[list[str]], visited: list[tuple[int,int]]):
    result = ""
    for (y, row) in enumerate(input):
        result += "#"
        for (x, cell) in enumerate(row):
            if (y,x) in visited:
                result += "O"
            else:
                result += cell
        result += "#\n"
    return result

want_solution_2 = True
if want_solution_2:
    print("Starting Solution 2")
    networkx_graph = graph.to_networkx()
    solution2_igraph = graph.get_all_shortest_paths(start_vertex, str(end_vertex), weights="weight")
    solution2 = nx.all_shortest_paths(
        networkx_graph,
          get_node_with_name(networkx_graph, str(start_vertex)), 
          get_node_with_name(networkx_graph, str(end_vertex)),
            weight="weight")
    list_solution = list(solution2)
    visited_nodes = set()
    
    # Get all visited Vertices and collapse the ones belonging to the same tile
    for path in list_solution:
        visited_nodes = visited_nodes.union(set(path))
    vertex_objects = graph.vs.select(lambda x: x.index in visited_nodes)["vertex"]
    visted = set([(s.y, s.x) for s in vertex_objects])
    
    # Get all visited Vertices and collapse the ones belonging to the same tile
    visited_nodes_ig = set()
    for path in solution2_igraph:
        visited_nodes_ig = visited_nodes_ig.union(set(path))
    vertex_objects_ig = graph.vs.select(lambda x: x.index in visited_nodes_ig)["vertex"]
    visted_ig = set([(s.y, s.x) for s in vertex_objects_ig])
    print("Solution 2 (NetworkX)", len(list(visted)))
    print("Solution 2 (igraph)", len(list(visted_ig)))
    print(f"There's a bug in igraph as {len(list(visted))} != { len(list(visted_ig))} and the first one is correct ")


demonstrate_ig_error = True
maze_small = create_inner_maze_from_path("2024/16/input_test_smol.txt")
(graph_small, end_vertex_small) = create_graph_from_input(maze_small)
start_small = find(maze_small, "S")
start_vertex_small = str(Vertex(start_small[0], start_small[1], Direction.SOUTH, "in"))

if demonstrate_ig_error:
    print("Demonstrating igraph bug")
    print("Initial Maze")
    print(print_map(maze_small, set()))
    networkx_graph = graph_small.to_networkx()
    solution2_igraph = graph_small.get_all_shortest_paths(start_vertex_small, str(end_vertex_small), weights="weight")
    solution2 = nx.all_shortest_paths(
        networkx_graph,
          get_node_with_name(networkx_graph, str(start_vertex_small)), 
          get_node_with_name(networkx_graph, str(end_vertex_small)),
            weight="weight")
    list_solution = list(solution2)
    visited_nodes = set()
    # Get all visited Vertices and collapse the ones belonging to the same tile
    for path in list_solution:
        visited_nodes = visited_nodes.union(set(path))
    vertex_objects = graph_small.vs.select(lambda x: x.index in visited_nodes)["vertex"]
    visted = set([(s.y, s.x) for s in vertex_objects])
    print("Network x Solution")
    print(print_map(maze_small, visted))
    # Get all visited Vertices and collapse the ones belonging to the same tile
    visited_nodes_ig = set()
    for path in solution2_igraph:
        visited_nodes_ig = visited_nodes_ig.union(set(path))
    vertex_objects_ig = graph_small.vs.select(lambda x: x.index in visited_nodes_ig)["vertex"]
    visted_ig = set([(s.y, s.x) for s in vertex_objects_ig])
  
    print("igraph Solution (Wrong)")
    print(print_map(maze_small, visted_ig))
    print("Solution  (NetworkX)", len(list(visted)))
    print("Solution (igraph)", len(list(visted_ig)))
    print(f"There's a bug in igraph as {len(list(visted))} != { len(list(visted_ig))} and the first one is correct ")