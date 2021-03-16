import math
from collections import Counter
from datetime import datetime,timedelta
from config import config


def calculate_wrt_for_issue(issue, app_weight, dc_dict):
    severity = issue['severity']
    defect_criticality = dc_dict[severity]
    if app_weight is None:
        app_weight = issue['business_criticality']
    issue_wrt = defect_criticality * app_weight
    return dict(wrt=issue_wrt, severity=severity, defect_criticality=defect_criticality, app_weight=app_weight)


def _get_m_by_date(date: datetime):
    return "{}-{}".format(date.year, date.month)


def _get_q_by_date(date: datetime):
    q = math.ceil(date.month / 3)
    return "{}-Q{}".format(date.year, q)




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
    return first_date, end_date


def calculate_wrt_timeline(issues, app_weight=None):
    for cur_issue in issues:
        # подсчитываем wrt для конкретного issue
        cur_issue.update(calculate_wrt_for_issue(cur_issue, app_weight, config['defect_criticality_dict']))

    c = Counter()

    for cur_issue in issues:
        cur_issue['date'] = _get_m_by_date(cur_issue['start_date'])
        m = _get_m_by_date(cur_issue['start_date'])
        q = _get_q_by_date(cur_issue['start_date'])
        project = cur_issue['project']
        c[ '|'.join((project,'M',m)) ] += cur_issue['wrt']
        c[ '|'.join((project,'q',q)) ] += cur_issue['wrt']
        c['|'.join((project, 'M_convergence1', m))] += 1
        c['|'.join((project, 'M_convergence1', _get_m_by_date(cur_issue['end_date'])))] -= 1
        c['|'.join((project, 'Q_convergence1', q))] += 1
        c['|'.join((project, 'Q_convergence1', _get_q_by_date(cur_issue['end_date'])))] -= 1
    result = list()
    for header,value in c.items():
        project, date_type, date = header.split('|')
        if date_type=='M' or date_type=='q':
            if value >= 40:
                significant = True
            else:
                significant = False
        elif date_type=='M_convergence1' or date_type=='Q_convergence1':
            if value >= 2:
                significant = True
            else:
                significant = False
        else:
            print('error_type')
            significant = 'undefind'
        result.append(dict(project=project, aggregation_type=date_type, date=date, wrt=value, significant=significant))

    return result



def calculate_drw_timeline2(issues):
    def _get_timerange(date1,date2):
        cur_day = date1
        while cur_day <=date2:
            yield cur_day
            cur_day += timedelta(days=1)

    fix_time_regulation = config['fix_time']
    first_date, end_date = _get_timeline_ends(issues)
    timeline_counter = Counter()
    iter_day = first_date

    for cur_issue in issues:
        fix_time = cur_issue['end_date'] - cur_issue['start_date']
        for day in _get_timerange(cur_issue['start_date'], cur_issue['end_date']):
            header = '#'.join((cur_issue['project'],day.strftime('%Y-%m-%d')))
            timeline_counter[header + '#wrt1'] += 1
            timeline_counter[header + '#wrt1.2'] += fix_time.days
            timeline_counter[header + '#wrt2'] += 1/fix_time_regulation[cur_issue['severity']]
            timeline_counter[header + '#wrt3'] += 1 / fix_time_regulation[cur_issue['severity']]
            timeline_counter[header + '#wrt4'] += (fix_time - timedelta(days=fix_time_regulation[cur_issue['severity']])).days
            timeline_counter[header + '#wrt5'] += (fix_time.days / fix_time_regulation[cur_issue['severity']]) * cur_issue['wrt']
            timeline_counter[header + '#wrt6'] += (fix_time.days - fix_time_regulation[cur_issue['severity']]) * cur_issue['wrt']
    result_timeline = list()
    for header, value in timeline_counter.most_common():
        project, date, metrics = header.split('#')
        date = datetime.strptime(date, '%Y-%m-%d')
        result_timeline.append(dict(project=project, date=date, metrics=metrics, drw=value, significant=True))
    return result_timeline




