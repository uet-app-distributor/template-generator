from settings import (
    DEPLOYMENT_TEMPLATE,
    DOCKERFILE_TEMPLATES,
    CREATE_DB_USER_JOB_TEMPLATE,
    IMAGE_REGISTRY_USER
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
        elif template == CREATE_DB_USER_JOB_TEMPLATE:
            return {
                "db_new_user": self.app_config["app_owner"],
                "db_new_user_password": self.app_config["app_owner"],
            }
        elif template == DEPLOYMENT_TEMPLATE:
            return {
                "registry_user": IMAGE_REGISTRY_USER,
                "app_name": self.app_config["app_name"],
                "app_owner": self.app_config["app_owner"]
            }
        else:
            raise ValueError("Invalid template_type")

    def _save_output_to_file(self, output, file_name):
        with open(file_name, "w") as file:
            file.write(output)

    def generate_dockerfile(self):
        runtime = self.app_config["backend"]["image"]
        template = self.template_env.get_template(DOCKERFILE_TEMPLATES[runtime])
        template_args = self._prepare_template_args(runtime)
        dockerfile = template.render(template_args)
        self._save_output_to_file(dockerfile, "customer-app-dockerfile")

    def generate_create_db_user_job(self):
        template = self.template_env.get_template(CREATE_DB_USER_JOB_TEMPLATE)
        template_args = self._prepare_template_args(CREATE_DB_USER_JOB_TEMPLATE)
        job = template.render(template_args)
        self._save_output_to_file(job, "create-db-user-job.yaml")
    
    def generate_manifest(self):
        template = self.template_env.get_template(DEPLOYMENT_TEMPLATE)
        template_args = self._prepare_template_args(DEPLOYMENT_TEMPLATE)
        manifest = template.render(template_args)
        self._save_output_to_file(manifest, "customer-app-deployment.yaml")
