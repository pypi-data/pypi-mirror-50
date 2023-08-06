import os

from method_defaults.config_manager import Config


def get_available_config_files(paths, extensions):
    possible_files = [
        (".").join([path, extension])
        for path in paths for extension in extensions
    ]
    for file_path in possible_files:
        if os.path.isfile(file_path):
            yield file_path


def get_config():
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".config", "eeutils")
    paths = [
        os.path.join(home_dir, '.eeutils'),
        os.path.join(config_dir, 'eeutils'),
    ]
    extensions = ["ini", "yaml", "json"]
    try:
        config_file = next(get_available_config_files(paths, extensions))
    except StopIteration:
        config_file = None
    config = Config(config_file)
    return config


config = get_config()
