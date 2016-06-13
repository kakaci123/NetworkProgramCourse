import re
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import os
from selenium import webdriver
import argparse

checklist = list()
pagelist = list()


def BrowserSetting():
    cwd = os.getcwd() + '/'
    options = webdriver.ChromeOptions()
    options.add_argument('--lang=en')
    driver = webdriver.Chrome(executable_path=cwd + 'chromedriver',
                              chrome_options=options)
    return driver


def crawler(URL, browser):
    try:
        if URL in pagelist or '.jpg' in URL or '.ppt' in URL or '.pdf' in URL or '.doc' in URL or '.xls' in URL or '.flv' in URL:
            return
        print('{} is crawler'.format(URL))

        global DomainUrl
        RegularText = 'E-mail: (.*?)@cs.ccu.edu.tw'

        browser.get(URL)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        pagelist.append(URL)
        page = browser.page_source.replace('\n', '').replace('<img src="at.png" />', '@')
        m = re.findall(RegularText, page)
        if len(m) != 0:
            for index in m:
                if '<' in index or '>' in index:
                    continue
                if index not in checklist:
                    print(index)
                    checklist.append(index+'@cs.ccu.edu.tw')

        temp = soup.find_all('a')
        for index in temp:
            TempStr = index.attrs['href']
            if 'mailto:' in TempStr or '@' in TempStr:
                TempStr = TempStr.replace('mailto:', '').replace('mail:','')
                if TempStr not in checklist:
                    print(TempStr)
                    checklist.append(TempStr)
            else:
                if 'http' not in TempStr:
                    if TempStr[0] == '/':
                        TempStr = DomainUrl + TempStr[1:]
                    elif TempStr[0] == '?':
                        TempStr = URL.split('?')[0] + TempStr
                    else:
                        TempStr = DomainUrl + TempStr
                    if 'ftype=pdf' not in TempStr and 'ftype=doc' not in TempStr:
                        crawler(TempStr, browser)
                else:
                    if DomainUrl in TempStr:
                        crawler(TempStr, browser)
    except:
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='send and receive UDP locally')
    parser.add_argument('-t', metavar='Target URL', type=str, default='https://www.cs.ccu.edu.tw/',
                        help='Target URL(Default CCU CS)')
    args = parser.parse_args()
    URL=args.t
    #URL = 'https://www.cs.ccu.edu.tw/'
    #URL = 'https://www.cs.ccu.edu.tw/members/teacher.php'
    global DomainUrl
    DomainUrl = "{0.scheme}://{0.netloc}/".format(urlsplit(URL))
    browser = BrowserSetting()
    crawler(URL, browser)
    print('===End of crawler===')
    for index in checklist:
        print(index)
    print('Count={}'.format(len(checklist)))
    browser.close()

DomainUrl = ''
