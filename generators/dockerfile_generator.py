from generators.utils import save_output_to_file

from settings import DOCKERFILE_TEMPLATES, CUSTOMER_APP_DOCKERFILE


class DockerfileGenerator:
    def __init__(self, template_env, app_config):
        self.template_env = template_env
        self.app_config = app_config

    def _prepare_template_args(self):
        template_args = {"version": self.app_config["backend"]["version"]}
        return template_args

    def generate(self):
        runtime = self.app_config["backend"]["image"]
        template = self.template_env.get_template(DOCKERFILE_TEMPLATES[runtime])
        template_args = self._prepare_template_args()
        dockerfile = template.render(template_args)
        save_output_to_file(dockerfile, CUSTOMER_APP_DOCKERFILE)
