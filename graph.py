import pydot
import json

def graph_drawer(user_input):
    graph = pydot.Dot(graph_name = "graph", graph_type="digraph", rankdir="LR")
    graph = pydot.Dot(graph_type="digraph", rankdir="LR")
    graph.add_node(pydot.Node(user_input["start"], shape="circle", style="filled", fillcolor="lightgreen"))

    for f in user_input["finals"]:
        graph.add_node(pydot.Node(f, shape="doublecircle", style="filled", fillcolor="lightcoral"))

    nodes_to_add = set()
    for t in user_input["transitions"]:
        nodes_to_add.add(t["from"])
        nodes_to_add.add(t["to"])

    for n in nodes_to_add:
        if n != user_input["start"] and n not in user_input["finals"]:
            graph.add_node(pydot.Node(n, shape="circle", style="filled", fillcolor="white"))

    for t in user_input["transitions"]:
        inputs = t["on"]
        if isinstance(inputs, list):
            label = ", ".join([str(i) if i is not None else "ε" for i in inputs])
        else:
            label = str(inputs)
            
        graph.add_edge(pydot.Edge(t["from"], t["to"], label=label))

    graph.write_png("automata.png")
