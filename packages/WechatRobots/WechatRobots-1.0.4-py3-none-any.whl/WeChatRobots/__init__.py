import json

import requests

class Get():
    def __init__(self, url):
        self._url = url

    def send(self, content, msgtype, ai=None, SSL=False):
        if ai is None:
            ai = []

        if msgtype == "text":
            re = self._sendText(content, ai, SSL)
        elif msgtype == "markdown":
            re = self._sendMarkdown(content, SSL)
        elif msgtype == "news":
            re = self._sendNews(content["title"], content["description"], content["url"], content["picurl"], SSL)
        else:
            re = "请选择正确类型"

        if re == "ok":
            return "完成"
        else:
            return re

    def _sendText(self, text, ai, SSL):
        data = {
            "msgtype": "text",
            "text": {
                "content": text,
                "mentioned_list": ai
            }
        }
        content = json.dumps(data)
        response = requests.post(url=self._url, data=content, verify=SSL)
        returnText = eval(response.text)
        return returnText["errmsg"]

    def _sendMarkdown(self, content, SSL):
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        content = json.dumps(data)
        response = requests.post(url=self._url, data=content, verify=SSL)
        returnText = eval(response.text)
        return returnText["errmsg"]

    def _sendNews(self, title, description, url, picurl, SSL):
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
        response = requests.post(url=self._url, data=content, verify=SSL)
        returnText = eval(response.text)
        return returnText["errmsg"]
