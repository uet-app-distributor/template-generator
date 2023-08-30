import sys
import yaml
import logging

from yaml.loader import SafeLoader
from generators.dockerfile_generator import DockerfileGenerator
from jinja2 import Environment, FileSystemLoader, select_autoescape
from settings import TEMPLATE_DIR, DEPLOYMENT_TEMPLATE, NODEPORT_TEMPLATE


def load_yaml_config(config_file):
    with open(config_file, "r") as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config


def prepare_template_environment():
    return Environment(
        loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape()
    )


if __name__ == "__main__":
    app_config = load_yaml_config(sys.argv[1])
    template_env = prepare_template_environment()
    DockerfileGenerator(template_env, app_config).generate()
