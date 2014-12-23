# /usr/bin/env python
#coding=utf8
__author__ = 'pitty'

DEBUG = True

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


HOST_URL = 'http://www.cwl.gov.cn/kjxx/ssq/hmhz/'


def log(info):
    if DEBUG:
        print(info)


def open_url(url):
    log("打开：" + url)
    request = urllib.request.urlopen(url, timeout=10)
    page = request.read().lower().decode('utf8')
    request.close()
    return etree.HTML(page)


def get_next_page(page):
    xpath_next_page = u"string(//*[@class='fc_ch1']/parent::a/@href)"
    next_url = urllib.parse.urljoin(HOST_URL, page.xpath(xpath_next_page))
    log("下一页: " + next_url)
    return next_url


def get_lottery_items(page):
    xpath_items = u"//*[@class='hz']//tr"
    items = page.xpath(xpath_items)
    items.pop(0)
    items.pop(0)
    v_list = []
    for item in items:
        blues = re.findall('(\d+)', item.xpath(u"string(./td[3]//span[1])"))
        if len(blues) > 1:
            blue1 = blues[0]
            blue2 = blues[1]
        else:
            blue1 = blues[0]
            blue2 = ''
        v_dict = {'expect': item.xpath(u"string(./td[1])"),
                  'red1': item.xpath(u"string(./td[2]//span[1])"),
                  'red2': item.xpath(u"string(./td[2]//span[2])"),
                  'red3': item.xpath(u"string(./td[2]//span[3])"),
                  'red4': item.xpath(u"string(./td[2]//span[4])"),
                  'red5': item.xpath(u"string(./td[2]//span[5])"),
                  'red6': item.xpath(u"string(./td[2]//span[6])"),
                  'blue1': blue1,
                  'blue2': blue2,
                  'winners': re.sub('\D', '', item.xpath(u"string(./td[4])")),
                  'sales': re.sub('\D', '', item.xpath(u"string(./td[5])")),
                  'pool': re.sub('\D', '', item.xpath(u"string(./td[6])")),
                  'detail': urllib.parse.urljoin(HOST_URL, item.xpath(u"string(./td[7]/a/@href)"))}
        v_list.append(v_dict)
        log(v_dict)
    log(v_list)
    return v_list


m_page = open_url(HOST_URL)
get_lottery_items(m_page)