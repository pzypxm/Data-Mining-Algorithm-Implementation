from sys import argv
from networkx import Graph, connected_components, draw_networkx, neighbors, all_shortest_paths
from community import modularity
from matplotlib import pyplot


def get_graph(input_fd):
    input_fd.seek(0)
    G = Graph()
    edges = []
    for line in input_fd:
        temp = line.split('\n')[0].split(" ")
        edges.append((int(temp[0]), int(temp[1])))
    G.add_edges_from(edges)

    return G


def get_betweenness(input_fd):
    """
    Process:
    1. Select one node as root
    2. Use neighbor() to get information of parent(s) and children(s) for other nodes
    3. All leaf nodes have credit of 1.0/(# of their parents)
    4. Assign # of level to each node
    4. Start form bottom, in each level, add credit to their parents as well as to betweenness
    5. Divide the final betweenness value by 2.0
    """
    # Initial betweenness of edges (edge #: betweenness value)
    betweenness = {}
    input_fd.seek(0)
    for line in input_fd:
        temp = line.split('\n')[0].split(" ")
        temp = sorted([int(temp[0]), int(temp[1])])

        betweenness.setdefault(tuple(temp), 0.)

    # Initial information of nodes (node #: [[parents' #], [children's #], credit])

    graph = get_graph(input_fd)

    for root in graph.nodes():
        # Fill information for every node
        nodes_info = {}
        for current_node in graph.nodes():
            nodes_info.setdefault(current_node, [[], [], 1.])    # Initialize value of each node
            if current_node == root:
                nodes_info[current_node][0] = []
                nodes_info[current_node][1] = neighbors(graph, root)    # When the node is root
                nodes_info[current_node][2] = 0.0
            else:
                # Get every neighbor and then check
                for nei in neighbors(graph, current_node):

                    # Check if current neighbor is one of the parents
                    for path_to_root in all_shortest_paths(graph, current_node, root):
                        if len(set([nei]).intersection(path_to_root)) > 0:
                            nodes_info[current_node][0].append(nei)

                    # Check if current neighbor is one of the children
                    for nei_path_to_root in all_shortest_paths(graph, nei, root):
                        if len(set([current_node]).intersection(nei_path_to_root)) > 0:
                            nodes_info[current_node][1].append(nei)

        # Add level property for each node
        children = list(nodes_info[root][1])
        nodes_info[root].append(1)
        level = 1
        while len(children) > 0:
            level += 1
            children_buffer = []
            for child in children:
                nodes_info[child].append(level)
                for grand_child in nodes_info[child][1]:
                    if grand_child not in children_buffer:
                        children_buffer.append(grand_child)
            children = list(children_buffer)

        # Get maximum level (bottom)
        max_level = 0
        for node in nodes_info:
            if nodes_info[node][3] > max_level:
                max_level = int(nodes_info[node][3])
        current_level = max_level

        while current_level > 1:
            for current_node in nodes_info:
                if nodes_info[current_node][3] == current_level:

                    # Divide node's credit if more than one parents exist
                    if len(nodes_info[current_node][0]) > 1:
                        nodes_info[current_node][2] /= float(len(nodes_info[current_node][0]))

                    for parent_node in nodes_info[current_node][0]:

                        # Add children's value to parents
                        nodes_info[parent_node][2] += float(nodes_info[current_node][2])

                        # Add betweenness of this edge
                        current_edge = tuple(sorted([current_node, parent_node]))
                        betweenness[current_edge] += float(nodes_info[current_node][2])

            current_level -= 1

    # Divide all the betweenness value by 2
    for edge in betweenness:
        betweenness[edge] /= 2.

    # Transform to desired format
    btw = []
    for key in betweenness:
        btw.append([betweenness[key], key])

    return sorted(btw)


def get_optimal_communities(betweenness, G, G_cpy):
    partition_with_mod = []
    while len(betweenness) > 0:
        single = False      # Check if there are multiple nodes with same betweenness
        while not single:
            node_max_btw = betweenness.pop()
            G_cpy.remove_edge(node_max_btw[1][0], node_max_btw[1][1])
            if len(betweenness) == 0:
                break
            if node_max_btw[0] != betweenness[len(betweenness)-1][0]:
                single = True
        sub_graph = []
        for comp in connected_components(G_cpy):
            sub_graph.append(list(comp))

        # Get partition data structure
        community_label = 0
        partition = {}
        for sub in sub_graph:
            for node in sub:
                partition.setdefault(node, community_label)
            community_label += 1

        if len(betweenness) > 0:    # Calculate modularity and record
            partition_with_mod.append([modularity(partition, G), partition])

    return sorted(partition_with_mod).pop()[1]      # Select the partition with maximum modularity value


def output_partitions(partition):

    # Output separated communities
    all_communities = []
    current_community = []
    first = True
    for key in partition:
        if first:
            current_community.append(key)
            last_label = partition[key]
            first = False
        else:
            if partition[key] == last_label:
                current_community.append(key)
                last_label = partition[key]
            else:
                all_communities.append(current_community)
                current_community = [key]
                last_label = partition[key]
    all_communities.append(current_community)
    for com in all_communities:
        print com


def draw_graph(partition, graph, img_fd):
    value = []
    for key in partition:
        value.append(partition[key])
    draw_networkx(graph, node_color=value)
    pyplot.savefig(img_fd)

if __name__ == '__main__':

    # For IDE debugging
    input_fd = open("/Users/patrickpeng/Workspace_Python/HW_5/input2.txt")
    img_fd = "image.png"

    #input_fd = open(argv[1])
    #img_fd = str(argv[2])

    graph = get_graph(input_fd)
    graph_cpy = graph.copy()    # Make a copy of graph

    btw = get_betweenness(input_fd)

    optimal_partition = get_optimal_communities(btw, graph, graph_cpy)

    output_partitions(optimal_partition)

    draw_graph(optimal_partition, graph, img_fd)

