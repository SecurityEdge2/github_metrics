config = {
    'app_weight': {
        'ClickHouse/ClickHouse': 12,
        'authelia/authelia' : 10,
        'gravitational/teleport' : 13
    },
    'defect_criticality': (
    #(count_comments, criticality)
        (11, 10),  # 12-infitly - Critical
        (8, 5),  # 9-11 -Hight
        (3, 2),  # 4-8  - medium
        (0,   1)  #0-3  - low
    )
}
