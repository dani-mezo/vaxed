import os
import yaml


class Config:
    def __init__(self):
        self.config = ''
        self.fetch_config()

    def fetch_config(self):
        script_dir = os.path.dirname(__file__)
        with open(os.path.join(script_dir, "../config.yml"), 'r') as stream:
            try:
                self.config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)