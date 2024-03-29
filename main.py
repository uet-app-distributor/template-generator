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
    parser.add_argument(
        "--output-dockerfile",
        default="dockerfile",
        help="Output name of customer app Dockerfile",
    )
    parser.add_argument(
        "--output-initial-job",
        default="initial-job",
        help="Output name of customer app initial job",
    )
    parser.add_argument(
        "--output-manifest",
        default="manifest",
        help="Output name of customer app deployment manifest file",
    )
    parser.add_argument(
        "--compose",
        type=bool,
        choices=[True, False],
        default=False,
        help="Specify generating compose.yml file",
    )

    options = parser.parse_args()

    app_config = load_yaml_config(options.app_config)
    template_env = prepare_template_environment()
    generator = TemplateGenerator(
        template_env,
        app_config,
        options.output_dockerfile,
        options.output_initial_job,
        options.output_manifest,
    )

    generator.generate_customer_app_files()

    if options.compose:
        generator.generate_compose_file()
        generator.generate_reverse_proxy_nginx_config()
