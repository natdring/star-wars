import json
import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read('config/settings.ini')
 
interactions_data_file = config['DEFAULT']['data_dir_path'] + 'starwars-episode-1-interactions.json'

with open(interactions_data_file) as f:
    interactions_data = json.load(f)

character_df = pd.DataFrame(interactions_data['nodes'])
link_df = pd.DataFrame(interactions_data['links'])
