import math
import calendar

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
        issue_wrt = defect_criticality*app_weight
        return dict(wrt=issue_wrt,severity=severity,defect_criticality=defect_criticality,app_weight=app_weight)

    def _is_one_month(date1,date2):
        if date1.strftime('%m-%Y') == date2.strftime('%m-%Y'): return True
        else: return False

    def _is_one_qartar(date1,date2):
        if date1.year != date2.year:
            return False
        if math.ceil(date1.month/3) != math.ceil(date2.month/3):
            return False
        return True

    def _get_last_month_date(date: datetime):
        m, y = date.month, date.year
        _,last_month_date = calendar.monthrange(y,m)
        return datetime(y,m,last_month_date,0,0)

    def _get_last_month_in_qarter(month: int):
        if month >=10:
            return 4
        if month >= 7:
            return 3
        if month >= 4:
            return 2
        return 1

    def _get_last_quarter_date(date):
        m, y = date.month, date.year
        last_month = _get_last_month_in_qarter(m)
        last_date = _get_last_month_date(datetime(y,last_month,1,0,0))
        return datetime(y,last_month,last_date,0,0)

    def _prepare_unit(issue):
        unit = {}
        unit['date'] = issue['start_date']
        unit['project'] = issue['project']
        unit['wrt'] = issue['wrt']
        unit['business_criticality'] = issue['app_weight']
        return unit



    for cur_issue in issues:
        #подсчитываем wrt для конкретного issue
        cur_issue.update(calculate_wrt_for_issue(cur_issue,app_weight,config['defect_criticality_dict']))

    m_timeline = list()
    q_timeline = list()

    prev_issue = issues[0]
    cur_date = prev_issue['start_date']
    cur_wrt_m = prev_issue['wrt']
    cur_wrt_q = prev_issue['wrt']



    if len(issues) == 1:
        m_timeline = prev_issue
        q_timeline = prev_issue
        return m_timeline,q_timeline

    for i, cur_issue in enumerate(issues):
        if i == 0:
            continue

        if _is_one_month(prev_issue['start_date'],cur_issue['start_date']):
            cur_wrt_m += cur_issue['wrt']
        else:
            #save prev month issue
            tmp = prev_issue['start_date']
            prev_issue['start_date'] = prev_issue['start_date'].strftime('%Y-%m')
            prev_issue['wrt'] = cur_wrt_m
            m_timeline.append(_prepare_unit(prev_issue))
            prev_issue['start_date'] = tmp
            #reset wrt sum
            cur_wrt_m = cur_issue['wrt']

        if _is_one_qartar(prev_issue['start_date'], cur_issue['start_date']):
            cur_wrt_q += cur_issue['wrt']
        else:
            q = math.ceil(prev_issue['start_date'].month/3)
            tmp = prev_issue['start_date']
            prev_issue['start_date'] = prev_issue['start_date'].strftime('%Y-') + "Q" + str(q)
            prev_issue['wrt'] = cur_wrt_q
            q_timeline.append(_prepare_unit(prev_issue))
            cur_wrt_q = cur_issue['wrt']
            prev_issue['start_date'] = tmp

        prev_issue = cur_issue
    return m_timeline,q_timeline













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
    while iter_day <= end_date:
        unit = dict(date=iter_day,
                    app_weight=app_weight, drw_1=timedelta(), drw_2=timedelta(), drw_3 = timedelta(),
                    drw_4 = timedelta(), drw_5 = timedelta(), drw_6=timedelta()
                    )
        count = 0
        for issue in issues:
            if issue['start_date'] <= iter_day and iter_day <= issue['end_date']:
                unit['project']  = issue['project']

                fix_time = issue['end_date'] - issue['start_date']
                unit['drw_1'] += fix_time
                unit['drw_2'] += fix_time/fix_time_regulation[issue['severity']]
                unit['drw_3'] += fix_time / fix_time_regulation[issue['severity']]
                unit['drw_4'] += fix_time - timedelta(days=fix_time_regulation[issue['severity']])
                unit['drw_5'] += (fix_time / fix_time_regulation[issue['severity']]) * defect_criticality_dict[issue['severity']] * app_weight
                unit['drw_6'] += (fix_time - timedelta(days=fix_time_regulation[issue['severity']])) * defect_criticality_dict[issue['severity']] * app_weight
                count += 1
        unit['drw_1'] = unit['drw_1'].days
        unit['drw_2'] = unit['drw_2'].days
        unit['drw_3'] = (unit['drw_3'] / count).days
        unit['drw_4'] = unit['drw_4'].days
        unit['drw_5'] = (unit['drw_5'] / count).days
        unit['drw_6'] = (unit['drw_6'] / count).days

        timeline.append(unit)



        iter_day += timedelta(days=1)

    return timeline