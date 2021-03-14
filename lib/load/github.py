from github import Github
from collections import OrderedDict
from config import config
import os
from datetime import datetime

#загрузка данных из github
def load_from_github(github_repo, security_labels):
    g = Github(os.environ['github_token'])
    repo = g.get_repo(github_repo)
    issues = repo.get_issues(labels=security_labels, state='all')
    issues = _normolize_data(list(issues),github_repo)
    issues.sort(key=lambda x:x['start_date'])
    return issues

#приведение к универсальному формату
def _normolize_data(issues, github_repo):
    def get_severity_by_comments(issue, dc_table):
        for dc_threshold, severity in dc_table:
            if issue.comments >= dc_threshold:
                return severity

    result = []
    for issue in issues:
        #получаем имя проекта
        project = github_repo.split('/')[1]
        #получаем severity на основе информации о количестве комментариев
        severity = get_severity_by_comments(issue, config['github_severity_list'])

        #если задача находится в статусе open, то в качестве end_date используем текущую на данный день дату
        if issue.state == 'open' or issue.closed_at is None:
            end_date = datetime.now()
        else:
            end_date = issue.closed_at

        result.append(dict( state=issue.state,
                            start_date=issue.created_at,
                            end_date=end_date,
                            severity=severity,
                            project=project,
                            title=issue.title,
                            labelts=issue.labels))


    return result