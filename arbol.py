class DecisionNode:
    def __init__(self, feature=None, threshold=None, children=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.children = children if children is not None else []
        self.value = value

def build_tree():
    # Nivel 6 (hojas)
    leaf1 = DecisionNode(value=1)
    leaf2 = DecisionNode(value=2)
    leaf3 = DecisionNode(value=3)
    leaf4 = DecisionNode(value=4)
    leaf5 = DecisionNode(value=5)
    leaf6 = DecisionNode(value=6)
    leaf7 = DecisionNode(value=7)
    leaf8 = DecisionNode(value=8)
    leaf9 = DecisionNode(value=9)
    leaf10 = DecisionNode(value=10)
    leaf11 = DecisionNode(value=11)
    leaf12 = DecisionNode(value=12)
    leaf13 = DecisionNode(value=13)
    leaf14 = DecisionNode(value=14)
    leaf15 = DecisionNode(value=15)
    leaf16 = DecisionNode(value=16)

    # Nivel 5
    node5_1 = DecisionNode(feature=0, threshold=5.0, children=[leaf1, leaf2])
    node5_2 = DecisionNode(feature=1, threshold=3.0, children=[leaf3, leaf4])
    node5_3 = DecisionNode(feature=2, threshold=4.0, children=[leaf5, leaf6])
    node5_4 = DecisionNode(feature=3, threshold=2.0, children=[leaf7, leaf8])
    node5_5 = DecisionNode(feature=4, threshold=6.0, children=[leaf9, leaf10])
    node5_6 = DecisionNode(feature=5, threshold=1.0, children=[leaf11, leaf12])
    node5_7 = DecisionNode(feature=6, threshold=7.0, children=[leaf13, leaf14])
    node5_8 = DecisionNode(feature=7, threshold=8.0, children=[leaf15, leaf16])

    # Nivel 4
    node4_1 = DecisionNode(feature=0, threshold=5.0, children=[node5_1, node5_2])
    node4_2 = DecisionNode(feature=1, threshold=3.0, children=[node5_3, node5_4])
    node4_3 = DecisionNode(feature=2, threshold=4.0, children=[node5_5, node5_6])
    node4_4 = DecisionNode(feature=3, threshold=2.0, children=[node5_7, node5_8])

    # Nivel 3
    node3_1 = DecisionNode(feature=0, threshold=5.0, children=[node4_1, node4_2])
    node3_2 = DecisionNode(feature=1, threshold=3.0, children=[node4_3, node4_4])

    # Nivel 2
    node2_1 = DecisionNode(feature=0, threshold=5.0, children=[node3_1, node3_2])

    # Nivel 1 (raíz)
    root = DecisionNode(feature=0, threshold=4.0, children=[node2_1])
    
    return root

def print_tree(node, depth=0):
    if node.value is not None:
        print(f"{'|   ' * depth}Leaf: {node.value}")
    else:
        print(f"{'|   ' * depth}Feature {node.feature} <= {node.threshold}")
        for child in node.children:
            print_tree(child, depth + 1)

def minimax(node, depth, is_maximizing_player):
    if node.value is not None:
        return node.value
    
    if is_maximizing_player:
        best_value = float('-inf')
        for child in node.children:
            best_value = max(best_value, minimax(child, depth + 1, False))
        return best_value
    else:
        best_value = float('inf')
        for child in node.children:
            best_value = min(best_value, minimax(child, depth + 1, True))
        return best_value

# Construir y mostrar el árbol de decisiones
tree = build_tree()
print_tree(tree)

# Aplicar Minimax al árbol de decisiones
best_value = minimax(tree, 0, True)
print(f"El mejor valor calculado por Minimax es: {best_value}")