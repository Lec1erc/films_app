import re
import requests


class Parser:
    def __init__(self, link):
        r = requests.get(link)
        text = r.text
        self.image = re.findall(r"https://st\..*\.jpg", text)[0]
        self.name = re.findall(r"<h1>.*</h1>", text)[0][4:-5]
        self.description = re.findall(r'"description">.*</div>', text)[0][14:-6]

    def response(self):
        return [self.name, self.description, self.image]
