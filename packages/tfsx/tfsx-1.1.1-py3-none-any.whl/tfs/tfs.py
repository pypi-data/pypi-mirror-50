from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from pprint import pprint

class ProjectDTO(object):

    def __init__(self, project_id, teams):
        self.project_id = project_id
        self.teams = teams

class TFS(object):

    def __init__(self, personal_access_token, organization_url):

        self.credentials = BasicAuthentication('', personal_access_token)
        self.connection = Connection(base_url=organization_url, creds=self.credentials)
        self.core_client = self.connection.clients.get_core_client()


    def get_projects(self):
        projects = self.core_client.get_projects()
        return projects

    def get_teams(self, project_id):
        return self.core_client.get_teams(project_id)

    def get_team_members(self, project_id, team_id):
        
        return self.core_client.get_team_members_with_extended_properties(project_id=project_id,team_id=team_id)
        
    def get_all_team_project_organization(self):
       
        projects = self.core_client.get_projects()
        
        all_projects_teams = []

        for project in projects:
            teams = self.core_client.get_teams(project.id)
            project_DTO = ProjectDTO(project.id, teams)
            all_projects_teams.append (project_DTO)     
        
        return all_projects_teams
    
    def get_all_team_members_project(self):
        projects = self.core_client.get_projects()
        
        all_team_members = []

        # Show details about each project in the console
        for project in projects:
            teams = core_client.get_teams(project.id)
            for team in teams:
                team_members = core_client.get_team_members(project.id,team.id)
                for team_member in team_members:
                    team_member.additional_properties["team"] = team.id
                    all_team_members.append(team_member)
        return all_team_members
