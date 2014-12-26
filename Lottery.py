# /usr/bin/env python
#coding=utf8
__author__ = 'pitty'

DEBUG = True

import re

try:
    from urllib import request
    print ("import request")
except ImportError:
    try:
        # Python 2.7
        import urllib2 as request
    except ImportError:
        print("Failed to import urllib.request from any known place")

try:
    from urllib import parse as urlparse
    print ("import urlparse")
except ImportError:
    try:
        # Python 2.7
        import urlparse
    except ImportError:
        print("Failed to import urlparse from any known place")

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
    req = request.urlopen(url, timeout=30)
    page = req.read().lower().decode('utf8')
    req.close()
    return etree.HTML(page)


def get_next_page(page):
    xpath_next_page = u"string((//*[@class='pagebar']//span)[3]/parent::a/@href)"
    next_url = page.xpath(xpath_next_page)
    if next_url:
        next_url = urlparse.urljoin(HOST_URL, next_url)
        log("下一页: " + next_url)
        return next_url
    return None


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
            blue2 = None
        v_dict = {'expect': item.xpath(u"string(./td[1])"),
                  'red1': item.xpath(u"string(./td[2]//span[1])"),
                  'red2': item.xpath(u"string(./td[2]//span[2])"),
                  'red3': item.xpath(u"string(./td[2]//span[3])"),
                  'red4': item.xpath(u"string(./td[2]//span[4])"),
                  'red5': item.xpath(u"string(./td[2]//span[5])"),
                  'red6': item.xpath(u"string(./td[2]//span[6])"),
                  'blue1': blue1,
                  'detail': {'sales': re.sub('\D', '', item.xpath(u"string(./td[5])")),
                             'pool': re.sub('\D', '', item.xpath(u"string(./td[6])")),
                             'url': urlparse.urljoin(HOST_URL, item.xpath(u"string(./td[7]/a/@href)"))}}
        if blue2:
            v_dict['blue2'] = blue2
        v_list.append(v_dict)
    log(v_list)
    return v_list


def get_lottery_detail(page):
    xpath_items = u"//tbody//tr"
    items = page.xpath(xpath_items)
    i = 0
    awards1 = get_detail_items(items[i])
    awards1['cases'] = re.sub("\s+", '', page.xpath(u"string(//*[@class='drawright']/div)"))
    i += 1
    awards2 = get_detail_items(items[i])
    if len(items) > 6:
        i += 1
        awards2['plus'] = get_detail_items(items[i])
    i += 1
    awards3 = get_detail_items(items[i])
    i += 1
    awards4 = get_detail_items(items[i])
    i += 1
    awards5 = get_detail_items(items[i])
    i += 1
    awards6 = get_detail_items(items[i])
    v_dict = {'award1': awards1,
              'award2': awards2,
              'award3': awards3,
              'award4': awards4,
              'award5': awards5,
              'award6': awards6}
    log(v_dict)
    return v_dict


def get_detail_items(item):
    count = item.xpath(u"string(./td[2])")
    amount = re.findall("(\d+)", item.xpath(u"string(./td[3])"))
    append = None
    if len(amount) > 1:
        append = amount[1]
    amount = amount[0]
    v_dict = {'count': count,
            'amount': amount}
    if append:
        v_dict['append'] = append
    return v_dict


def get_lottery(url):
    m_page = open_url(url)
    m_list = get_lottery_items(m_page)
    for item in m_list:
        d_page = open_url(item['detail']['url'])
        d_dict = get_lottery_detail(d_page)
        item['detail'] = dict(item['detail'], **d_dict)
    log(m_list)
    m_next_page = get_next_page(m_page)
    if m_next_page:
        get_lottery(m_next_page)

get_lottery(HOST_URL)