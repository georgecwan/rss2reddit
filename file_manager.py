import json
import yaml

def load_config(config_file):
    # Loads the config file
    try:
        with open(config_file) as yaml_data_file:
            config = yaml.safe_load_all(yaml_data_file)
            return next(config), next(config)
    except Exception as e:
        print(f'Error loading {config_file}: {str(e)}')


def load_db(filename):
    # Loads the database file
    try:
        with open(filename) as file:
            return json.load(file)
    except Exception as e:
        print(f'Error loading {filename}: {str(e)}')
        print(f'Creating empty db...')
        return {}


def update_db(filename, db):
    with open(filename, 'w') as file:
        json.dump(db, file, indent=4)