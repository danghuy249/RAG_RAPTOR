import pickle
from datetime import datetime
import os
import networkx as nx

def save_detailed_tree_info(save_path, output_file):
    """
    Load tree and save text report only
    """
    # Create both directories
    os.makedirs(save_path, exist_ok=True)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Create a sample tree if tree.pkl doesn't exist
    pkl_path = os.path.join(save_path, "tree.pkl")
    if not os.path.exists(pkl_path):
        print(f"Creating sample tree at {pkl_path}")
        # Create a simple tree structure for testing
        class Node:
            def __init__(self, index, text):
                self.index = index
                self.text = text
                self.children = set()

        class Tree:
            def __init__(self):
                self.num_layers = 2
                self.all_nodes = {}
                self.layer_to_nodes = {0: [], 1: []}
                self.root_nodes = {}
                
                # Create sample nodes
                node1 = Node(1, "Root node")
                node2 = Node(2, "Child node 1")
                node3 = Node(3, "Child node 2")
                
                # Set up relationships
                node1.children.add(2)
                node1.children.add(3)
                
                # Add nodes to tree
                self.all_nodes = {1: node1, 2: node2, 3: node3}
                self.layer_to_nodes[0] = [node1]
                self.layer_to_nodes[1] = [node2, node3]
                self.root_nodes = {1: node1}
        
        # Save sample tree
        tree = Tree()
        with open(pkl_path, 'wb') as f:
            pickle.dump(tree, f)
    
    # Load tree
    with open(pkl_path, 'rb') as f:
        tree = pickle.load(f)
    
    # Save text report only
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Tree Analysis Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Layers: {tree.num_layers}\n")
        f.write(f"Total Nodes: {len(tree.all_nodes)}\n")
        f.write("=" * 80 + "\n\n")

        for layer in range(tree.num_layers):
            f.write(f"\nLAYER {layer}\n")
            f.write("-" * 80 + "\n")
            
            layer_nodes = tree.layer_to_nodes.get(layer, [])
            f.write(f"Number of nodes in layer: {len(layer_nodes)}\n\n")
            
            for node in layer_nodes:
                f.write(f"Node ID: {node.index}\n")
                f.write(f"Text: {node.text}\n")
                f.write(f"Children nodes: {sorted(list(node.children))}\n")
                f.write("-" * 40 + "\n\n")

        f.write("\nROOT NODES\n")
        f.write("-" * 80 + "\n")
        for node in tree.root_nodes.values():
            f.write(f"Root Node ID: {node.index}\n")
            f.write(f"Text: {node.text}\n\n")
    
    return tree.num_layers, len(tree.all_nodes)

if __name__ == "__main__":
    # Use absolute path for testing
    current_dir = os.path.dirname(os.path.abspath(__file__))
    SAVE_PATH = os.path.join(current_dir, "demo", "cinderella")
    OUTPUT_FILE = os.path.join(current_dir, "demo", "tree_analysis.txt")
    
    try:
        num_layers, total_nodes = save_detailed_tree_info(SAVE_PATH, OUTPUT_FILE)
        print(f"Tree analysis saved to {OUTPUT_FILE}")
        print(f"Tree has {num_layers} layers and {total_nodes} total nodes")
    except Exception as e:
        print(f"Error: {str(e)}")

    print(f"Đường dẫn đầy đủ: {os.path.abspath(SAVE_PATH)}")
    print(f"File tree.pkl tồn tại: {os.path.exists(os.path.join(SAVE_PATH, 'tree.pkl'))}")