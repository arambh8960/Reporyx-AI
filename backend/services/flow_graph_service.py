from collections import defaultdict

def build_flow_graph(entities):

    graph = defaultdict(list)

    for entity in entities:

        # Route -> Handler
        for route in entity.get("routes", []):

            route_node = (
                f"{route['method']} "
                f"{route['path']}"
            )

            handler = route["handler"]

            if handler not in graph[route_node]:
                graph[route_node].append(handler)

        # Function -> Calls
        for func in entity.get("functions", []):

            func_name = func["name"]

            for call in func.get("calls", []):

                if call not in graph[func_name]:
                    graph[func_name].append(call)

    return graph


def format_graph(graph):

    result = []

    for node, neighbours in graph.items():

        result.append(node)

        for neighbour in neighbours:

            result.append(
                f"  -> {neighbour}"
            )

    return "\n".join(result)