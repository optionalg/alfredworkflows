#!/usr/bin/python
# encoding: utf-8

import sys
from workflow import Workflow, web
import datetime

ICON_DEFAULT = 'icon.png'

def today():
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    url = 'http://matchweb.sports.qq.com/kbs/list?from=NBA_PC&columnId=100000&startTime=%s&endTime=%s' % (now,now)
    r = web.get(url)
    r.raise_for_status()

    nbas = []
    data = r.json()
    results = data['data'][now]
    return results

def main(wf):
    
    # 请求数据
    nbas = wf.cached_data('today', today, max_age=60)

    if len(nbas) <= 0:
        wf.add_item(title=u'今天没有比赛', valid=True, icon=ICON_DEFAULT)
    
    # 添加 item 到 workflow 列表
    for nba in nbas:
        tit = '%s (%s) VS %s (%s)' % (nba['leftName'],nba['leftGoal'],nba['rightName'],nba['rightGoal'])
        # sub =  nba['matchDesc'] 
        sub = '%s %s' %(nba['quarter'],nba['quarterTime'])
        weburl = 'http://kbs.sports.qq.com/kbsweb/game.htm?mid=%s' % (nba['mid'])
        matchPeriod = nba['matchPeriod']
        if matchPeriod == '2':
            sub = u'比赛结束'
            weburl = nba['latestNews']['url']
        elif matchPeriod == '0':
            sub = u'比赛开始时间 %s' % (nba['startTime'])

        wf.add_item(title=tit,
                    subtitle=sub,
                    arg=weburl,
                    valid=True,
                    icon=ICON_DEFAULT)
   
    
    wf.send_feedback()
    


if __name__ == '__main__':
    
    wf = Workflow()

    logger = wf.logger

    sys.exit(wf.run(main))