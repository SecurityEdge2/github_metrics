config = {
    'github_projects': {
        'ClickHouse/ClickHouse': {'business_criticality': 13, 'tags': ['security']},
        'authelia/authelia': {'business_criticality': 9, 'tags': ['security']},
        'gravitational/teleport': {'business_criticality': 17, 'tags': ['security']},
        'rust-lang/rust': {'business_criticality': 5, 'tags': ['A-security']},
        'openshift/origin': {'business_criticality': 7, 'tags': ['area/security']},
        'kubernetes/kubernetes': {'business_criticality': 7, 'tags': ['area/security']},
        'ansible/ansible': {'business_criticality': 14, 'tags': ['security']},
        'dotnet/runtime': {'business_criticality': 12, 'tags': ['Security']},
        'nodejs/node': {'business_criticality': 16, 'tags': ['security']}

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
        'Highest': 2.5,
        'Medium': 1,
        'Low':   0.5,
        'Lowest':   0.5
    },
    'fix_time': {
        'Critical': 1,
        'High': 2,
        'Medium': 60,
        'Low': 120
    },

    'mongodb': {
        'host':'192.168.49.20',
        'port': 27017,
    },
    'services': {
        'github': {
            'enabled': True,
            'upload_db': 'github',
        },
        'jira': {
            'enabled': True,
            'upload_db': 'wrt',
        },
        'metrics': {
            'wrt': True,
            'drw': True
        }
    }
}
