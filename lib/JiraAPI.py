import os
import requests
import json
from pprint import pprint


class JiraAPI:
    BASE_URL = "https://city-mobil.atlassian.net/"
    JIRA_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

    @staticmethod
    def post_request(url: str, data: dict) -> object:
        if not os.path.isfile('tokens/token.jira.txt'):
           raise ValueError('tokens/token.jira.txt file with valid gitlab token required')
        username = "a.voznesenskii@city-mobil.ru"
        token = open('tokens/token.jira.txt', 'r').read()
        url = JiraAPI.BASE_URL + url
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, auth=(username, token), json=data, headers=headers)
        return response


    @staticmethod
    def get_request(url: str) -> object:
        if not os.path.isfile('tokens/token.jira.txt'):
           raise ValueError('tokens/token.jira.txt file with valid gitlab token required')
        username = "a.voznesenskii@city-mobil.ru"
        token = open('tokens/token.jira.txt', 'r').read()
        url = JiraAPI.BASE_URL + url
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.get(url, auth=(username, token), headers=headers)
        return response

    @staticmethod
    def create_issue():
        data = {
            "fields": {
                "project": {"key": "IS"},
                "customfield_10014": "IS-381",
                "summary": "No REST for the Wicked.",
                "description": {
                  "version": 1,
                  "type": "doc",
                  "content": [
                    {
                      "type": "paragraph",
                      "content": [
                        {
                          "type": "text",
                          "text": "Hello "
                        },
                        {
                          "type": "text",
                          "text": "world",
                          "marks": [
                            {
                              "type": "strong"
                            }
                          ]
                        }
                      ]
                    }
                  ]
                },
                "issuetype": {
                    "name": "Баг",
                    "id": 10119
                }
            }
        }
        pprint( json.dumps(data) )
        response = JiraAPI.post_request(url="rest/api/3/issue/", data=data)
        return response

if __name__ ==\
        '__main__':
    JiraAPI.main()