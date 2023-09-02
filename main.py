import sys
import yaml
import logging

from yaml.loader import SafeLoader
from modules.generators import TemplateGenerator
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
    generator = TemplateGenerator(template_env, app_config)

    generator.generate_dockerfile()
    generator.generate_create_db_user_job()
    generator.generate_manifest()