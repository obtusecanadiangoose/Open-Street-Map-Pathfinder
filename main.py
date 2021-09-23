import osmnx as ox
import imageio
import os

#If output is true, all steps are shown, if false, only the final path is shown
output = True

#The starting point will be the closest node (intersection) to this point
origin = (43.693450, -80.385900)

#The minimum distance (in Metres) that the path must be
dist = 10000




def find_next_nodes_from_point(lat, long):
    origin_node = ox.get_nearest_node(G, (lat, long))

    # lat = G.nodes[origin_node]['y']
    # long = G.nodes[origin_node]['x']
    dest_nodes = []

    num_edges1 = ox.get_nearest_edge(G, (lat + 0.0001, long))
    if num_edges1[0] != origin_node and num_edges1[0] not in dest_nodes:
        dest_nodes.append(num_edges1[0])
    if num_edges1[1] != origin_node and num_edges1[1] not in dest_nodes:
        dest_nodes.append(num_edges1[1])

    num_edges2 = ox.get_nearest_edge(G, (lat - 0.0001, long))
    if num_edges2[0] != origin_node and num_edges2[0] not in dest_nodes:
        dest_nodes.append(num_edges2[0])
    if num_edges2[1] != origin_node and num_edges2[1] not in dest_nodes:
        dest_nodes.append(num_edges2[1])

    num_edges3 = ox.get_nearest_edge(G, (lat, long + 0.0001))
    if num_edges3[0] != origin_node and num_edges3[0] not in dest_nodes:
        dest_nodes.append(num_edges3[0])
    if num_edges3[1] != origin_node and num_edges3[1] not in dest_nodes:
        dest_nodes.append(num_edges3[1])

    num_edges4 = ox.get_nearest_edge(G, (lat, long - 0.0001))
    if num_edges4[0] != origin_node and num_edges4[0] not in dest_nodes:
        dest_nodes.append(num_edges4[0])
    if num_edges4[1] != origin_node and num_edges4[1] not in dest_nodes:
        dest_nodes.append(num_edges4[1])

    dists = []
    routes = []
    for node in dest_nodes:
        routes.append([origin_node, node])
        edge_lengths = ox.utils_graph.get_route_edge_attributes(G, routes[0], 'length')
        dists.append(sum(edge_lengths))
    if len(routes) == 0:
        print("map machine broke")

    longest_route = routes[dists.index(max(dists))]
    longest_node = longest_route[1]
    return longest_node, max(dists)


def find_next_nodes_from_node(node, curr_path, blacklist):
    origin_node = node

    lat = G.nodes[origin_node]['y']
    long = G.nodes[origin_node]['x']
    dest_nodes = []

    num_edges1 = ox.get_nearest_edge(G, (lat + 0.0001, long))
    if num_edges1[0] != origin_node and num_edges1[0] not in dest_nodes and num_edges1[0] not in curr_path\
            and num_edges1[0] not in blacklist:
        dest_nodes.append(num_edges1[0])
    if num_edges1[1] != origin_node and num_edges1[1] not in dest_nodes and num_edges1[1] not in curr_path\
            and num_edges1[1] not in blacklist:
        dest_nodes.append(num_edges1[1])

    num_edges2 = ox.get_nearest_edge(G, (lat - 0.0001, long))
    if num_edges2[0] != origin_node and num_edges2[0] not in dest_nodes and num_edges2[0] not in curr_path\
            and num_edges2[0] not in blacklist:
        dest_nodes.append(num_edges2[0])
    if num_edges2[1] != origin_node and num_edges2[1] not in dest_nodes and num_edges2[1] not in curr_path\
            and num_edges2[1] not in blacklist:
        dest_nodes.append(num_edges2[1])

    num_edges3 = ox.get_nearest_edge(G, (lat, long + 0.0001))
    if num_edges3[0] != origin_node and num_edges3[0] not in dest_nodes and num_edges3[0] not in curr_path\
            and num_edges3[0] not in blacklist:
        dest_nodes.append(num_edges3[0])
    if num_edges3[1] != origin_node and num_edges3[1] not in dest_nodes and num_edges3[1] not in curr_path\
            and num_edges3[1] not in blacklist:
        dest_nodes.append(num_edges3[1])

    num_edges4 = ox.get_nearest_edge(G, (lat, long - 0.0001))
    if num_edges4[0] != origin_node and num_edges4[0] not in dest_nodes and num_edges4[0] not in curr_path\
            and num_edges4[0] not in blacklist:
        dest_nodes.append(num_edges4[0])
    if num_edges4[1] != origin_node and num_edges4[1] not in dest_nodes and num_edges4[1] not in curr_path\
            and num_edges4[1] not in blacklist:
        dest_nodes.append(num_edges4[1])

    dists = []
    routes = []
    for node in dest_nodes:
        try:
            edge_lengths = ox.utils_graph.get_route_edge_attributes(G, [origin_node, node], 'length')
            dists.append(sum(edge_lengths))
            routes.append([origin_node, node])
        except AttributeError:
            pass
    if len(routes) == 0:
        return 0

    longest_route = routes[dists.index(max(dists))]
    longest_node = longest_route[1]
    return longest_node, max(dists)


counter = 0

ox.config(use_cache=True, log_console=False)


G = ox.graph_from_point((origin[0], origin[1]), dist=1750, network_type='all')

blacklist = [] #list of dead end nodes or nodes that lead to dead ends
dist_blacklist = []

total_dist = []
curr_path = [ox.get_nearest_node(G, (origin[0], origin[1]))]
route1 = find_next_nodes_from_point(origin[0], origin[1])
curr_path.append(route1[0])
total_dist.append(route1[1])
if output == True:
    fig, ax = ox.plot_graph_route(G, curr_path)
    fig.savefig(str(counter))
    counter += 1



while (sum(total_dist) // 1) < dist:
    while (sum(total_dist) // 1) < dist:
        #print(curr_path)
        route = find_next_nodes_from_node(curr_path[-1], curr_path, blacklist)

        depth = 1
        while route == 0:
            blacklist.append(curr_path[-depth])
            dist_blacklist.append(total_dist[-depth])

            depth += 1
            route = find_next_nodes_from_node(curr_path[-depth], curr_path, blacklist)

        curr_path.append(route[0])
        total_dist.append(route[1])

        for bad_node in blacklist:
            if bad_node in curr_path:
                curr_path.remove(bad_node)
        if output == True:
            fig, ax = ox.plot_graph_route(G, curr_path)
            fig.savefig(str(counter))
            counter += 1

    for bad_dist in dist_blacklist:
        if bad_dist in total_dist:
            total_dist.remove(bad_dist)

print("nodes used:")
print(curr_path)
fig, ax = ox.plot_graph_route(G, curr_path)
print("Total Distance: " + str(sum(total_dist) // 1))
fig.savefig("output")
counter += 1
if output == True:
#a lazy way to make the final frame of the animation longer
    fig.savefig(str(counter))
    counter += 1
    fig.savefig(str(counter))
    counter += 1
    fig.savefig(str(counter))
    counter += 1
    fig.savefig(str(counter))
    counter += 1
    fig.savefig(str(counter))
    counter += 1
    fig.savefig(str(counter))
    counter += 1
    fig.savefig(str(counter))
    counter += 1
    fig.savefig(str(counter))
    counter += 1
    fig.savefig(str(counter))
    counter += 1
    fig.savefig(str(counter))
    counter += 1


if output == True:
    images = []
    for i in range(counter):
        images.append(imageio.imread(str(i)+".png"))
    imageio.mimsave('animation.gif', images, duration=1)
    for i in range(counter):
        os.remove(str(i)+".png")


