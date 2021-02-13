from lib.load_data_github import load_data_from_github
from lib.upload_data_mongodb import upload_data_to_mongodb
from datetime import datetime, timedelta
from config import config
from collections import OrderedDict

def load_issues(github_repo_url):
    return load_data_from_github(github_repo_url)

def calculate_wrt_timeline(issues, app_weight):

    def calculate_wrt_for_issue(issue, app_weight, dc_dict):
        severity = issue['severity']
        defect_criticality = dc_dict[severity]
        issue_wrt = defect_criticality *app_weight
        return issue_wrt

    #инициализируем переменные
    first_date = (datetime.now() + timedelta(days=1))
    end_date = (datetime.now() - timedelta(days=365*30))
    #находим значения для frst_date & last_date
    for issue in issues:
            if issue['start_date'] < first_date:
                first_date = issue['start_date']
            if issue['end_date'] > end_date:
                end_date = issue['end_date']
            #подсчитываем criticality для конкретного issue
            issue['criticality'] = calculate_wrt_for_issue(issue,app_weight,config['defect_criticality_dict'])

    timeline = list()
    iter_day = first_date
    #складываем criticality от разных issue в конкретный день
    while iter_day<= end_date:
        #date=iter_day.strftime('%d/%m/%Y')
        unit = dict(criticality=0, date=iter_day)
        for issue in issues:
            if issue['start_date'] <= iter_day and iter_day <= issue['end_date']:
                unit['criticality'] += issue['criticality']
                unit['project'] = issue['project']
        timeline.append(unit)
        iter_day += timedelta(days=1)


    return timeline

def upload_data(timeline):
    upload_data_to_mongodb(timeline)


#projects = ('ClickHouse/ClickHouse',12)

projects = config['app_weight']
for current_project, app_weight in projects.items():
    issues = load_issues(current_project)
    timeline = calculate_wrt_timeline(issues, app_weight)
    export_status = upload_data(timeline)

print('Done')
