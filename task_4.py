import uuid 
import heapq
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор для кожного вузла

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
def draw_tree(tree_root):  
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()


def build_heap_tree(heap_list):
    """
    Створює бінарне дерево (Node), використовуючи масив купи.
    heap_list - список, що представляє бінарну купу.
    """
    if not heap_list:
        return None

    # Створюємо список вузлів
    nodes = [Node(key) for key in heap_list]

    # Прив'язуємо лівих і правих дітей за індексами
    for i in range(len(nodes)):
        left_index = 2 * i + 1
        right_index = 2 * i + 2

        if left_index < len(nodes):
            nodes[i].left = nodes[left_index]
        if right_index < len(nodes):
            nodes[i].right = nodes[right_index]

    return nodes[0]  # корінь дерева


def draw_heap(heap_list):
    """
    Візуалізує бінарну купу у вигляді дерева.
    """
    if not heap_list:
        print("Купа порожня")
        return

    root = build_heap_tree(heap_list)
    draw_tree(root)


if __name__ == "__main__":
    # Приклад: створимо мін-купу з довільного масиву
    data = [10, 4, 15, 20, 0, 3, 5]
    heapq.heapify(data)  # перетворюємо список на купу

    print("\nКупа у вигляді списку:", data)
    print("Візуалізація купи у вигляді дерева\n") 
    draw_heap(data)