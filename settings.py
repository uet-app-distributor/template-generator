IMAGE_REGISTRY_USER = "thainmtrashy"
TEMPLATE_DIR = "templates"
FE_SERVICE_TYPE = "frontend"
BE_SERVICE_TYPE = "backend"

UAD_DOMAIN_NAME = "uet-app-distributor.site"

BE_DOCKERFILE_TEMPLATES = {
    "node": "be-nodejs-dockerfile.j2",
    "django": "be-django-dockerfile.j2",
}
FE_DOCKERFILE_TEMPLATES = {"node": "fe-nodejs-dockerfile.j2"}
INITIAL_JOB_TEMPLATE = "customer-app-initial-job.yaml.j2"
REVERSE_PROXY_TEMPLATE = "customer-app-reverse-proxy.conf.j2"
COMPOSE_TEMPLATE = "customer-app-compose.yaml.j2"
BE_MANIFEST_TEMPLATE = "be-customer-app-deployment.yaml.j2"
FE_MANIFEST_TEMPLATE = "fe-customer-app-deployment.yaml.j2"
SHARED_RESOURCES_TEMPLATE = "customer-app-shared-resources.yaml.j2"

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
