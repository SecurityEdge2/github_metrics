from lib.load.github import load_from_github
from lib.upload.mongodb import upload_to_mongodb
from lib.calculate_metrics import calculate_wrt_timeline, calculate_drw_timeline
from config import config



def load_issues(github_repo_url, security_labels):
    return load_from_github(github_repo_url, security_labels)

def upload_data(timeline, collection):
    upload_to_mongodb(timeline, collection)

projects = config['app_weight']
for current_project, value in projects.items():
    app_weight, security_label = value
    issues = load_issues(current_project, security_label)
    m_wrt, q_wrt = calculate_wrt_timeline(issues, app_weight)
    #drw = calculate_drw_timeline(issues, app_weight)

    export_status = upload_data(q_wrt,  'wrt_q')
    export_status = upload_data(m_wrt, 'wrt_m')
    #export_status = upload_data(drw, 'drw')
    exit(0)

print('Done')
