import random
import json
from collections import deque

class FractalNode:
    def __init__(self, node_id, level, parent=None):
        self.node_id = node_id
        self.level = level
        self.parent = parent
        self.children = []
        self.state = {}
        self.history = deque(maxlen=100)  # Temporal folding cache

    def add_child(self, child_node):
        self.children.append(child_node)

    def update_state(self, key, value):
        self.state[key] = value
        self.history.append((key, value))

    def recursive_describe(self, depth=0):
        indent = '  ' * depth
        desc = f"{indent}Node {self.node_id} (Level {self.level}): State={self.state}\n"
        for child in self.children:
            desc += child.recursive_describe(depth + 1)
        return desc

class FractalRealityEngine:
    def __init__(self, max_depth=5):
        self.root = FractalNode("root", 0)
        self.max_depth = max_depth
        self.node_count = 1
        self.build_fractal(self.root, 0)

    def build_fractal(self, current_node, depth):
        if depth >= self.max_depth:
            return
        num_children = random.randint(1, 3)
        for _ in range(num_children):
            child_id = f"node_{self.node_count}"
            child_node = FractalNode(child_id, depth + 1, parent=current_node)
            current_node.add_child(child_node)
            self.node_count += 1
            self.build_fractal(child_node, depth + 1)

    def simulate_step(self):
        nodes_to_update = [self.root]
        while nodes_to_update:
            node = nodes_to_update.pop()
            # Update node state with random value to simulate change
            key = f"param_{random.randint(1,5)}"
            value = random.random()
            node.update_state(key, value)
            nodes_to_update.extend(node.children)

    def export_state(self):
        def node_to_dict(node):
            return {
                "node_id": node.node_id,
                "level": node.level,
                "state": node.state,
                "children": [node_to_dict(child) for child in node.children]
            }
        return json.dumps(node_to_dict(self.root), indent=2)

    def describe(self):
        return self.root.recursive_describe()

if __name__ == "__main__":
    engine = FractalRealityEngine(max_depth=4)
    for _ in range(3):
        engine.simulate_step()
    print(engine.describe())
