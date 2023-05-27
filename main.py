import sys
import yaml
from yaml.loader import SafeLoader
from jinja2 import Environment, FileSystemLoader, select_autoescape
from generators import dockerfile_generator

TEMPLATE_DIR = 'templates'
DOCKERFILE_TEMPLATES = {
  'node': "nodejs-dockerfile.j2"
}


def prepare_template_environment():
  global template_env
  template_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape()
  )

def load_yaml_config(config_file):
  with open(config_file, 'r') as file:
    config = yaml.load(file, Loader=SafeLoader)
  return config
  

def main():
  if len(sys.argv) > 2:
    print(f"Generator accepts only 1 argument, got ${len(sys.argv) - 1}.")
    sys.exit(2)
  else:
    prepare_template_environment()
    config = load_yaml_config(sys.argv[1])
    generate_dockerfile(config)


if __name__ == "__main__":
  main()