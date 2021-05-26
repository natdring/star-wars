import json
import configparser
import pandas as pd
from graphviz import Graph

config = configparser.ConfigParser()
config.read('config/settings.ini')
 
interactions_data_file = config['DEFAULT']['data_dir_path'] + 'starwars-episode-1-interactions.json'

with open(interactions_data_file) as f:
    interactions_data = json.load(f)

# node_df = pd.DataFrame(interactions_data['nodes'])
# link_df = pd.DataFrame(interactions_data['links'])

dot = Graph(comment='SW EP1 INTERACTIONS')

i=0
for node in interactions_data['nodes']:
    dot.node(str(i), label=node['name'], color=node['colour'])
    i+=1

for link in interactions_data['links']:
    dot.edge(str(link['source']), str(link['target']), value=str(link['value']))

dot.render('test-output/sw.gv', view=True)