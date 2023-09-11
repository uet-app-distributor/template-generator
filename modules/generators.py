from logger import logger
from settings import (
    DEPLOYMENT_TEMPLATE,
    FE_SERVICE_TYPE,
    BE_SERVICE_TYPE,
    FE_DOCKERFILE_TEMPLATES,
    BE_DOCKERFILE_TEMPLATES,
    INITIAL_JOB_TEMPLATE,
    IMAGE_REGISTRY_USER,
    UAD_DOMAIN_NAME
)


class TemplateGenerator:
    def __init__(self, template_env, app_config, fe_output_dockerfile):
        self.template_env = template_env
        self.app_config = app_config
        self.fe_output_dockerfile = fe_output_dockerfile

    def _prepare_template_args(self, template):
        if template == BE_DOCKERFILE_TEMPLATES:
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
        elif template == FE_DOCKERFILE_TEMPLATES:
            return {
                "runtime": self.app_config["frontend"]["image"],
                "version": self.app_config["frontend"]["version"],
                "static_dir": self.app_config["frontend"]["static_dir"],
            }
        else:
            raise ValueError("Invalid template_type")

    def _save_output_to_file(self, output, file_name):
        with open(file_name, "w") as file:
            file.write(output)

    def _generate_dockerfile(self, service_type):
        runtime = self.app_config[service_type]["image"]
        dockerfile_template = FE_DOCKERFILE_TEMPLATES if service_type == FE_SERVICE_TYPE else BE_DOCKERFILE_TEMPLATES
        template = self.template_env.get_template(dockerfile_template[runtime])
        template_args = self._prepare_template_args(dockerfile_template)
        dockerfile = template.render(template_args)
        self._save_output_to_file(dockerfile, self.fe_output_dockerfile)

    def generate_initial_job(self, output_file):
        if self.app_config["backend"]:
            template = self.template_env.get_template(INITIAL_JOB_TEMPLATE)
            template_args = self._prepare_template_args(INITIAL_JOB_TEMPLATE)
            job = template.render(template_args)
            self._save_output_to_file(job, output_file)
        else:
            logger.info("No backend config found. Skip creating initial job.")
    
    def generate_manifest(self, output_file):
        template = self.template_env.get_template(DEPLOYMENT_TEMPLATE)
        template_args = self._prepare_template_args(DEPLOYMENT_TEMPLATE)
        manifest = template.render(template_args)
        self._save_output_to_file(manifest, output_file)

    def generate_customer_app_files(self):
        if FE_SERVICE_TYPE in self.app_config:
            self._generate_dockerfile(FE_SERVICE_TYPE)
