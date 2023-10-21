from .client import ProjectsRestClient


def test_health(projects_rest_client: ProjectsRestClient):
    projects_rest_client.get_health()
