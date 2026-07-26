import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Any

class NormGraph:
    def __init__(self):
        self.G = nx.DiGraph()
    
    def add_transition(self, source: str, target: str, label: str, modality: str = "PERM"):
        self.G.add_edge(source, target, label=label, modality=modality)
    
    def visualize(self, title="NormGraph MVP"):
        pos = nx.spring_layout(self.G)
        plt.figure(figsize=(10, 6))
        
        nx.draw(self.G, pos, with_labels=True, node_color='lightblue', 
                node_size=2000, font_size=10, arrows=True)
        
        edge_labels = nx.get_edge_attributes(self.G, 'label')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        
        plt.title(title)
        plt.show()
    
    def get_stats(self) -> Dict:
        return {
            "nodes": self.G.number_of_nodes(),
            "edges": self.G.number_of_edges(),
            "transitions": list(self.G.edges(data=True))
        }
