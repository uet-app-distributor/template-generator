import sys
import yaml
from yaml.loader import SafeLoader
from jinja2 import Environment, FileSystemLoader, select_autoescape


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

def prepare_template_vars(runtime, config):
  if runtime == 'node':
    vars = {
      'version': config['appSpec']['version']
    }
  return vars

def save_output_to_file(output, file_name):
  with open(file_name, "w") as file:
    file.write(output)

def generate_dockerfile(config):
  runtime = config['appSpec']['image']
  dockerfile_template = DOCKERFILE_TEMPLATES[runtime]
  template = template_env.get_template(dockerfile_template)
  template_vars = prepare_template_vars(runtime, config)
  dockerfile = template.render(template_vars)
  save_output_to_file(dockerfile, f"{config['project']}-app-dockerfile")
  

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