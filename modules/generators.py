from settings import (
    DEPLOYMENT_TEMPLATE,
    DOCKERFILE_TEMPLATES,
    INITIAL_JOB_TEMPLATE,
    IMAGE_REGISTRY_USER,
    UAD_DOMAIN_NAME
)


class TemplateGenerator:
    def __init__(self, template_env, app_config):
        self.template_env = template_env
        self.app_config = app_config

    def _prepare_template_args(self, template):
        if template in DOCKERFILE_TEMPLATES:
            return {
                "runtime": self.app_config["backend"]["image"],
                "version": self.app_config["backend"]["version"],
            }
        elif template == INITIAL_JOB_TEMPLATE:
            return {
                "app_name": self.app_config["app_name"],
                "registry_user": IMAGE_REGISTRY_USER,
                "db_new_user": self.app_config["app_owner"],
                "db_new_user_password": self.app_config["app_owner"],
            }
        elif template == DEPLOYMENT_TEMPLATE:
            return {
                "uad_domain": UAD_DOMAIN_NAME,
                "registry_user": IMAGE_REGISTRY_USER,
                "app_name": self.app_config["app_name"],
                "app_owner": self.app_config["app_owner"],
            }
        else:
            raise ValueError("Invalid template_type")

    def _save_output_to_file(self, output, file_name):
        with open(file_name, "w") as file:
            file.write(output)

    def generate_dockerfile(self, output_file):
        runtime = self.app_config["backend"]["image"]
        template = self.template_env.get_template(DOCKERFILE_TEMPLATES[runtime])
        template_args = self._prepare_template_args(runtime)
        dockerfile = template.render(template_args)
        self._save_output_to_file(dockerfile, output_file)

    def generate_initial_job(self, output_file):
        template = self.template_env.get_template(INITIAL_JOB_TEMPLATE)
        template_args = self._prepare_template_args(INITIAL_JOB_TEMPLATE)
        job = template.render(template_args)
        self._save_output_to_file(job, output_file)
    
    def generate_manifest(self, output_file):
        template = self.template_env.get_template(DEPLOYMENT_TEMPLATE)
        template_args = self._prepare_template_args(DEPLOYMENT_TEMPLATE)
        manifest = template.render(template_args)
        self._save_output_to_file(manifest, output_file)
