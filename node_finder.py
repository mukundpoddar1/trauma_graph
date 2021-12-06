import networkx as nx

def connected_nodes(graph, source_node, degree, number, weight_thres):
    '''
    this function is to 
    - print out all of the nodes associated to the source node corresponding the number of connected edges
    - plot the subgraph from the overall graph containing the source_node

    input: 
    graph: networkx graph
    source_node: source node name
    degree: number of edges in between the source_node and the returned node
    number: number of nodes to be returned

    output: nodes which satisfy requirments as specified above

    note: essentially the idea is to extract a subgraph coming from that node
    the result of this could be further verified by using nx.descendants(graph, source_node)
    '''
    if source_node not in graph:
        return []
    temp_graph = nx.Graph()
    result_nodes = {}
    all_nodes = [source_node]
    neighbors = [x for x in graph.neighbors(source_node)]
    weights = {}
    cur_num_edge = 1

    # iterate through current node in neighbor of the source node:

    # update node
    for cur_node in neighbors:
        weights[cur_node] = graph.get_edge_data(source_node,cur_node)['weight']
    # update result_nodes at number of edge = 1
    result_nodes[cur_num_edge] = [x for x in neighbors if weights[x]>weight_thres]
    # updates all node (all of the node which we have previously go through)
    all_nodes.extend(neighbors)
    # update neighbors information (which satistfy the weight threshold)
    neighbors = [x for x in neighbors if weights[x] > weight_thres]
    # iterate through the neighbors node, add edge to the output graph
    for ii in neighbors:
        temp_graph.add_edge(source_node, ii)

    # iterate through the neighbors of the neighbors
    while len(neighbors) != 0 and cur_num_edge < degree:

        temp = []

        cur_num_edge += 1

        for node in neighbors:

            temp.extend([x for x in graph.neighbors(node) if x not in all_nodes])

            cur_weight = weights[node]
            for cur_node in graph.neighbors(node):
                if cur_node not in all_nodes:
                    weights[cur_node] = cur_weight * graph.get_edge_data(node, cur_node)['weight']
                    if weights[cur_node] > weight_thres:
                        temp_graph.add_edge(node, cur_node)
            all_nodes.extend(temp)
        if len(temp)!=0:
            result_nodes[cur_num_edge] = [x for x in temp if weights[x]>weight_thres]
        neighbors = [x for x in temp if weights[x]>weight_thres]
        flattened_result = []
        [flattened_result.extend(x) for x in result_nodes.values()]

    return flattened_result

