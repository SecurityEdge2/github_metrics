config = {
    'app_weight': {
        'ClickHouse/ClickHouse': 12,
        'authelia/authelia' : 10,
        'gravitational/teleport' : 13
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
        'Critical': 10,
        'High': 5,
        'Medium': 2,
        'Low':   1
    },
    'mongodb': {
        'host':'localhost',
        'port': 27017,
        'db': 'WRT'
    }
}
