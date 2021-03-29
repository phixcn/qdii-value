import requests
from bs4 import BeautifulSoup
import re

__url = 'http://fundsresearch.investments.hsbc.com.cn/rbwm/Overview.aspx?code={}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}


def lists(fund_id):
    r = requests.get(__url.format(str(fund_id)), headers=headers)
    s = BeautifulSoup(r.content, features='lxml')
    n = s.find(id=re.compile('lbFundNameText')).string
    if n.strip() == '-':
        return None
    d = s.find(id=re.compile('lbPortfolioText')).string
    d = re.search(r"\d{4}-\d{2}-\d{2}", d).group()
    p = s.find(id=re.compile('panelTop10')).find(class_='ms_table')
    if p is None:
        return None
    stock = s.find(id=re.compile('lbStockText')).string[:-1]

    def get_tr(tr):
        td = tr.find_all('td')
        return {
            'code': td[0].string,
            'name': td[1].string,
            'capital': td[2].string,
            'weight': td[3].string
        }
    return {
        "fund_name": n, 
        "last_update": d, 
        "equities": list(map(get_tr, p.table.find_all('tr')))[1:],
        "equities_percent": stock
    }
