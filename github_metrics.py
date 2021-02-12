from config import config

def export_issues(github_repo_url):
    return None

def search_security_issues(issues_list):
    return None

def handle_issues_for_export(security_issues_list):
    return None

def export_to_mongo_db(result_data):
    return None

def export_issues(result_data):
    export_to_mongo_db(result_data)

all_issues = export_issues(config['config']['url'])
security_issues = search_security_issues(all_issues)
result_data = handle_issues_for_export(security_issues)
export_status = export_issues(result_data)

print(export_status)