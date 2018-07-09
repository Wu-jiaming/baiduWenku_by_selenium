import requests
import re

html = requests.get('https://wenku.baidu.com/view/37338aebdd36a32d72758152.html?from=search')
content = html.content.decode('gbk')

docType = re.findall(r"docType.*?:.*?\'(.*?)\'\,", content)[0]
print(docType)
title = re.findall(r"title.*?:.*?'(.*?)'", content)[0]
print(title)