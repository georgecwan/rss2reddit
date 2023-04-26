import json
import yaml


def load_config(config_file: str) -> tuple[list[dict], dict[str, str]]:
    """
    Loads the config file

    Args:
        config_file: Absolute path to the config file

    Returns:
        The configurations and credentials from the config file
    """
    try:
        with open(config_file) as yaml_data_file:
            config = yaml.safe_load_all(yaml_data_file)
            return next(config), next(config)
    except Exception as e:
        print(f'Error loading {config_file}: {str(e)}')


def load_db(filename: str) -> dict[str, dict]:
    """
    Loads the database file

    Args:
        filename: Absolute path to the database JSON file

    Returns:
        The dictionary stored in the database JSON file if it exists, otherwise an empty dictionary
    """
    try:
        with open(filename) as file:
            return json.load(file)
    except Exception as e:
        print(f'Error loading {filename}: {str(e)}')
        print(f'Creating new db...')
        return {}


def update_db(filename: str, db: dict[str, dict]) -> None:
    """
    Updates the database file

    Args:
        filename: Path to the database JSON file
        db: The dictionary to be stored in the database JSON file

    Returns:
        None
    """
    with open(filename, 'w') as file:
        json.dump(db, file, indent=2)
