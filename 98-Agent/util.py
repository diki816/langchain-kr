from IPython.display import Image, display
from langgraph.graph import StateGraph

def display_graph(graph: StateGraph):
    try:
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception:
        pass