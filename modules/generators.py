from settings import (
    DOCKERFILE_TEMPLATES,
    CREATE_DB_USER_JOB_TEMPLATE,
    TYPE_DOCKERFILE,
    TYPE_K8S_JOB,
    TYPE_K8S_MANIFEST,
)


class TemplateGenerator:
    def __init__(self, template_env, app_config):
        self.template_env = template_env
        self.app_config = app_config

    def _prepare_template_args(self, template_type):
        if template_type == TYPE_DOCKERFILE:
            template_args = {
                "runtime": self.app_config["backend"]["image"],
                "version": self.app_config["backend"]["version"],
            }
        elif template_type == TYPE_K8S_JOB:
            template_args = {
                "db_new_user": self.app_config["app_owner"],
                "db_new_user_password": self.app_config["app_owner"],
            }
        else:
            raise ValueError("Invalid template_type")
        return template_args

    def _save_output_to_file(self, output, file_name):
        with open(file_name, "w") as file:
            file.write(output)

    def generate_dockerfile(self):
        runtime = self.app_config["backend"]["image"]
        template = self.template_env.get_template(DOCKERFILE_TEMPLATES[runtime])
        template_args = self._prepare_template_args(TYPE_DOCKERFILE)
        dockerfile = template.render(template_args)
        self._save_output_to_file(dockerfile, "customer-app-dockerfile")

    def generate_create_db_user_job(self):
        template = self.template_env.get_template(CREATE_DB_USER_JOB_TEMPLATE)
        template_args = self._prepare_template_args(TYPE_K8S_JOB)
        job = template.render(template_args)
        self._save_output_to_file(job, "create-db-user-job.yaml")
