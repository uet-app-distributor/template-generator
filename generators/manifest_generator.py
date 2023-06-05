from jinja2 import Environment, FileSystemLoader, select_autoescape


def prepare_template_vars(config):
    app_config = config['appSpec']
    database_config = config['databaseSpec']
    template_vars = {
        'app_name': config['project'],
        'runtime': app_config['image'],
        'runtime_version': app_config['version'],
        'app_vars': app_config['env'],
        'database': database_config['image'],
        'database_version': database_config['version'],
        'db_vars': database_config['env']
    }
    print(template_vars)
    return template_vars


def save_output_to_file(output, file_name):
    with open(file_name, "w") as file:
        file.write(output)


def generate_manifest(config, template_env, template_file, suffix):
    template = template_env.get_template(template_file)
    template_vars = prepare_template_vars(config)
    manifest = template.render(template_vars)
    save_output_to_file(manifest, f"{config['project']}-{suffix}")
