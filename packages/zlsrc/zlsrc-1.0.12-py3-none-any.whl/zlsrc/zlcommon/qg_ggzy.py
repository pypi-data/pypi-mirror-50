import random
import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from zlsrc.util.etl import est_html, est_meta, add_info, est_meta_large



# 省平台工程建设
def s_gcjs_zb(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle']")
        fbsj = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text.strip()
        if '近三月' not in fbsj:
            driver.find_element_by_xpath("//li[@id='choose_time_05']").click()
            locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle'][contains(string(), '近三月')]")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        sjly = driver.find_element_by_xpath("//li[contains(@id, 'choose_source') and @class='toggle']").text.strip()
        if '省平台' not in sjly:
            driver.find_element_by_xpath("//li[@id='choose_source_1']").click()
        yw = driver.find_element_by_xpath("//li[contains(@id, 'choose_classify') and @class='toggle']").text.strip()
        if '工程建设' not in yw:
            driver.find_element_by_xpath("//li[@id='choose_classify_01']").click()
        xx = driver.find_element_by_xpath("//li[contains(@id, 'choose_stage') and @class='toggle']").text.strip()
        if '招标/资审公告' not in xx:
            driver.find_element_by_xpath("//li[@id='choose_stage_0101']").click()
        locator = (By.XPATH, "//li[contains(@id, 'choose_stage') and @class='toggle'][contains(string(), '资审公告')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(2)
        driver.execute_script('cmd_find();')
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'block')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'none')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='toview']/div[1]//a")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

def s_gcjs_kb(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle']")
        fbsj = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text.strip()
        if '近三月' not in fbsj:
            driver.find_element_by_xpath("//li[@id='choose_time_05']").click()
            locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle'][contains(string(), '近三月')]")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        sjly = driver.find_element_by_xpath("//li[contains(@id, 'choose_source') and @class='toggle']").text.strip()
        if '省平台' not in sjly:
            driver.find_element_by_xpath("//li[@id='choose_source_1']").click()
        yw = driver.find_element_by_xpath("//li[contains(@id, 'choose_classify') and @class='toggle']").text.strip()
        if '工程建设' not in yw:
            driver.find_element_by_xpath("//li[@id='choose_classify_01']").click()
        xx = driver.find_element_by_xpath("//li[contains(@id, 'choose_stage') and @class='toggle']").text.strip()
        if '开标记录' not in xx:
            driver.find_element_by_xpath("//li[@id='choose_stage_0102']").click()
        locator = (By.XPATH, "//li[contains(@id, 'choose_stage') and @class='toggle'][contains(string(), '开标记录')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(2)
        driver.execute_script('cmd_find();')
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'block')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'none')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='toview']/div[1]//a")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

def s_gcjs_zhongb(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle']")
        fbsj = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text.strip()
        if '近三月' not in fbsj:
            driver.find_element_by_xpath("//li[@id='choose_time_05']").click()
            locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle'][contains(string(), '近三月')]")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        sjly = driver.find_element_by_xpath("//li[contains(@id, 'choose_source') and @class='toggle']").text.strip()
        if '省平台' not in sjly:
            driver.find_element_by_xpath("//li[@id='choose_source_1']").click()
        yw = driver.find_element_by_xpath("//li[contains(@id, 'choose_classify') and @class='toggle']").text.strip()
        if '工程建设' not in yw:
            driver.find_element_by_xpath("//li[@id='choose_classify_01']").click()
        xx = driver.find_element_by_xpath("//li[contains(@id, 'choose_stage') and @class='toggle']").text.strip()
        if '交易结果公示' not in xx:
            driver.find_element_by_xpath("//li[@id='choose_stage_0104']").click()
        locator = (By.XPATH, "//li[contains(@id, 'choose_stage') and @class='toggle'][contains(string(), '交易结果公示')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(2)
        driver.execute_script('cmd_find();')
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'block')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'none')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='toview']/div[1]//a")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

def s_gcjs_wjcq(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle']")
        fbsj = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text.strip()
        if '近三月' not in fbsj:
            driver.find_element_by_xpath("//li[@id='choose_time_05']").click()
            locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle'][contains(string(), '近三月')]")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        sjly = driver.find_element_by_xpath("//li[contains(@id, 'choose_source') and @class='toggle']").text.strip()
        if '省平台' not in sjly:
            driver.find_element_by_xpath("//li[@id='choose_source_1']").click()
        yw = driver.find_element_by_xpath("//li[contains(@id, 'choose_classify') and @class='toggle']").text.strip()
        if '工程建设' not in yw:
            driver.find_element_by_xpath("//li[@id='choose_classify_01']").click()
        xx = driver.find_element_by_xpath("//li[contains(@id, 'choose_stage') and @class='toggle']").text.strip()
        if '资审文件澄清' not in xx:
            driver.find_element_by_xpath("//li[@id='choose_stage_0105']").click()
        locator = (By.XPATH, "//li[contains(@id, 'choose_stage') and @class='toggle'][contains(string(), '资审文件澄清')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(2)
        driver.execute_script('cmd_find();')
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'block')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'none')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='toview']/div[1]//a")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

def s_gcjs_zsjg(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle']")
        fbsj = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text.strip()
        if '近三月' not in fbsj:
            driver.find_element_by_xpath("//li[@id='choose_time_05']").click()
            locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle'][contains(string(), '近三月')]")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        sjly = driver.find_element_by_xpath("//li[contains(@id, 'choose_source') and @class='toggle']").text.strip()
        if '省平台' not in sjly:
            driver.find_element_by_xpath("//li[@id='choose_source_1']").click()
        yw = driver.find_element_by_xpath("//li[contains(@id, 'choose_classify') and @class='toggle']").text.strip()
        if '工程建设' not in yw:
            driver.find_element_by_xpath("//li[@id='choose_classify_01']").click()
        xx = driver.find_element_by_xpath("//li[contains(@id, 'choose_stage') and @class='toggle']").text.strip()
        if '资格预审结果' not in xx:
            driver.find_element_by_xpath("//li[@id='choose_stage_0106']").click()
        locator = (By.XPATH, "//li[contains(@id, 'choose_stage') and @class='toggle'][contains(string(), '资格预审结果')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(2)
        driver.execute_script('cmd_find();')
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'block')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'none')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='toview']/div[1]//a")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

# 省平台政府采购
def s_zfcg_zb(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle']")
        fbsj = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text.strip()
        if '近三月' not in fbsj:
            driver.find_element_by_xpath("//li[@id='choose_time_05']").click()
            locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle'][contains(string(), '近三月')]")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        sjly = driver.find_element_by_xpath("//li[contains(@id, 'choose_source') and @class='toggle']").text.strip()
        if '省平台' not in sjly:
            driver.find_element_by_xpath("//li[@id='choose_source_1']").click()
        yw = driver.find_element_by_xpath("//li[contains(@id, 'choose_classify') and @class='toggle']").text.strip()
        if '政府采购' not in yw:
            driver.find_element_by_xpath("//li[@id='choose_classify_02']").click()
        xx = driver.find_element_by_xpath("//li[contains(@id, 'choose_stage') and @class='toggle']").text.strip()
        if '采购' not in xx:
            driver.find_element_by_xpath("//li[@id='choose_stage_0201']").click()
        locator = (By.XPATH, "//li[contains(@id, 'choose_stage') and @class='toggle'][contains(string(), '采购')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(2)
        driver.execute_script('cmd_find();')
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'block')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'none')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='toview']/div[1]//a")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

def s_zfcg_zhongb(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle']")
        fbsj = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text.strip()
        if '近三月' not in fbsj:
            driver.find_element_by_xpath("//li[@id='choose_time_05']").click()
            locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle'][contains(string(), '近三月')]")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        sjly = driver.find_element_by_xpath("//li[contains(@id, 'choose_source') and @class='toggle']").text.strip()
        if '省平台' not in sjly:
            driver.find_element_by_xpath("//li[@id='choose_source_1']").click()
        yw = driver.find_element_by_xpath("//li[contains(@id, 'choose_classify') and @class='toggle']").text.strip()
        if '政府采购' not in yw:
            driver.find_element_by_xpath("//li[@id='choose_classify_02']").click()
        xx = driver.find_element_by_xpath("//li[contains(@id, 'choose_stage') and @class='toggle']").text.strip()
        if '中标公告' not in xx:
            driver.find_element_by_xpath("//li[@id='choose_stage_0202']").click()
        locator = (By.XPATH, "//li[contains(@id, 'choose_stage') and @class='toggle'][contains(string(), '中标公告')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(2)
        driver.execute_script('cmd_find();')
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'block')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'none')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='toview']/div[1]//a")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

def s_zfcg_biangeng(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle']")
        fbsj = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text.strip()
        if '近三月' not in fbsj:
            driver.find_element_by_xpath("//li[@id='choose_time_05']").click()
            locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle'][contains(string(), '近三月')]")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        sjly = driver.find_element_by_xpath("//li[contains(@id, 'choose_source') and @class='toggle']").text.strip()
        if '省平台' not in sjly:
            driver.find_element_by_xpath("//li[@id='choose_source_1']").click()
        yw = driver.find_element_by_xpath("//li[contains(@id, 'choose_classify') and @class='toggle']").text.strip()
        if '政府采购' not in yw:
            driver.find_element_by_xpath("//li[@id='choose_classify_02']").click()
        xx = driver.find_element_by_xpath("//li[contains(@id, 'choose_stage') and @class='toggle']").text.strip()
        if '更正事项' not in xx:
            driver.find_element_by_xpath("//li[@id='choose_stage_0204']").click()
        locator = (By.XPATH, "//li[contains(@id, 'choose_stage') and @class='toggle'][contains(string(), '更正事项')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(2)
        driver.execute_script('cmd_find();')
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'block')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'none')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='toview']/div[1]//a")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

# 省平台药品采购
def s_yiliao_zb(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle']")
        fbsj = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text.strip()
        if '近三月' not in fbsj:
            driver.find_element_by_xpath("//li[@id='choose_time_05']").click()
            locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle'][contains(string(), '近三月')]")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        sjly = driver.find_element_by_xpath("//li[contains(@id, 'choose_source') and @class='toggle']").text.strip()
        if '省平台' not in sjly:
            driver.find_element_by_xpath("//li[@id='choose_source_1']").click()
        yw = driver.find_element_by_xpath("//li[contains(@id, 'choose_classify') and @class='toggle']").text.strip()
        if '药品采购' not in yw:
            driver.find_element_by_xpath("//li[@id='choose_classify_23']").click()
        xx = driver.find_element_by_xpath("//li[contains(@id, 'choose_stage') and @class='toggle']").text.strip()
        if '交易公告' not in xx:
            driver.find_element_by_xpath("//li[@id='choose_stage_2302']").click()
        locator = (By.XPATH, "//li[contains(@id, 'choose_stage') and @class='toggle'][contains(string(), '交易公告')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(2)
        driver.execute_script('cmd_find();')
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'block')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'none')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='toview']/div[1]//a")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

# 省平台其他采购
def s_qita_zb(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle']")
        fbsj = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text.strip()
        if '近三月' not in fbsj:
            driver.find_element_by_xpath("//li[@id='choose_time_05']").click()
            locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle'][contains(string(), '近三月')]")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        sjly = driver.find_element_by_xpath("//li[contains(@id, 'choose_source') and @class='toggle']").text.strip()
        if '省平台' not in sjly:
            driver.find_element_by_xpath("//li[@id='choose_source_1']").click()
        yw = driver.find_element_by_xpath("//li[contains(@id, 'choose_classify') and @class='toggle']").text.strip()
        if '其他' not in yw:
            driver.find_element_by_xpath("//li[@id='choose_classify_90']").click()
        xx = driver.find_element_by_xpath("//li[contains(@id, 'choose_stage') and @class='toggle']").text.strip()
        if '交易公告' not in xx:
            driver.find_element_by_xpath("//li[@id='choose_stage_9001']").click()
        locator = (By.XPATH, "//li[contains(@id, 'choose_stage') and @class='toggle'][contains(string(), '交易公告')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(2)
        driver.execute_script('cmd_find();')
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'block')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'none')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='toview']/div[1]//a")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

def s_qita_zhongb(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle']")
        fbsj = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text.strip()
        if '近三月' not in fbsj:
            driver.find_element_by_xpath("//li[@id='choose_time_05']").click()
            locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle'][contains(string(), '近三月')]")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        sjly = driver.find_element_by_xpath("//li[contains(@id, 'choose_source') and @class='toggle']").text.strip()
        if '省平台' not in sjly:
            driver.find_element_by_xpath("//li[@id='choose_source_1']").click()
        yw = driver.find_element_by_xpath("//li[contains(@id, 'choose_classify') and @class='toggle']").text.strip()
        if '其他' not in yw:
            driver.find_element_by_xpath("//li[@id='choose_classify_90']").click()
        xx = driver.find_element_by_xpath("//li[contains(@id, 'choose_stage') and @class='toggle']").text.strip()
        if '成交公示' not in xx:
            driver.find_element_by_xpath("//li[@id='choose_stage_9002']").click()
        locator = (By.XPATH, "//li[contains(@id, 'choose_stage') and @class='toggle'][contains(string(), '成交公示')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(2)
        driver.execute_script('cmd_find();')
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'block')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'none')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='toview']/div[1]//a")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

# 央企招投标工程建设
def y_gcjs_zb(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle']")
        fbsj = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text.strip()
        if '近三月' not in fbsj:
            driver.find_element_by_xpath("//li[@id='choose_time_05']").click()
            locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle'][contains(string(), '近三月')]")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        sjly = driver.find_element_by_xpath("//li[contains(@id, 'choose_source') and @class='toggle']").text.strip()
        if '央企招投标' not in sjly:
            driver.find_element_by_xpath("//li[@id='choose_source_2']").click()

        yw = driver.find_element_by_xpath("//li[contains(@id, 'choose_classify') and @class='toggle']").text.strip()
        if '工程建设' not in yw:
            driver.find_element_by_xpath("//li[@id='choose_classify_01']").click()

        xx = driver.find_element_by_xpath("//li[contains(@id, 'choose_stage') and @class='toggle']").text.strip()
        if '招标/资审公告' not in xx:
            driver.find_element_by_xpath("//li[@id='choose_stage_0101']").click()

        locator = (By.XPATH, "//li[contains(@id, 'choose_stage') and @class='toggle'][contains(string(), '资审公告')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(2)
        driver.execute_script('cmd_find();')
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'block')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'none')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='toview']/div[1]//a")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap

def y_gcjs_zhongb(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle']")
        fbsj = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text.strip()
        if '近三月' not in fbsj:
            driver.find_element_by_xpath("//li[@id='choose_time_05']").click()
            locator = (By.XPATH, "//li[contains(@id, 'choose_time') and @class='toggle'][contains(string(), '近三月')]")
            WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        sjly = driver.find_element_by_xpath("//li[contains(@id, 'choose_source') and @class='toggle']").text.strip()
        if '央企招投标' not in sjly:
            driver.find_element_by_xpath("//li[@id='choose_source_2']").click()

        yw = driver.find_element_by_xpath("//li[contains(@id, 'choose_classify') and @class='toggle']").text.strip()
        if '工程建设' not in yw:
            driver.find_element_by_xpath("//li[@id='choose_classify_01']").click()

        xx = driver.find_element_by_xpath("//li[contains(@id, 'choose_stage') and @class='toggle']").text.strip()
        if '交易结果公示' not in xx:
            driver.find_element_by_xpath("//li[@id='choose_stage_0104']").click()

        locator = (By.XPATH, "//li[contains(@id, 'choose_stage') and @class='toggle'][contains(string(), '交易结果公示')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(2)
        driver.execute_script('cmd_find();')
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'block')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'none')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='toview']/div[1]//a")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        return f(*krg)
    return wrap



def f1(driver, num):
    locator = (By.XPATH, "//div[@id='toview']/div[last()]//a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # url = driver.current_url
    locator = (By.XPATH, "//b[@id='topRight']")
    snum = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    cnum = int(re.findall(r'(\d+)/', snum)[0])

    if num != cnum:
        val = driver.find_element_by_xpath("//div[@id='toview']/div[last()]//a").get_attribute('href')[-40:]
        driver.execute_script('javascript:getList({})'.format(num))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'block')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='filter' and contains(@style, 'none')]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@id='toview']/div[last()]//a[not(contains(@href,'%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    data = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', id='toview')
    lis = div.find_all('div', class_='publicont')
    for tr in lis:
        info = {}
        a = tr.h4.find('a')
        try:
            name = a['title']
        except:
            name = a.text.strip()
        ggstart_time = tr.h4.find('span', class_='span_o').text.strip()
        link = a['href']
        if 'http' in link:
            href = link
        else:
            href = 'http://www.ggzy.gov.cn' + link
        p = tr.find('p', class_='p_tw')
        try:
            diqu = p.find_all('span', class_='span_on')[0].text.strip()
            if diqu: info['diqu'] = diqu
        except:pass
        try:
            laiyuan = p.find_all('span', class_='span_on')[1].text.strip()
            if laiyuan: info['laiyuan'] = laiyuan
        except:pass
        try:
            ywlx = p.find_all('span', class_='span_on')[2].text.strip()
            if ywlx: info['ywlx'] = ywlx
        except:pass
        try:
            xxlx = p.find_all('span', class_='span_on')[3].text.strip()
            if xxlx: info['xxlx'] = xxlx
        except:pass
        try:
            hangye = p.find_all('span', class_='span_on')[4].text.strip()
            if hangye: info['hangye'] = hangye
        except:pass
        if info:
            info = json.dumps(info, ensure_ascii=False)
        else:
            info = None
        tmp = [name, ggstart_time, href, info]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df



def f2(driver):
    locator = (By.XPATH, "//b[@id='topRight']")
    txt = WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator)).text
    total_page = re.findall('/(\d+)', txt)[0]
    driver.quit()
    return int(total_page)



def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, "//div[@class='fully_toggle_cont' and (contains(@style, 'block'))]")
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(locator))
    val = driver.find_element_by_xpath("//div[@class='fully_toggle_cont' and (contains(@style, 'block'))]").text.strip()
    if '暂无数据' in val:
        return 404
    name1 = driver.find_element_by_xpath('//iframe[contains(@id, "iframe")]')
    driver.switch_to.frame(name1)
    if '无文本内容' in str(driver.page_source):
        return 404
    locator = (By.XPATH, "//div[@class='detail'][string-length()>40]")
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(locator))
    before = len(driver.page_source)
    time.sleep(0.5)
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
    div = soup.find('body')
    return div


data = [
    ["gcjs_zhaobiao_sheng_gg",
     "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
     ["name", "ggstart_time", "href", "info"], s_gcjs_zb(f1), s_gcjs_zb(f2)],

    ["gcjs_kaibiao_sheng_gg",
     "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
     ["name", "ggstart_time", "href", "info"], s_gcjs_kb(f1), s_gcjs_kb(f2)],

    ["gcjs_zhongbiao_sheng_gg",
     "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
     ["name", "ggstart_time", "href", "info"], s_gcjs_zhongb(f1), s_gcjs_zhongb(f2)],

    ["gcjs_gqita_cheng_sheng_gg",
     "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
     ["name", "ggstart_time", "href", "info"], s_gcjs_wjcq(f1), s_gcjs_wjcq(f2)],

    ["gcjs_zsjg_sheng_gg",
     "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
     ["name", "ggstart_time", "href", "info"], s_gcjs_zsjg(f1), s_gcjs_zsjg(f2)],

    ["zfcg_zhaobiao_sheng_gg",
     "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
     ["name", "ggstart_time", "href", "info"], s_zfcg_zb(f1), s_zfcg_zb(f2)],

    ["zfcg_zhongbiao_sheng_gg",
     "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
     ["name", "ggstart_time", "href", "info"], s_zfcg_zhongb(f1), s_zfcg_zhongb(f2)],

    ["zfcg_biangeng_sheng_gg",
     "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
     ["name", "ggstart_time", "href", "info"], s_zfcg_biangeng(f1), s_zfcg_biangeng(f2)],

    ["yiliao_zhaobiao_sheng_gg",
     "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
     ["name", "ggstart_time", "href", "info"], s_yiliao_zb(f1), s_yiliao_zb(f2)],

    ["jqita_zhaobiao_sheng_gg",
     "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
     ["name", "ggstart_time", "href", "info"], s_qita_zb(f1), s_qita_zb(f2)],

    ["jqita_zhongbiao_sheng_gg",
     "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
     ["name", "ggstart_time", "href", "info"], s_qita_zhongb(f1), s_qita_zhongb(f2)],

    ["gcjs_zhaobiao_yangqi_gg",
     "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
     ["name", "ggstart_time", "href", "info"], y_gcjs_zb(f1), y_gcjs_zb(f2)],

    ["gcjs_zhongbiao_yangqi_gg",
     "http://deal.ggzy.gov.cn/ds/deal/dealList.jsp",
     ["name", "ggstart_time", "href", "info"], y_gcjs_zhongb(f1), y_gcjs_zhongb(f2)],
]


def work(conp, **args):
    est_meta_large(conp, data=data, diqu="全国公共资源", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "zlest", "qg_ggzy"])


    # for d in data[2:]:
    #     driver=webdriver.Chrome()
    #     url=d[1]
    #     print(url)
    #     driver.get(url)
    #     df = d[-1](driver)
    #     print(df)
    #     driver = webdriver.Chrome()
    #     driver.get(url)
    #
    #     df=d[-2](driver, 12)
    #     print(df.values)
    #     for f in df[2].values:
    #         d = f3(driver, f)
    #         print(d)


