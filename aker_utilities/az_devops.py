from typing import Any

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.git.models import GitItem


class DevOpsSDK:
    """
    # from azure.devops.v7_0.git import git_client_base  # This is for codebase ref only
    # from azure.devops.v7_0.core import core_client     # This is for codebase ref only
    """
    def __init__(
        self,
        organization: str,
        project: str,
        url: str | None = None,
        pat: str | None = None,
    ) -> None:
        self.organization = organization
        self.project = project

        # URL for devops rest api
        if url is None:
            self.url = "https://dev.azure.com"
        else:
            self.url = url

        # Fill in with your personal access token and org URL
        _organization_url = self.url + "/" + self.organization
        # PAT is passed as argument to remove environment variable dependency
        # or default access level if pat is set to None
        _personal_access_token = str(pat)

        # Create a connection to the org
        _credentials = BasicAuthentication("", _personal_access_token)
        _connection = Connection(base_url=_organization_url, creds=_credentials)

        # Get a client (the "core" client provides access to projects, teams, etc)
        self.core_client = _connection.clients.get_core_client()
        self.git_client = _connection.clients.get_git_client()

    def get_organization_projects(self) -> list[dict[str, Any]]:
        # Get all projects for the organization
        projects = self.core_client.get_projects()
        return projects

    def get_organization_repositories(self) -> list[dict[str, Any]]:
        # Get all repositories for all the projects
        organization_repositories = self.git_client.get_repositories()
        return organization_repositories

    def get_project_repositories(self) -> list[dict[str, Any]]:
        # Get all repositories for a specific project
        project_repositories = self.git_client.get_repositories(project=self.project)
        return project_repositories

    def get_repository_items(self, repository: str) -> list[dict[str, Any]]:
        # Get all the items in repo starting from the root folder recursively
        repository_items: list[GitItem] = self.git_client.get_items(
            project=self.project,
            repository_id=repository,
            scope_path="/",
            recursion_level="full",
        )
        return [item.as_dict() for item in repository_items]

    def get_item(self, repository: str, path: str) -> dict[str, Any]:
        # Get the item in the repository
        item: GitItem = self.git_client.get_item(
            project=self.project,
            repository_id=repository,
            path=path,
            include_content=True
        )
        return item.as_dict()

    def read_file_as_str(self, repository: str, path: str | None) -> str:
        # Get the file content

        if path is not None:
            repo_file = self.get_item(repository=repository, path=path)

            repo_file_content = repo_file.get("content", "")
        else:
            repo_file_content = ""

        return repo_file_content

    def push_changes(self, repository: str) -> None:
        ...

    def __str__(self) -> str:
        return f"MS DevOps wrapper for {self.project} project in {self.organization} org"

    def __repr__(self) -> str:
        return f"MS DevOps Wrapper for {self.project} project in {self.organization} org"
