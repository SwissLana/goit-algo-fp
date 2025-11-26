import uuid
from collections import deque

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="#1296F0"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())

# Рекурсивна функція для додавання ребер до графа 
def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

# Візуалізація бінарного дерева 
def draw_tree(tree_root, title="Дерево"):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    fig, ax = plt.subplots(figsize=(8, 5.5))
    try:
        fig.canvas.manager.set_window_title(title)
    except Exception:
        pass
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(ymin, ymax)  
    plt.show()


def collect_nodes(root):
    """Збирає всі вузли дерева в список (BFS), щоб мати їх для скидання кольорів."""
    nodes = []
    if root is None:
        return nodes
    queue = deque([root])
    while queue:
        node = queue.popleft()
        nodes.append(node)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return nodes


def generate_color_gradient(n, start_color="#08306B", end_color="#C6DBEF"):
    """
    Генерує n кольорів від темного до світлого (HEX).
    start_color, end_color – рядки типу '#RRGGBB'.
    """
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb):
        return "#{:02X}{:02X}{:02X}".format(*rgb)

    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)

    colors = []
    for i in range(n):
        t = i / max(1, n - 1)
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
        colors.append(rgb_to_hex((r, g, b)))
    return colors



def dfs_order(root):
    """Обхід у глибину (DFS) зі стеком. Повертає список вузлів у порядку відвідування."""
    if root is None:
        return []

    order = []
    stack = [root]

    while stack:
        node = stack.pop()
        order.append(node)
        # Спочатку додаємо правого, потім лівого, щоб лівий опрацювався першим
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return order


def bfs_order(root):
    """Обхід у ширину (BFS) з чергою. Повертає список вузлів у порядку відвідування."""
    if root is None:
        return []

    order = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return order


def color_by_order(root, order, title):
    """Присвоює кольори вузлам згідно з порядком обходу й малює дерево."""
    all_nodes = collect_nodes(root)
    # Скидаємо кольори
    for node in all_nodes:
        node.color = "#CCCCCC"

    colors = generate_color_gradient(len(order))

    for idx, node in enumerate(order):
        node.color = colors[idx]

    draw_tree(root, title=title)


if __name__ == "__main__":
    # Створюємо приклад дерева для демонстрації обходів (DFS і BFS) 
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.left = Node(6)
    root.right.right = Node(7)

    # DFS
    dfs_nodes = dfs_order(root)
    color_by_order(root, dfs_nodes, title="Обхід у глибину (DFS)")

    # BFS
    bfs_nodes = bfs_order(root)
    color_by_order(root, bfs_nodes, title="Обхід у ширину (BFS)")