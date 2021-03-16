from lib.load.github import load_from_github
from lib.upload.mongodb import upload_to_mongodb
from lib.calculate_metrics import calculate_wrt_timeline, calculate_drw_timeline2
from lib.jira_cloud_city import H1Issues
from lib.JiraAPI import JiraAPI
from lib.load.cloud_jira import load_data as load_jira
from config import config



def load_issues(github_repo_url, security_labels):
    return load_from_github(github_repo_url, security_labels)

def upload_data(timeline, collection):
    upload_to_mongodb(timeline, collection)

projects = config['app_weight']
for current_project, value in projects.items():
    app_weight, security_label = value
    #issues = load_issues(current_project, security_label)
    #m_wrt, q_wrt = calculate_wrt_timeline(issues, app_weight)


    #export_status = upload_data(q_wrt,  'wrt_q')
    #export_status = upload_data(m_wrt, 'wrt_m')
    #export_status = upload_data(drw, 'drw')

    data = load_jira()
    wrt = calculate_wrt_timeline(data)
    drw = calculate_drw_timeline2(data)
    upload_data(wrt,  'wrt')
    upload_data(drw, 'drw')
    exit(0)

print('Done')
