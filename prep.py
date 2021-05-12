# imports
import pandas as pd
import random 

def random_color(i):
    random.seed(i)
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % ( r(), r(), r() )

def import_data(sheet_name, sheet_id = "1gQ69WDBNpTIegl1pKKwLvN2KJfTRnird6_2P41_qwfo"):
    return pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={sheet_name}")

def encode_factions_to_ints(nodes):
    nodes.group = pd.Categorical(nodes.group)
    nodes['group_id'] = nodes.group.cat.codes
    return nodes

def add_node_sizes(nodes, links):

    sizes = links.Target.append(links.Source).value_counts()
    nodes = nodes.merge(pd.DataFrame({"Source" : sizes.index,
                              "Size" : sizes.values}), 
                left_on = "name",
                right_on = "Source",
                how = "left") \
                .drop("Source", axis = 1)

    nodes.Size = nodes.Size.fillna(nodes.Size.mean())
    return nodes                        

def set_group_color(nodes):
    nodes["group_color"] = nodes.group_id.apply(lambda x: random_color(x))
    return nodes


def set_link_relation_color(links):
    rel_color_lookup = {"Friend" : "green", 
                        "Foe" : 'red', 
                        "Unknown" : 'blue'}
                    
    links["rel_color"] = links.Relation.apply(lambda x: rel_color_lookup[x])
    return links
                                                      

def get_data():

    links = (import_data("1435699897").pipe(set_link_relation_color)) # import links and set color
    nodes = (import_data("1157642109").pipe(encode_factions_to_ints) # import nodes and encode factions
                                      .pipe(add_node_sizes, links) # set node sizes based on # of relations
                                      .pipe(set_group_color)) # sets a random but consistent color. Specify instead?
                            
    return links, nodes


    

                
            


