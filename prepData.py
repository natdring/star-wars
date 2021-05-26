import pandas as pd
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

        tmp = pd.DataFrame(interactions_data['nodes'])
        tmp['episode'] = i
        link_df = link_df.append(tmp)

        with open(mentions_data_file) as f:
            mentions_data = json.load(f)
        tmp = pd.DataFrame(mentions_data['nodes'])
        tmp['episode'] = i
        mentions_df = mentions_df.append(tmp)
    
    return node_df, link_df, mentions_df

if __name__ == "__main__":
    prepData()