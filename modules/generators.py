from logger import logger
from settings import (
    FE_SERVICE_TYPE,
    BE_SERVICE_TYPE,
    FE_DOCKERFILE_TEMPLATES,
    BE_DOCKERFILE_TEMPLATES,
    FE_MANIFEST_TEMPLATE,
    BE_MANIFEST_TEMPLATE,
    INITIAL_JOB_TEMPLATE,
    COMPOSE_TEMPLATE,
    IMAGE_REGISTRY_USER,
    UAD_DOMAIN_NAME,
    REVERSE_PROXY_TEMPLATE,
)


class TemplateGenerator:
    def __init__(
        self,
        template_env,
        app_config,
        output_dockerfile,
        output_initial_job,
        output_manifest,
    ):
        self.template_env = template_env
        self.app_config = app_config
        self.output_dockerfile = output_dockerfile
        self.output_initial_job = output_initial_job
        self.output_manifest = output_manifest

    def _prepare_template_args(self, template):
        app_owner = self.app_config["app_owner"]
        app_name = self.app_config["app_name"]
        enable_frontend = "frontend" in self.app_config
        enable_backend = "backend" in self.app_config
        enable_database = "database" in self.app_config

        if template == BE_DOCKERFILE_TEMPLATES:
            return {
                "runtime": self.app_config["backend"]["image"],
                "version": self.app_config["backend"]["version"],
            }
        elif template == FE_DOCKERFILE_TEMPLATES:
            return {
                "runtime": self.app_config["frontend"]["image"],
                "version": self.app_config["frontend"]["version"],
                "static_dir": self.app_config["frontend"]["static_dir"],
            }
        elif template == INITIAL_JOB_TEMPLATE:
            return {
                "app_name": self.app_config["app_name"],
                "registry_user": IMAGE_REGISTRY_USER,
                "db_new_user": app_owner,
                "db_new_user_password": app_owner,
            }
        elif template == BE_MANIFEST_TEMPLATE:
            return {
                "uad_domain": UAD_DOMAIN_NAME,
                "registry_user": IMAGE_REGISTRY_USER,
                "app_name": app_name,
                "app_owner": app_owner,
            }
        elif template == FE_MANIFEST_TEMPLATE:
            return {
                "uad_domain": UAD_DOMAIN_NAME,
                "registry_user": IMAGE_REGISTRY_USER,
                "app_name": app_name,
                "app_owner": app_owner,
                "frontend_env_vars": self.app_config["frontend"]["env"],
            }
        elif template == COMPOSE_TEMPLATE:
            return {
                "registry_user": IMAGE_REGISTRY_USER,
                "enable_frontend": enable_frontend,
                "enable_backend": enable_backend,
                "enable_database": enable_database,
                "app_name": app_name,
                "app_owner": app_owner,
                "env_vars": self.app_config["frontend"]["env"]
                if enable_frontend
                else "",
                "database_type": self.app_config["database"]["image"]
                if enable_database
                else "",
            }
        elif template == REVERSE_PROXY_TEMPLATE:
            return {
                "frontend_domain_name": f"{app_owner}-{app_name}.{UAD_DOMAIN_NAME}",
                "backend_domain_name": f"api-{app_owner}-{app_name}.{UAD_DOMAIN_NAME}",
            }
        else:
            raise ValueError("Invalid template_type")

    def _save_output_to_file(self, content, file_name, prefix="output-"):
        with open(f"{prefix}{file_name}", "w") as file:
            file.write(content)

    def _generate_dockerfile(self, service_type):
        dockerfile_template = (
            FE_DOCKERFILE_TEMPLATES
            if service_type == FE_SERVICE_TYPE
            else BE_DOCKERFILE_TEMPLATES
        )
        runtime = self.app_config[service_type]["image"]
        template = self.template_env.get_template(dockerfile_template[runtime])
        template_args = self._prepare_template_args(dockerfile_template)
        dockerfile = template.render(template_args)
        self._save_output_to_file(
            dockerfile, f"{service_type}-{self.output_dockerfile}"
        )

    def _generate_initial_job(self):
        template = self.template_env.get_template(INITIAL_JOB_TEMPLATE)
        template_args = self._prepare_template_args(INITIAL_JOB_TEMPLATE)
        job = template.render(template_args)
        self._save_output_to_file(job, self.output_initial_job)

    def _generate_manifest(self, service_type):
        manifest_template = (
            FE_MANIFEST_TEMPLATE
            if service_type == FE_SERVICE_TYPE
            else BE_MANIFEST_TEMPLATE
        )
        template = self.template_env.get_template(manifest_template)
        template_args = self._prepare_template_args(manifest_template)
        manifest = template.render(template_args)
        self._save_output_to_file(manifest, f"{service_type}-{self.output_manifest}")

    def generate_customer_app_files(self):
        self._generate_initial_job()

        if FE_SERVICE_TYPE in self.app_config:
            self._generate_dockerfile(FE_SERVICE_TYPE)
            self._generate_manifest(FE_SERVICE_TYPE)

        if BE_SERVICE_TYPE in self.app_config:
            self._generate_dockerfile(BE_SERVICE_TYPE)
            self._generate_manifest(BE_SERVICE_TYPE)

    def generate_compose_file(self):
        template = self.template_env.get_template(COMPOSE_TEMPLATE)
        template_args = self._prepare_template_args(COMPOSE_TEMPLATE)
        dockerfile = template.render(template_args)
        self._save_output_to_file(dockerfile, "compose.yaml", prefix="")

    def generate_reverse_proxy_nginx_config(self):
        template = self.template_env.get_template(REVERSE_PROXY_TEMPLATE)
        template_args = self._prepare_template_args(REVERSE_PROXY_TEMPLATE)
        nginx_config = template.render(template_args)
        self._save_output_to_file(nginx_config, "nginx.conf", prefix="")
