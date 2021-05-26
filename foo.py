import json
import configparser
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

config = configparser.ConfigParser()
config.read('config/settings.ini')
 
interactions_data_file = config['DEFAULT']['data_dir_path'] + 'starwars-episode-3-interactions.json'

with open(interactions_data_file) as f:
    interactions_data = json.load(f)

# node_df = pd.DataFrame(interactions_data['nodes'])
# link_df = pd.DataFrame(interactions_data['links'])

G_weighted = nx.Graph()

characters = []
for node in interactions_data['nodes']:
    characters.append(node['name'])

for link in interactions_data['links']:
    G_weighted.add_edge(characters[link['source']], characters[link['target']], weight=link['value'])

nx.draw_networkx(G_weighted)
plt.show()