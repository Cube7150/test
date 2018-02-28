# 나라장터의 어제날짜 기준 입찰 물품을 조회합니다.
# target_string 에 리스트 형태로 추가하시면 목록으로 출력해줍니다.
# cron 에 넣고 메일로 받아보시는 것을 권장합니다.
# pandas 와 BeautifulSoup, requests 를 필요로 합니다.

from requests import session
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import pandas as pd

now = datetime.now()
fromdate = now.strftime("%Y/%m/%d")
todate = (now + timedelta(days=60)).strftime("%Y/%m/%d")

target_string = ['연구', '분자']

ORGURL = "http://www.g2b.go.kr:8101/ep/tbid/tbidList.do?searchType=1&bidSearchType=1&taskClCds=1&bidNm=&searchDtType=1&fromOpenBidDt=&toOpenBidDt=&exceptEnd=Y&radOrgan=1&instNm=&instSearchRangeType=&refNo=&area=&areaNm=&industry=&industryCd=&budget=&budgetCompare=UP&detailPrdnmNo=&detailPrdnm=&procmntReqNo=&intbidYn=&regYn=Y&recordCountPerPage=1000&fromBidDt=" + fromdate + "&toBidDt=" + todate


def iscontained(fullstr, targetlist):
    idx = 0
    for t in targetlist:
        if fullstr.find(t) > -1:
            idx = 1
    return idx == 1


sess = session()
sess.get('http://www.g2b.go.kr/')
RESULT = sess.get(ORGURL)
if RESULT.status_code == 200:
    RAW = RESULT.text
    soup = BeautifulSoup(RAW, 'html.parser')
    TRs = soup.findAll('tr', {'onmouseout': "this.className=''"})

    RAW = None

    tot = list()
    for t in TRs:
        tlist = list()
        for c in t.contents:
            try:
                r = c.text
                tlist.append(r)
            except:
                pass
        tot.append(tlist)

    findlist = list()
    for t in tot:
        if iscontained(t[3], target_string):
            findlist.append(t)

    if len(findlist) > 0:
        html_result = pd.DataFrame(findlist).to_html
    else:
        html_result = '결과가 없습니다.'

# print(html_result)
