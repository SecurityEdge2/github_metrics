import math
import calendar
import copy
from collections import Counter
from datetime import datetime,timedelta
from config import config

def _get_timeline_ends(issues):
    # инициализируем переменные
    first_date = (datetime.now() + timedelta(days=1))
    end_date = (datetime.now() - timedelta(days=365 * 30))
    # находим значения для frst_date & last_date
    for issue in issues:
        if issue['start_date'] < first_date:
            first_date = issue['start_date']
        if issue['end_date'] > end_date:
            end_date = issue['end_date']
    return  first_date, end_date



def calculate_wrt_timeline(issues, app_weight):
    def calculate_wrt_for_issue(issue, app_weight, dc_dict):
        severity = issue['severity']
        defect_criticality = dc_dict[severity]
        if app_weight is None:
            app_weight = issue['business_criticality']
        issue_wrt = defect_criticality*app_weight
        return dict(wrt=issue_wrt,severity=severity,defect_criticality=defect_criticality,app_weight=app_weight)

    def _get_m_by_date(date: datetime):
        return "{}-{}".format(date.year, date.month)

    def _get_q_by_date(date: datetime):
        q = math.ceil(date.month/3)
        return "{}-Q{}".format(date.year, q)


    for cur_issue in issues:
        #подсчитываем wrt для конкретного issue
        cur_issue.update(calculate_wrt_for_issue(cur_issue,app_weight,config['defect_criticality_dict']))

    c = Counter()

    for cur_issue in issues:
        cur_issue['date'] = _get_m_by_date(cur_issue['start_date'])
        m = _get_m_by_date(cur_issue['start_date'])
        q = _get_q_by_date(cur_issue['start_date'])
        project = cur_issue['target_url']
        c[ '|'.join((project,'M',m)) ] += cur_issue['wrt']
        c[ '|'.join((project,'q',q)) ] += cur_issue['wrt']

    result = list()
    for header,value in c.items():
        project, date_type, date = header.split('|')
        if value >= 40:
            significant = True
        else:
            significant = False
        result.append(dict(project=project, aggregation_type=date_type, date=date, wrt=value, significant=significant))


    #agregate wrt
    return result













def old(issues, app_weight):

    for issue in issues:
        #подсчитываем wrt для конкретного issue
        issue.update(calculate_wrt_for_issue(issue,app_weight,config['defect_criticality_dict']))

    first_date, end_date = _get_timeline_ends(issues)
    timeline_month = list()
    timeline_quarter = list()
    iter_day = first_date
    #складываем criticality от разных issue в конкретный день
    while iter_day<= end_date:
        #date=iter_day.strftime('%d/%m/%Y')
        m_wrt = 0
        q_wrt = 0
        for issue in issues:

            if issue['start_date'] <= iter_day and iter_day <= issue['end_date']:

                unit = dict(wrt=0, date=iter_day)
                unit['wrt'] = issue['wrt']
                unit['project'] = issue['project']
                unit['app_weight'] = issue['app_weight']
                unit['severity'] = issue['severity']
                timeline.append(unit)
        iter_day += timedelta(days=1)

    return timeline




#drw = Defect Remediation Window
def calculate_drw_timeline(issues,app_weight):
    fix_time_regulation = config['fix_time']
    defect_criticality_dict = config['defect_criticality_dict']
    first_date, end_date = _get_timeline_ends(issues)
    timeline = list()
    iter_day = first_date
    handled_projects = set()
    while iter_day <= end_date:
        unit = dict(date=iter_day,
                    app_weight=app_weight, drw_1=timedelta(), drw_2=timedelta(), drw_3 = timedelta(),
                    drw_4 = timedelta(), drw_5 = timedelta(), drw_6=timedelta()
                    )
        count = 0
        cur_url = None
        for issue in issues:
            if cur_url is None:
                if issues['target_url'] in handled_projects:
                    continue
                else:
                    cur_url = issue['target_url']
            if cur_url != issue['target_url']:
                continue

            cur_project = None
            if issue['start_date'] <= iter_day and iter_day <= issue['end_date']:
                unit['project']  = issue['project']
                if app_weight is None:
                    app_weight = issue['business_criticality']

                fix_time = issue['end_date'] - issue['start_date']
                unit['drw_1'] += fix_time
                unit['drw_2'] += fix_time/fix_time_regulation[issue['severity']]
                unit['drw_3'] += fix_time / fix_time_regulation[issue['severity']]
                unit['drw_4'] += fix_time - timedelta(days=fix_time_regulation[issue['severity']])
                unit['drw_5'] += (fix_time / fix_time_regulation[issue['severity']]) * defect_criticality_dict[issue['severity']] * app_weight
                unit['drw_6'] += (fix_time - timedelta(days=fix_time_regulation[issue['severity']])) * defect_criticality_dict[issue['severity']] * app_weight
                unit['target_url'] = issue['target_url']
                count += 1
        unit['drw_1'] = unit['drw_1'].days
        unit['drw_2'] = unit['drw_2'].days
        unit['drw_3'] = (unit['drw_3'] / count).days
        unit['drw_4'] = unit['drw_4'].days
        unit['drw_5'] = (unit['drw_5'] / count).days
        unit['drw_6'] = (unit['drw_6'] / count).days
        handled_projects.add()

        timeline.append(unit)



        iter_day += timedelta(days=1)

    return timeline