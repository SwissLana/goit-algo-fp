import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        # граф зберігаємо як словник: вершина -> список (сусід, вага)
        self.adj_list = {}

    def add_edge(self, u, v, weight, bidirectional=True):
        """Додає ребро u -> v з вагою weight.
        Якщо bidirectional=True, додає також v -> u.
        """
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []

        self.adj_list[u].append((v, weight))
        if bidirectional:
            self.adj_list[v].append((u, weight))

    def dijkstra(self, start):
        """Алгоритм Дейкстри для знаходження найкоротших шляхів
        від вершини start до всіх інших вершин графа.
        Використовує бінарну купу (heapq).
        """

        # Початкові відстані: безкінечність для всіх, 0 для start
        distances = {vertex: float("inf") for vertex in self.adj_list}
        distances[start] = 0

        # Для відновлення шляхів
        previous = {vertex: None for vertex in self.adj_list}

        # Пріоритетна черга: (поточна_відстань, вершина)
        heap = [(0, start)]

        while heap:
            current_distance, current_vertex = heapq.heappop(heap)

            # Якщо ми вже знайшли кращу (меншу) відстань раніше — пропускаємо
            if current_distance > distances[current_vertex]:
                continue

            # Оновлюємо відстані до сусідів
            for neighbor, weight in self.adj_list[current_vertex]:
                distance = current_distance + weight

                # Якщо знайшли кращий шлях до сусіда — оновлюємо
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(heap, (distance, neighbor))

        return distances, previous

    def get_shortest_path(self, previous, start, target):
        """Відновлення найкоротшого шляху з start до target
        на основі словника previous.
        """
        path = []
        current = target

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        # Якщо шлях не починається зі start — значить, до вершини немає шляху
        if not path or path[0] != start:
            return None

        return path


def visualize_graph(graph: Graph, shortest_path=None):
    """
    Візуалізація графа:
    - вузли: вершини
    - підписи на ребрах: ваги
    - найкоротший шлях (якщо заданий) підсвічується іншим кольором
    """
    G = nx.Graph()

    # Додаємо ребра в networkx-граф
    for u, neighbors in graph.adj_list.items():
        for v, w in neighbors:
            # networkx сам ігнорує дублікати ребер, якщо вага однакова
            G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)  # красиве розташування вершин

    plt.figure(figsize=(8, 6))

    # Ребра та ваги
    edges = G.edges()
    weights = nx.get_edge_attributes(G, "weight")

    # Якщо є найкоротший шлях — виділимо ребра на ньому
    edge_colors = []
    edge_widths = []

    path_edges = set()
    if shortest_path and len(shortest_path) > 1:
        for i in range(len(shortest_path) - 1):
            a = shortest_path[i]
            b = shortest_path[i + 1]
            # робимо неорієнтовану пару
            path_edges.add((a, b))
            path_edges.add((b, a))

    for (u, v) in edges:
        if (u, v) in path_edges:
            edge_colors.append("red")
            edge_widths.append(2.5)
        else:
            edge_colors.append("gray")
            edge_widths.append(1)

    # Малюємо вершини
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color="skyblue")
    # Малюємо ребра
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edge_colors, width=edge_widths)
    # Підписи вершин
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")
    # Підписи ваг ребер
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weights, font_size=10)

    plt.axis("off")
    plt.title("Граф та найкоротший шлях (алгоритм Дейкстри)")
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    graph = Graph()

    # Створимо невеликий зважений граф
    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 2)
    graph.add_edge("B", "C", 5)
    graph.add_edge("B", "D", 10)
    graph.add_edge("C", "E", 3)
    graph.add_edge("E", "D", 4)
    graph.add_edge("D", "F", 11)

    start_vertex = "A"
    distances, previous = graph.dijkstra(start_vertex)

    print(f"\nНайкоротші відстані від вершини {start_vertex}:")
    for vertex, distance in distances.items():
        print(f"  {start_vertex} -> {vertex}: {distance}")

    # Приклад: відновимо шлях з A до F
    target_vertex = "F"
    path = graph.get_shortest_path(previous, start_vertex, target_vertex)

    print(f"\nНайкоротший шлях від {start_vertex} до {target_vertex}:")
    if path is None:
        print("  Шляху не існує")
    else:
        print("  " + " -> ".join(path))
        
    # Візуалізація графа та найкоротшого шляху
    visualize_graph(graph, shortest_path=path)