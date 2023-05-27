import sys
import yaml
from yaml.loader import SafeLoader
from generators import dockerfile_generator


def load_yaml_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f"Generator accepts only 1 argument, got ${len(sys.argv) - 1}.")
        sys.exit(2)
    else:
        config = load_yaml_config(sys.argv[1])
        dockerfile_generator.generate_dockerfile(config)
