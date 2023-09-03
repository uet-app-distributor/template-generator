import sys
import yaml
import logging
import argparse

from yaml.loader import SafeLoader
from modules.generators import TemplateGenerator
from jinja2 import Environment, FileSystemLoader, select_autoescape
from settings import TEMPLATE_DIR


def load_yaml_config(config_file):
    with open(config_file, "r") as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config


def prepare_template_environment():
    return Environment(
        loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape()
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--app-config", help="App YAML configuration file")
    parser.add_argument("--output-dockerfile", help="Output name of customer app Dockerfile")
    parser.add_argument("--output-initial-job", help="Output name of customer app initial job")
    parser.add_argument("--output-deployment", help="Output name of customer app deployment manifest file")

    options = parser.parse_args()

    app_config = load_yaml_config(options.app_config)
    template_env = prepare_template_environment()
    generator = TemplateGenerator(template_env, app_config)

    generator.generate_dockerfile(options.output_dockerfile)
    generator.generate_initial_job(options.output_initial_job)
    generator.generate_manifest(options.output_deployment)