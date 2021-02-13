config = {
    'app_weight': {
        'ClickHouse/ClickHouse': (13,'security'),
        'authelia/authelia' : (9,'security'),
        'gravitational/teleport' : (17,'security'),
        'rust-lang/rust': (5,'A-security'),
        'openshift/origin': (7,'area/security'),
        'kubernetes/kubernetes': (7,'area/security '),
        'ansible/ansible': (14, 'security'),
        'dotnet/runtime': (12,'Security'),
        'nodejs/node': (16,'security')

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
