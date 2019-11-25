import os
import yaml


class Config:
    def __init__(self):
        self.config = ''
        self.fetch_config()

    def fetch_config(self):
        script_dir = os.path.dirname(__file__)
        try:
            #with open(os.path.join(script_dir, "config.yml"), 'r') as stream:
            with open("config.yml", 'r') as stream:
                try:
                    self.config = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
        except:
            with(open(os.path.join(script_dir, "config.yml"), 'w+')) as file:
                file.write('sources:\n')
                file.write('  full: "Nincs fájl kiválasztva."\n')
                file.write('  terv: "Nincs fájl kiválasztva."')



