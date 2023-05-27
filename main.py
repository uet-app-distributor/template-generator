import sys
import yaml
from yaml.loader import SafeLoader
from generators import dockerfile_generator
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATE_DIR = 'templates'


def load_yaml_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config


def prepare_template_environment():
    template_env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape()
    )
    return template_env


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f"Generator accepts only 1 argument, got ${len(sys.argv) - 1}.")
        sys.exit(2)
    else:
        config = load_yaml_config(sys.argv[1])
        template_env = prepare_template_environment()
        dockerfile_generator.generate_dockerfile(config, template_env)
