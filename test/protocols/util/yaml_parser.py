import pyaml
import yaml


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = \
                super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class YamlConfigManager(metaclass=Singleton):

    def __init__(self):
        print("init yaml config manager")

        with open("config.yaml", "r") as stream:
            self.yaml_storage = yaml.safe_load(stream)

    def __str__(self):
        return pyaml.dump(self.yaml_storage)


def main():

    yaml_config_manager = YamlConfigManager()
    print(yaml_config_manager)

    yaml_config_manager2 = YamlConfigManager()
    print(yaml_config_manager2)

    print(yaml_config_manager.yaml_storage["protocol_WebSocket"])


if __name__ == '__main__':
    main()
