from lib.load_data_github import load_data_from_github
from lib.upload_data_mongodb import upload_data_to_mongodb
from lib.calculate_metrics import calculate_wrt_timeline, calculate_drw_timeline
from config import config




def load_issues(github_repo_url):
    return load_data_from_github(github_repo_url)

def upload_data(timeline):
    upload_data_to_mongodb(timeline)

projects = config['app_weight']
for current_project, app_weight in projects.items():
    issues = load_issues(current_project)
    timeline = calculate_drw_timeline(issues, app_weight)
    export_status = upload_data(timeline)

print('Done')
