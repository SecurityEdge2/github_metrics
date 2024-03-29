from lib.JiraAPI import JiraAPI
from lib.jira_cloud_city import H1Issues
import os
from datetime import datetime
import re
from urllib import parse
business_criticality = {
    '':0
}




def load_all_results():
    start_at=0
    results = list()
    cur_results = 0
    total = 0
    while True:
        filter = '%22Epic+Link%22+%3D+IS-185+ORDER+BY+cf%5B10154%5D+ASC'
        response = JiraAPI.get_request('rest/api/3/search?jql=' + filter + '&startAt={}'.format(start_at) +  "&maxResults=100")
        obj_h1 = H1Issues(response.json())
        json_results = response.json()
        total = json_results['total']
        start_at = start_at + json_results['maxResults']
        results_count = len(json_results['issues'])
        if total <= results_count:
            return obj_h1.results
        results.extend(obj_h1.results)
        cur_results += 100
        if cur_results > total:
            return results




def load_data():
    obj_h1=load_all_results()
    result = _normolize_data(obj_h1)
    return result

#приведение к универсальному формату
def _normolize_data(issues):
    results = list()
    for issue in issues:
        #build target url
        if issue['target_url'] is None:
            print(issue['key'])
            continue
        if issue['target_url'][-1] == '/':
            issue['target_url'] = issue['target_url'][:-1]

        #build project field
        url = parse.urlparse(issue['target_url'])
        if url.netloc == '':
            print(issue['key'])
            continue
        if url.netloc == 'city-mobil.ru':
            if url.path[:10] == '/taxiserv/':
                project = 'city-mobil.ru/taxiserv/'
        else:
            project = url.netloc

        #fix severity
        if issue['priority'] == 'Highest':
            issue['priority'] = 'High'
        if issue['priority'] == 'Lowest':
            issue['priority'] = 'Low'

        results.append(dict(state=issue['state'],
                       start_date=datetime.strptime(issue['created'].split('.')[0], '%Y-%m-%dT%H:%M:%S'),
                       end_date=datetime.strptime(issue['finished'].split('.')[0], '%Y-%m-%dT%H:%M:%S'),
                       severity=issue['priority'],
                       project=project,
                       title=issue['key'],
                       labels=issue['vuln_type'],
                       target_url=issue['target_url']
                      ))
    no_bus_crit = set()
    for result in results:
        if result['target_url'] in business_criticality:
            result['business_criticality'] = business_criticality[result['target_url']]
        else:
            result['business_criticality'] = 6
            no_bus_crit.add(result['target_url'])

    print(no_bus_crit)


    return results
