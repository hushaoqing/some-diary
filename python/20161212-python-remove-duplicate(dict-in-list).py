# !usr/bin/python
# coding=utf-8

import requests
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


_replace = lambda a:re.subn(r'\[[\d-]*\]', '', a.replace(" ", "").replace("\n", "").replace("\t", "").replace("，", ",").replace("\\", ",").replace("、", ",").strip())[0]
url = "http://baike.baidu.com/item/%E8%BF%98%E7%8F%A0%E6%A0%BC%E6%A0%BC/903367"
res = requests.get(url).content
def getActor(res):
    actorList, roleList = [], []
    ac = []
    soup = BeautifulSoup(res, "html.parser")
    try:
        for data in soup.find_all('li', class_="pages"):
            message = data.find_all("dt")
            for drama in message:
                actorList.append(_replace(drama.get_text()).split("饰")[0].strip())
                roleList.append(_replace(drama.get_text()).split("饰")[1].strip())
        ac = zip(actorList, roleList)
        if not ac:
            for data in soup.find("table", attrs={"log-set-param":"table_view", "class":"cell-module", "nslog":"area"}).find("tbody").find_all("tr")[:-1]:
                roleList.append(_replace(data.find_all("td")[0].get_text()))
                actorList.append(_replace(data.find_all("td")[1].get_text()).replace(";", "/").strip("/"))
            ac = zip(actorList, roleList)
    except:
        pass
    return ac
actor = getActor(res)
# list 内嵌 tuple, tuple 不重复，但tuple中的值重复
def remove_duplicate(actor):
    def merge(kv, index, actor):
        v = []
        for a in kv:
            v.append(a[1])
        actor[index] = (a[0], "/".join(v))
        for f in kv[1:]:
            actor.remove(f)

    for i in actor:
        index = actor.index(i)
        ll = []
        for j in actor:
            if i[0] == j[0]:
                ll.append(j)
        merge(ll, index, actor)
    return actor

for k,v in actor:
    print k,v
print "*" * 30
for a in remove_duplicate(actor):
    print a[0], a[1]

