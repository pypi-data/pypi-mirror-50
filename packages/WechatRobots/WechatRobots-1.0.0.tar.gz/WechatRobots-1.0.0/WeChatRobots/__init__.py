import json

import requests

class Get():
    def __init__(self, url):
        self.url = url

    def send(self, content, msgtype, ai=None):
        if ai is None:
            ai = []

        if msgtype == "text":
            re = self.sendText(content, ai)
        elif msgtype == "markdown":
            re = self.sendMarkdown(content)
        elif msgtype == "news":
            re = self.sendNews(content["title"], content["description"], content["url"], content["picurl"])
        else:
            re = "请选择正确类型"

        if re == "ok":
            return "完成"
        else:
            return re

    def sendText(self, text, ai):
        data = {
            "msgtype": "text",
            "text": {
                "content": text,
                "mentioned_list": ai
            }
        }
        content = json.dumps(data)
        response = requests.post(url=self.url, data=content)
        returnText = eval(response.text)
        return returnText["errmsg"]

    def sendMarkdown(self, content):
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        content = json.dumps(data)
        response = requests.post(url=self.url, data=content)
        returnText = eval(response.text)
        return returnText["errmsg"]

    def sendNews(self, title, description, url, picurl):
        data = {
            "msgtype": "news",
            "news": {
                "articles": [
                    {
                        "title": title,
                        "description": description,
                        "url": url,
                        "picurl": picurl
                    }
                ]
            }
        }
        content = json.dumps(data)
        response = requests.post(url=self.url, data=content)
        returnText = eval(response.text)
        return returnText["errmsg"]
