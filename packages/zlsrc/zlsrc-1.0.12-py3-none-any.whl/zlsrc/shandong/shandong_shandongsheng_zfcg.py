import time

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from zlsrc.util.etl import est_html,add_info, est_meta_large




def f1(driver, num):
    locator = (By.XPATH, '(//td[@class="Font9"])[1]/a')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    cnum = driver.find_element_by_xpath('(//td[@class="Font9"])[last()]//font[@color="red"]').text.strip()

    if int(cnum) != num:
        val = driver.find_element_by_xpath('(//td[@class="Font9"])[1]/a').get_attribute('href').rsplit(
            '/', maxsplit=1)[1]

        driver.execute_script("javascript:query({})".format(num))

        locator = (By.XPATH, '(//td[@class="Font9"])[1]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find_all('td', class_='Font9')[:-1]
    for td in div:
        if len(td) == 0:
            continue
        href = td.a['href']
        if 'http' in href:
            href = href
        else:
            href = "http://www.ccgp-shandong.gov.cn" + href
        name = td.a['title']
        td.a.extract()
        ggstart_time = td.get_text().strip()
        tmp = [name, ggstart_time, href]
        data.append(tmp)

    df = pd.DataFrame(data=data)
    df['info'] = None
    return df


def f2(driver):
    locator = (By.XPATH, '(//td[@class="Font9"])[1]/a')
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('(//td[@class="Font9"])[last()]//strong').text
    # print(page)
    total = re.findall('/(\d+)', page)[0]
    total = int(total)

    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    WebDriverWait(driver, 20).until(lambda driver: len(driver.current_url) > 10)

    if '500' in driver.title:
        return '500'

    driver.get(url)

    locator = (By.XPATH, '(//td[@bgcolor="#FFFFFF"])[3][string-length()>50]')

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

    try:
        rame = driver.find_element_by_xpath('//td[@class="aa"]/iframe')
        driver.switch_to.frame(rame)
        locator = (By.XPATH, '//body[string-length()>100]')
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
        mark = 0
    except:
        mark = 1

    before = len(driver.page_source)
    time.sleep(0.1)
    after = len(driver.page_source)
    i = 0
    while before != after:
        before = len(driver.page_source)
        time.sleep(0.1)
        after = len(driver.page_source)
        i += 1
        if i > 5: break

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')

    driver.switch_to.default_content()

    if mark == 1:
        div = soup.find_all('td', attrs={'bgcolor': '#FFFFFF'})[2].parent.parent

    else:
        div1 = soup.find('body')
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        div2 = soup.find_all('td', attrs={'bgcolor': '#FFFFFF'})[2].parent.parent
        div = BeautifulSoup(str(div1) + str(div2), 'html.parser')

    if div == None:
        raise ValueError('div is None')

    return div

data = [
    #
    ["zfcg_zhaobiao_diqu1_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp?colcode=0301",
     ['name', 'ggstart_time', 'href', 'info'], add_info(f1, {"diqu": "省直"}), f2],
    ["zfcg_zhaobiao_diqu2_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp?colcode=0303",
     ['name', 'ggstart_time', 'href', 'info'], add_info(f1, {"diqu": "市县"}), f2],
    ["zfcg_zhongbiao_diqu1_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp?colcode=0302",
     ['name', 'ggstart_time', 'href', 'info'], add_info(f1, {"diqu": "省直"}), f2],
    ["zfcg_zhongbiao_diqu2_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp?colcode=0304",
     ['name', 'ggstart_time', 'href', 'info'], add_info(f1, {"diqu": "市县"}), f2],
    ["zfcg_biangeng_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp?colcode=0305",
     ['name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["zfcg_liubiao_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp?colcode=0306",
     ['name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["zfcg_zgys_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp?colcode=0307",
     ['name', 'ggstart_time', 'href', 'info'], f1, f2],
    #
    ["zfcg_yucai_diqu1_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/listneedall.jsp",
     ['name', 'ggstart_time', 'href', 'info'], add_info(f1, {"diqu": "省直"}), f2],
    ["zfcg_yanshou_diqu1_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/listchkall.jsp",
     ['name', 'ggstart_time', 'href', 'info'], add_info(f1, {"diqu": "省直"}), f2],
    ["zfcg_gqita_dingdian_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/listcontractall.jsp?contractType=2",
     ['name', 'ggstart_time', 'href', 'info'], add_info(f1, {"tag": "协议供货|定点采购"}), f2],
    ["zfcg_yucai_diqu2_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelallshow.jsp?colcode=2504",
     ['name', 'ggstart_time', 'href', 'info'], add_info(f1, {"diqu": "市县"}), f2],
    ["zfcg_yanshou_diqu2_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelallshow.jsp?colcode=2506",
     ['name', 'ggstart_time', 'href', 'info'], add_info(f1, {"diqu": "市县"}), f2],

    #
    ["zfcg_gqita_jinkou_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp?colcode=2101",
     ['name', 'ggstart_time', 'href', 'info'], add_info(f1, {"tag": "进口产品"}), f2],
    ["zfcg_dyly_diqu1_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp?colcode=2102",
     ['name', 'ggstart_time', 'href', 'info'], add_info(f1, {"diqu": "省直"}), f2],
    ["zfcg_gqita_ppp_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp?colcode=2103",
     ['name', 'ggstart_time', 'href', 'info'], add_info(f1, {"tag": "PPP项目"}), f2],
    ["zfcg_dyly_diqu2_gg", "http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp?colcode=2106",
     ['name', 'ggstart_time', 'href', 'info'], add_info(f1, {"diqu": "市县"}), f2],

]


def work(conp, **args):
    est_meta_large(conp, data=data, diqu="山东省", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    conp = ["postgres", "since2015", "192.168.3.171", "lch", "shandong_shandong"]

    work(conp=conp, pageloadtime=60, num=20)
