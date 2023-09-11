IMAGE_REGISTRY_USER = "thainm"
TEMPLATE_DIR = "templates"
FE_SERVICE_TYPE = "frontend"
BE_SERVICE_TYPE = "backend"

UAD_DOMAIN_NAME = "uet-app-distributor.site"

BE_DOCKERFILE_TEMPLATES = {"node": "be-nodejs-dockerfile.j2"}
FE_DOCKERFILE_TEMPLATES = {"node": "fe-nodejs-dockerfile.j2"}
INITIAL_JOB_TEMPLATE = "customer-app-initial-job.yaml.j2"
DEPLOYMENT_TEMPLATE = "customer-app-deployment.yaml.j2"

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"