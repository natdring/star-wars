from os import link
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import configparser
import json

config = configparser.ConfigParser()
config.read('config/settings.ini')

def prepData():
    node_df = pd.DataFrame()
    link_df = pd.DataFrame()
    mentions_df = pd.DataFrame()

    for i in range(1,8):
        interactions_data_file = config['DEFAULT']['data_dir_path'] + 'starwars-episode-' + str(i) + '-interactions.json'
        mentions_data_file = config['DEFAULT']['data_dir_path'] + 'starwars-episode-' + str(i) + '-mentions.json'

        with open(interactions_data_file) as f:
            interactions_data = json.load(f)

        tmp = pd.DataFrame(interactions_data['nodes'])
        tmp['episode'] = i
        node_df = node_df.append(tmp)

        tmp = pd.DataFrame(interactions_data['links'])
        tmp['episode'] = i
        link_df = link_df.append(tmp)

        with open(mentions_data_file) as f:
            mentions_data = json.load(f)
        tmp = pd.DataFrame(mentions_data['nodes'])
        tmp['episode'] = i
        mentions_df = mentions_df.append(tmp)
    
    return node_df, link_df, mentions_df

def prepNetwork():
    node_df, link_df, mentions_df = prepData()

    networks = {}
    for i in range(1,8):
        G_weighted = nx.Graph()

        curr_df = link_df.loc[link_df['episode'] == i]
        for index, link in curr_df.iterrows():
            # print(node_df.iloc[link['source']]['name'])
            # print(node_df.iloc[link['target']]['name'])
            # print(link['value']))
            G_weighted.add_edge(node_df.iloc[link['source']]['name'], node_df.iloc[link['target']]['name'], weight=link['value'])
        
        networks[i] = G_weighted

    return networks
    


if __name__ == "__main__":
    prepNetwork()
    nx.draw_networkx(prepNetwork()[1])
    plt.show()