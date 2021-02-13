config = {
    'app_weight': {
        'ClickHouse/ClickHouse': 13,
        'authelia/authelia' : 9,
        'gravitational/teleport' : 17
    },
    'github_severity_list': (
        #(comments_count, Severity)
        (11, 'Critical'),
        (8, 'High'),
        (3, 'Medium'),
        (0, 'Low')

    ),
    'defect_criticality_dict': {
    #{Severity, criticality rate}
        'Critical': 5,
        'High': 2.5,
        'Medium': 1,
        'Low':   0.5
    },
    'fix_time': {
        'Critical': 1,
        'High': 2,
        'Medium': 60,
        'Low': 120
    },

    'mongodb': {
        'host':'localhost',
        'port': 27017,
        'db': 'WRT'
    }
}
