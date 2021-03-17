from lib.load.github import load_from_github
from lib.upload.mongodb import upload_to_mongodb
from lib.calculate_metrics import calculate_wrt_timeline, calculate_drw_timeline2
from lib.jira_cloud_city import H1Issues
from lib.JiraAPI import JiraAPI
from lib.load.cloud_jira import load_data as load_jira
from config import config


def upload_data(timeline, db, collection):
    upload_to_mongodb(timeline, db, collection)


if config['services']['github']['enabled'] == True:
    issues = load_from_github()
    if config['services']['metrics']['wrt']:
        wrt = calculate_wrt_timeline(issues)
        upload_data(wrt, config['services']['github']['upload_db'], 'wrt')
    if config['services']['metrics']['drw']:
        wrt = calculate_wrt_timeline(issues)
        upload_data(wrt,config['services']['github']['upload_db'],'drw')

if config['services']['jira']['enabled'] == True:
    issues = load_jira()
    if config['services']['metrics']['wrt']:
        wrt = calculate_wrt_timeline(issues)
        upload_data(wrt, config['services']['jira']['upload_db'], 'wrt')
    if config['services']['metrics']['drw']:
        wrt = calculate_wrt_timeline(issues)
        upload_data(wrt, config['services']['jira']['upload_db'], 'drw')

print('Done')
