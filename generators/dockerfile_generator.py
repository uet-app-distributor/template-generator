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
    prepare_template_environment()
    runtime = config['appSpec']['image']
    dockerfile_template = DOCKERFILE_TEMPLATES[runtime]
    template = template_env.get_template(dockerfile_template)
    template_vars = prepare_template_vars(runtime, config)
    dockerfile = template.render(template_vars)
    save_output_to_file(dockerfile, f"{config['project']}-app-dockerfile")
