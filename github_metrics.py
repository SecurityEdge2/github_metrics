from lib.load_data_github import load_data_from_github
from lib.upload_data_mongodb import upload_data_to_mongodb
from lib.calculate_metrics import calculate_wrt_timeline, calculate_drw_timeline
from config import config



def load_issues(github_repo_url, security_labels):
    return load_data_from_github(github_repo_url, security_labels)

def upload_data(timeline, collection):
    upload_data_to_mongodb(timeline, collection)

projects = config['app_weight']
for current_project, value in projects.items():
    app_weight, security_label = value
    issues = load_issues(current_project, security_label)
    timeline = calculate_wrt_timeline(issues, app_weight)
    timeline2 = calculate_drw_timeline(issues, app_weight)

    export_status = upload_data(timeline,  'wrt')
    export_status = upload_data(timeline2, 'drw')

print('Done')
