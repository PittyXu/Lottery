# /usr/bin/env python
#coding=utf8
__author__ = 'pitty'

import urllib.request
import urllib.parse
import re

try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")

DEBUG = True
HOST_URL = 'http://www.cwl.gov.cn/kjxx/ssq/hmhz/'


def log(info):
    if DEBUG:
        print(info)

request = urllib.request.urlopen(HOST_URL, timeout=10)
mPage = request.read().lower().decode('utf8')
mPage = etree.HTML(mPage)
XPATH_NEXT_PAGE = u"string(//*[@class='fc_ch1']/parent::a/@href)"
next_url = urllib.parse.urlparse(HOST_URL, mPage.xpath(XPATH_NEXT_PAGE))
log("下一页: " + next_url.__str__())
XPATH_ITEMS = u"//*[@class='hz']//tr"
items = mPage.xpath(XPATH_ITEMS)
items.pop(0)
items.pop(0)
for item in items:
    expect = item.xpath(u"string(./td[1])")
    openCode1 = item.xpath(u"string(./td[2]//span[1])")
    openCode2 = item.xpath(u"string(./td[2]//span[2])")
    openCode3 = item.xpath(u"string(./td[2]//span[3])")
    openCode4 = item.xpath(u"string(./td[2]//span[4])")
    openCode5 = item.xpath(u"string(./td[2]//span[5])")
    openCode6 = item.xpath(u"string(./td[2]//span[6])")
    openCode7 = item.xpath(u"string(./td[3]//span[1])")
    openCode8 = ''
    openCodes = re.split('(\d+)', openCode7)
    if len(openCodes) > 1:
        openCode7 = openCodes[0]
        openCode8 = openCodes[2]
    winners = re.sub('\D', '', item.xpath(u"string(./td[4])"))
    salesAmount = re.sub('\D', '', item.xpath(u"string(./td[5])"))
    prizePool = re.sub('\D', '', item.xpath(u"string(./td[6])"))
    detail = urllib.parse.urlparse(HOST_URL, item.xpath(u"string(./td[7]/a/@href)"))
    log(expect + ' code: ' + openCode1 + ',' + openCode2 + ',' + openCode3 + ',' + openCode4 + ','
        + openCode5 + ',' + openCode6 + ',' + openCode7 + ',' + openCode8 + ' winners: ' + winners
        + winners + ' sales: ' + salesAmount + ' pool: ' + prizePool + ' detail: ' + detail.__str__())
request.close()