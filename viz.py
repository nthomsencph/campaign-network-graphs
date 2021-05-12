# imports
from plotly.offline import iplot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import networkx as nx   

from prep import get_data, random_color


def add_nodes_to_graph(graph : object, nodes : pd.DataFrame):
    for idx, char in nodes.iterrows():
        graph.add_node(char.name,
                       size = char.Size,
                       name = char.name,
                       color = random_color(char.group_id),
                       description = char.description,
                       weight = 1,
                       group = char.group) 

def add_links_to_graph(graph : object, links : pd.DataFrame, nodes : pd.DataFrame):

    node_lookup = dict(zip(nodes.name, nodes.index))
    
    for idx, link in links.iterrows(): # for each co-appearance between two characters, add an edge
        graph.add_edge(node_lookup[link.Source], 
                    node_lookup[link.Target], 
                    weight = 1, 
                    color = link.rel_color)


def get_node_coordinates(graph_obj : object, layout: object) -> tuple:
    
    Xn, Yn, Zn = [], [], []
    for k in range(graph_obj.number_of_nodes()): 
        Xn += [ layout[k][0] ] 
        Yn += [ layout[k][1] ]
        Zn += [ layout[k][2] ]

    return Xn, Yn, Zn

def get_link_coordinates(graph_obj : object, nodes_df : pd.DataFrame) -> tuple:
    
    edge_x, edge_y, edge_z = [], [], []
    for edge in graph_obj.edges():
        x0, y0, z0 = nodes_df.loc[edge[0]][["Xn", "Yn", "Zn"]].values
        x1, y1, z1 = nodes_df.loc[edge[1]][["Xn", "Yn", "Zn"]].values
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None) # I'll be perfectly honest. I have no idea why we append these None elements. But it works!
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        edge_z.append(z0)
        edge_z.append(z1)
        edge_z.append(None)

    return edge_x, edge_y, edge_z



def create_node_trace(node_cluster : pd.DataFrame, name : str) -> object:

    return go.Scatter3d(x = node_cluster.Xn, 
                        y = node_cluster.Yn, 
                        z = node_cluster.Zn, 
                        mode = 'markers + text', 
                        name = name, 
                        marker = dict(symbol = 'circle', 
                                    size = node_cluster.Size, 
                                    color = node_cluster.group_color),
                        line = dict(color='rgb(125,125,125)', width=0.5),
                        text = node_cluster.name, 
                        visible = True,
                        hoverinfo = 'text',
                        showlegend = True,
                        customdata = np.stack([node_cluster.description, 
                                               node_cluster.group], 
                                               axis = 1),
                        hovertemplate = ('%{text}'+\
                                        '<br><i>%{customdata[0]}</i><br>'+\
                                        '<b>Affiliation</b>: %{customdata[1]}<br>'))


def create_edge_trace(edge_x : list, edge_y : list, edge_z : list, edge_cluster : pd.DataFrame, name : str) -> object:
    return go.Scatter3d(x = edge_x, 
                        y = edge_y, 
                        z = edge_z,
                        name = name,
                        text = edge_cluster.Relation,
                        line = dict(width=1,
                                    color=edge_cluster.rel_color),
                        visible = True,
                        hoverinfo= 'text',
                        mode='lines')


def create_graph_object(links : pd.DataFrame, nodes : pd.DataFrame) -> object:

    dnd = nx.Graph() # our graph object

    add_nodes_to_graph(dnd, nodes) # adds nodes in place. No need for return
    add_links_to_graph(dnd, links, nodes)

    return dnd






def create_plot(links, nodes, graph):


    pos_ = nx.spring_layout(graph, 
                            dim = 3, 
                            k = 2, 
                            iterations = 100, 
                            threshold = 0.00001, 
                            seed = 93) # get coordinates for nodes in spring layoyt 

    placed_nodes = pd.merge(nodes, pd.DataFrame(zip(*get_node_coordinates(graph, pos_)), 
                                                columns = ["Xn", "Yn", "Zn"]),
                            left_index = True,
                            right_index = True)

    node_trace = create_node_trace(placed_nodes,
                                   name = "nodes")


    edge_trace = create_edge_trace(*get_link_coordinates(graph, 
                                                         placed_nodes), 
                                   links, 
                                   name = "edges")                                                               


    axis = dict(showbackground = False, 
            showline = False, 
            zeroline = False, 
            showgrid = False, 
            showticklabels = False, 
            showspikes = False,
            title = '')

    layout = go.Layout(
        # title = "Campaign Cast Network", 
        plot_bgcolor='#696969',
        autosize=True,
        # width = 1200,
        height = 900,
        showlegend = True,
        scene = dict(
            xaxis = dict(axis),
            yaxis = dict(axis),
            zaxis = dict(axis)))

    fig = go.Figure(data = [edge_trace, node_trace], 
                    layout = layout)

    return fig


def create_cast_plot():

    links, nodes = get_data()
    dnd = create_graph_object(links, nodes)
    fig = create_plot(links, nodes, dnd)

    # fig.write_html("output/campaign-cast.html")                

 
    return fig



if __name__ == '__main__':
    
    create_cast_plot()
    


                        