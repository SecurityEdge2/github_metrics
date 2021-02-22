import os
import gitlab



from github import Github
from collections import OrderedDict
from config import config
import os
from datetime import datetime

#загрузка данных из github
def load_data_from_github(github_repo,security_labels):
    gitlab.Gitlab(os.environ['gitlab_url'], private_token='gitlab_token')
    return None

#приведение к универсальному формату
def _normolize_data(issues, github_repo):
    return None