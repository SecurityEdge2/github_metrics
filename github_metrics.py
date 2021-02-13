from github import Github
import os

from config import config

def import_issues(github_repo_url):
    repo = g.get_repo("ClickHouse/ClickHouse")
    issues = repo.get_issues(labels=['security'], state='all')
    issues = list(issues)
    return issues

def calculate_wrt(issues):
    wrt = []
    defect_criticality_dict = config['defect_criticality']
    app_criticality = 0
    for issue in issues:
        for comment_count, criticality in defect_criticality_dict:
            if issue.comments >= comment_count:
                app_criticality += criticality

    return criticality

def search_security_issues(issues_list):
    a=1
    return None

def handle_issues_for_export(security_issues_list):
    return None

def export_to_mongo_db(result_data):
    return None

def export_issues(result_data):
    export_to_mongo_db(result_data)



g = Github(os.environ['github_token'])

#issues = import_issues(config['project']['url'])
issues = import_issues('ClickHouse/ClickHouse')

wrt = calculate_wrt(issues)
security_issues = search_security_issues(issues)
result_data = handle_issues_for_export(security_issues)
export_status = export_issues(result_data)

print(export_status)