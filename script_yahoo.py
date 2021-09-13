import zipfile
from app import *
import pandas as pd
import json
import threading
import subprocess
from multiprocessing import Process
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
import random
from selenium.webdriver.chrome.options import Options as c_Options
import sys , os
import psutil
from selenium.webdriver.firefox.options import Options as f_Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import schedule
from apscheduler.schedulers.blocking import BlockingScheduler
from flask_apscheduler import APScheduler


start_time = time.time()
username = 'SALMAN ELKABIBI'
global PATH_chrome, PATH_firefox, PATH_comodo

PATH_chrome = ".\\chrome_driver\\chromedriver.exe"
PATH_firefox = ".\\firefox_driver\\geckodriver.exe"
PATH_comodo = ".\\firefox_driver\\geckodriver.exe"


def login_yahoo(email, password, driver):
    try:
        print("[Yahoo] ===> logging in ")
        driver.get(
            "https://login.yahoo.com/?.src=ym&pspid=159600001&activity=mail-direct&.lang=fr-FR&.intl=fr&.done=https%3A%2F%2Fmail.yahoo.com%2Fd%2Ffolders%2F1")
        # driver.get("https://myip.com")
        e = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='username']")))
        e.send_keys(email)
        time.sleep(random.uniform(1,2))
        e.send_keys(Keys.RETURN)

        time.sleep(random.uniform(2,3))
        p = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='password']")))
        p.send_keys(password)
        time.sleep(random.uniform(1,2))
        p.send_keys(Keys.RETURN)
    except Exception as e:
        print(e)
        driver.save_screenshot(".\\screenshots\\login_errors\\" + email + ".png")


def archive_yahoo(driver,subject):
    print('[Yahoo] Archive')

    archiver = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Archiver')]")))
    time.sleep(random.uniform(2,3))
    ActionChains(driver).move_to_element(archiver).click(archiver).perform()


def mark_as_not_spam_yahoo(driver,subject):
    print('[Yahoo] Spam to Inbox')

    select_all = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@data-test-id='checkbox']")))
    time.sleep(random.uniform(2,3))
    ActionChains(driver).move_to_element(select_all).click(select_all).perform()

    to_inbox = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Marquer comme non spam']")))
    ActionChains(driver).move_to_element(to_inbox).click(to_inbox).perform()

    print('[Yahoo] Spam to Inbox : Done')

def filter_as_inbox_yahoo(driver,subject):
    print('[Yahoo] Filter As inbox')

    others = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Autres']")))
    print(others)
    ActionChains(driver).move_to_element(others).click(others).perform()
    time.sleep(random.uniform(2,3))
    filter = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Filtrer les messages')]")))
    ActionChains(driver).move_to_element(filter).click(filter).perform()
    time.sleep(random.uniform(2,3))
    choose = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Sélectionnez un dossier')]")))
    ActionChains(driver).move_to_element(choose).click(choose).perform()
    time.sleep(random.uniform(2,3))
    inbox = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Boîte récept.')]")))
    ActionChains(driver).move_to_element(inbox).click(inbox).perform()
    time.sleep(random.uniform(2,3))
    register = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Enregistrer')]")))
    ActionChains(driver).move_to_element(register).click(register).perform()


def add_filter_yahoo(driver,subject,domains):
    print('[Yahoo] Add Filter')
    settings = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Menu Paramètres']")))
    ActionChains(driver).move_to_element(settings).click(settings).perform()
    time.sleep(random.uniform(2,3))
    other_settings = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Autres paramètres')]")))
    ActionChains(driver).move_to_element(other_settings).click(other_settings).perform()
    time.sleep(random.uniform(2,3))
    filters = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[@title='Filtres']")))
    ActionChains(driver).move_to_element(filters).click(filters).perform()
    time.sleep(random.uniform(2,3))
    for i in range(len(domains)):
        dom = str(domains[i]).replace('b', '').replace("'", "").replace('\\r\\n', '')
        add_filters = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@title='Ajouter de nouveaux filtres']")))
        ActionChains(driver).move_to_element(add_filters).click(add_filters).perform()
        time.sleep(random.uniform(2,3))
        filter_name = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='filterName']")))
        ActionChains(driver).move_to_element(filter_name).click(filter_name).perform()
        filter_name.send_keys(dom)
        time.sleep(random.uniform(2,3))
        filter_value = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='SENDER']")))
        ActionChains(driver).move_to_element(filter_value).click(filter_value).perform()
        filter_value.send_keys(dom)
        time.sleep(random.uniform(2,3))
        criteria = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Sélectionner un critère de filtre')]")))
        ActionChains(driver).move_to_element(criteria).click(criteria).perform()
        time.sleep(random.uniform(2,3))
        contient = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'contient')]")))
        ActionChains(driver).move_to_element(contient).click(contient).perform()
        time.sleep(random.uniform(2,3))
        folder = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Sélectionnez un dossier')]")))
        ActionChains(driver).move_to_element(folder).click(folder).perform()
        time.sleep(random.uniform(2,3))
        inbox = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'Boîte récept.')]")))
        ActionChains(driver).move_to_element(inbox).click(inbox).perform()
        time.sleep(random.uniform(2,3))
        register = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Enregistrer')]")))
        ActionChains(driver).move_to_element(register).click(register).perform()

    print('[Yahoo] Add Filter : Done')

def click_on_more_actions():
    more_actions = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Autres']")))
    more_actions.click()
    time.sleep(random.uniform(2,3))
    more_actions.click()

def scroll(e):
    verical_ordinate = 50
    for i in range(0, 400):
        driver.execute_script("arguments[0].scrollTop = arguments[1]", e, verical_ordinate)
        verical_ordinate += 1


def init_browser(ip, port, p_user, p_password, browsers, hide):
    PROXY_HOST = ip  # rotating proxy
    PROXY_PORT = port
    PROXY_USER = p_user
    PROXY_PASS = p_password

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    background_js_1 = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    """ % (PROXY_HOST, PROXY_PORT)

    firefox_options = f_Options()
    f = open('.\\paths\\path_firefox.txt', 'r')
    bp_firefox = f.readline()
    firefox_options.binary_location = bp_firefox

    comodo_options = f_Options()
    f = open('.\\paths\\path_comodo.txt', 'r')
    bp_comodo = f.readline()
    comodo_options.binary_location = bp_comodo

    chrome_options = c_Options()
    # chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_options.binary_location = '\\binaries\\binary_chrome\\chrome.exe'

    if hide == 'hide_browser':
        chrome_options.headless = True
        firefox_options.headless = True
        comodo_options.headless = True

    global driver

    if ip == '' and port == '' and p_user == '' and p_password == '':

        if browsers == 'comodo':
            driver = webdriver.Firefox(executable_path=PATH_comodo, options=comodo_options)
        elif browsers == 'firefox':
            driver = webdriver.Firefox(executable_path=PATH_firefox, options=firefox_options)
        elif browsers == 'chrome':
            print('[Yahoo] Chrome without proxy : Activated')
            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(executable_path=PATH_chrome, options=chrome_options)

    elif p_user == '' and p_password == '':

        proxy_ip_port = ip + ':' + port

        if browsers == 'comodo':
            print('[Yahoo] Comodo proxy : Activated')
            comodo_options = f_Options()
            comodo_options.binary_location = bp_comodo
            desired_capability = webdriver.DesiredCapabilities.FIREFOX
            desired_capability['marionette'] = True
            desired_capability['proxy'] = {
                'proxyType': "manual",
                'httpProxy': proxy_ip_port,
                'ftpProxy': proxy_ip_port,
                'sslProxy': proxy_ip_port,
            }
            driver = webdriver.Firefox(executable_path=PATH_comodo, options=comodo_options)
        elif browsers == 'firefox':
            print('[Yahoo] Firefox proxy : Activated')
            firefox_options = f_Options()
            firefox_options.binary_location = bp_firefox
            desired_capability = webdriver.DesiredCapabilities.FIREFOX
            desired_capability['marionette'] = True
            desired_capability['proxy'] = {
                'proxyType': "manual",
                'httpProxy': proxy_ip_port,
                'ftpProxy': proxy_ip_port,
                'sslProxy': proxy_ip_port,
            }
            driver = webdriver.Firefox(executable_path=PATH_firefox, capabilities=desired_capability,
                                       options=firefox_options)
        elif browsers == 'chrome':
            print('[Yahoo] Chrome proxy : Activated')
            chrome_options = webdriver.ChromeOptions()
            use_proxy = True
            user_agent = None
            if use_proxy:
                pluginfile = 'proxy_plugin.zip'
                with zipfile.ZipFile(pluginfile, 'w') as zp:
                    zp.writestr("manifest.json", manifest_json)
                    zp.writestr("background.js", background_js_1)
                chrome_options.add_extension(pluginfile)
            if user_agent:
                chrome_options.add_argument('--user-agent=%s' % user_agent)
            driver = webdriver.Chrome(executable_path=PATH_chrome, options=chrome_options)

    else:

        if browsers == 'comodo':
            print('[Yahoo] Comodo proxy with auth : Activated')
            driver = webdriver.Firefox(executable_path=PATH_comodo, options=comodo_options)
        elif browsers == 'firefox':
            driver = webdriver.Firefox(executable_path=PATH_firefox, options=firefox_options)
        elif browsers == 'chrome':
            print('[Yahoo] Chrome proxy with auth : Activated')
            chrome_options = webdriver.ChromeOptions()
            use_proxy = True
            user_agent = None
            if use_proxy:
                pluginfile = 'proxy_auth_plugin.zip'
                with zipfile.ZipFile(pluginfile, 'w') as zp:
                    zp.writestr("manifest.json", manifest_json)
                    zp.writestr("background.js", background_js)
                chrome_options.add_extension(pluginfile)
            if user_agent:
                chrome_options.add_argument('--user-agent=%s' % user_agent)
            driver = webdriver.Chrome(executable_path=PATH_chrome, options=chrome_options)

    return driver


def test(email, password, ip, port, p_user, p_password, tasks, subject, browsers, hide, domains):

    if 'mark_as_not_spam' in tasks and len(tasks) == 1:
        init_browser(ip, port, p_user, p_password, browsers, hide)
        try:
            login_yahoo(email, password, driver)
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Yahoo\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "w+")
            f.write(date_time + " Email : " + email + " -- task : " + tasks[0] + "-- Status : Success")
            f.close()
            time.sleep(random.uniform(2,3))
        except Exception as e:
            print(e)
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Yahoo\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "w+")
            f.write(date_time + " Email : " + email + " -- task : " + tasks[0] + "-- Status : Error")
            f.close()
            time.sleep(random.uniform(2,3))
        spam = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(@aria-label,'Spam')]")))
        time.sleep(random.uniform(2,3))
        ActionChains(driver).move_to_element(spam).click(spam).perform()
        try:
            eval('mark_as_not_spam_yahoo(driver,subject)')
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Yahoo\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "w+")
            f.write("\n\r" + date_time + " Email : " + email + " -- task : Mark as not spam -- Status : Success")
            f.close()
            time.sleep(random.uniform(2,3))
        except Exception as e:
            print(e)
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Yahoo\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "w+")
            f.write("\n\r" + date_time + " Email : " + email + " -- task : Mark as not spam -- Status : Error")
            f.close()
            time.sleep(random.uniform(2,3))
    elif 'mark_as_not_spam' in tasks and len(tasks) != 1:
        init_browser(ip, port, p_user, p_password, browsers, hide)
        try:
            login_yahoo(email, password, driver)
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Yahoo\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "w+")
            f.write(date_time + " Email : " + email + " -- task : Login -- Status : Success")
            f.close()
            time.sleep(random.uniform(2,3))
        except Exception as e:
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Yahoo\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "w+")
            f.write(date_time + " Email : " + email + " -- task : Login -- Status : Error")
            f.close()
            time.sleep(random.uniform(2,3))
        spam = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(@aria-label,'Spam')]")))
        time.sleep(random.uniform(2,3))
        ActionChains(driver).move_to_element(spam).click(spam).perform()
        try:
            eval('mark_as_not_spam_yahoo(driver,subject)')
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "a+")
            time.sleep(random.uniform(2,3))
            f.write(
                "\n\r" + date_time + " Email : " + email + " -- Task : Mark as not spam -- Status : Success ")
            f.close()
        except Exception as e:
            print(e)
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "a+")
            time.sleep(random.uniform(2,3))
            f.write(
                "\n\r" + date_time + " Email : " + email + " -- Task : Mark as not spam -- Status : Error ")
            f.close()
            pass
        time.sleep(random.uniform(2,3))
        search = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@aria-label,'Zone de recherche')]")))
        time.sleep(random.uniform(2,3))
        tasks.remove('mark_as_not_spam')
        search.send_keys('in:inbox subject:' + subject + Keys.RETURN)
        e = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@role='article']")))
        try:
            while (e):
                ActionChains(driver).move_to_element(e).click(e).perform()
                x = bool(random.getrandbits(1))
                print('x is ', x)
                y = bool(random.getrandbits(1))
                print('y is ', y)
                if x == True:
                    eval('click_on_more_actions()')
                else:
                    pass
                element = driver.find_element_by_xpath("//div[@aria-label='Vue Discussion']")
                if y == True:
                    eval('scroll(element)')
                else:
                    pass
                for task in tasks:
                    try:
                        eval(task + '_yahoo(driver,subject)')
                        time.sleep(random.uniform(1, 3))
                        now = datetime.now()
                        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                        f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "a+")
                        time.sleep(random.uniform(2,3))
                        f.write(
                            "\n\r" + date_time + " Email : " + email + " -- Task : " + task + " -- Status : Success ")
                        f.close()
                        print('[Yahoo] log done')
                    except Exception as e:
                        print(e)
                        now = datetime.now()
                        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                        f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "a+")
                        time.sleep(random.uniform(2,3))
                        f.write(
                            "\n\r" + date_time + " Email : " + email + " -- Task : " + task + " -- Status : Error ")
                        f.close()

                try:
                    back = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Retour')]")))
                    ActionChains(driver).move_to_element(back).click(back).perform()
                except Exception as e:
                    print(e)
                    pass
                time.sleep(random.uniform(2,3))
                e = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//a[@role='article']")))
        except Exception as e:
            print(e)

    elif 'add_filter' in tasks and len(tasks) == 1:
        init_browser(ip, port, p_user, p_password, browsers, hide)
        try:
            login_yahoo(email, password, driver)
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Yahoo\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "w+")
            f.write(date_time + " Email : " + email + " -- task : Login -- Status : Success")
            f.close()
            time.sleep(random.uniform(2,3))
        except Exception as e:
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Yahoo\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "w+")
            f.write(date_time + " Email : " + email + " -- task : Login -- Status : Success")
            f.close()
            time.sleep(random.uniform(2,3))
        try:
            eval('add_filter_yahoo(driver,subject,domains)')
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "a+")
            f.write("\n\r" + date_time + " Email : " + email + " -- task : " + tasks[0] + " -- Status : Success")
            f.close()
            time.sleep(random.uniform(2,3))
        except Exception as e:
            print(e)
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "a+")
            f.write("\n\r" + date_time + " Email : " + email + " -- task : " + tasks[0] + " -- Status : Success")
            f.close()
            time.sleep(random.uniform(2,3))


    elif ('mark_as_not_spam' not in tasks) and ('add_filter' not in tasks):

        init_browser(ip, port, p_user, p_password, browsers, hide)
        try:
            login_yahoo(email, password, driver)
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Yahoo\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "w+")
            f.write(date_time + " Email : " + email + " -- task : Login -- Status : Success")
            f.close()
            time.sleep(random.uniform(2,3))
        except Exception as e:
            print(e)
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Yahoo\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "w+")
            f.write(date_time + " Email : " + email + " -- task : Login -- Status : Success")
            f.close()
            time.sleep(random.uniform(2,3))

        search = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@aria-label,'Zone de recherche')]")))
        time.sleep(random.uniform(2,3))
        search.send_keys('in:inbox subject:'+subject+Keys.RETURN)
        e = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@role='article']")))
        try:
            while (e):
                ActionChains(driver).move_to_element(e).click(e).perform()
                x = bool(random.getrandbits(1))
                print('x is ', x)
                y = bool(random.getrandbits(1))
                print('y is ', y)
                if x == True:
                    eval('click_on_more_actions()')
                else:
                    pass
                element = driver.find_element_by_xpath("//div[@aria-label='Vue Discussion']")
                print(element)
                if y == True:
                    eval('scroll(element)')
                else:
                    pass
                for task in tasks:
                    try:
                        eval(task + '_yahoo(driver,subject)')
                        now = datetime.now()
                        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                        f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "a+")
                        f.write("\n\r" + date_time + " Email : " + email + " -- task : " + task + " -- Status : Success")
                        f.close()
                        time.sleep(random.uniform(1, 3))
                    except Exception as e:
                        print(e)
                        now = datetime.now()
                        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                        f = open(".\\Log_Yahoo\\" + date + "\\" + t + ".txt", "a+")
                        f.write("\n\r" + date_time + " Email : " + email + " -- task : " + task + " -- Status : Error")
                        f.close()
                        time.sleep(random.uniform(2,3))
                try:
                    back = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Retour')]")))
                    ActionChains(driver).move_to_element(back).click(back).perform()
                except Exception as e:
                    print(e)
                    pass
                time.sleep(random.uniform(2,3))
                e = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//a[@role='article']")))
        except Exception as e:
            print(e)

    time.sleep(5)
    driver.quit()


def hey(x):
    inputs = list(x.values())
    d = inputs[6].readlines()
    r = str(d[0]).replace('b', '').replace("'", "").replace('\\r\\n', '')
    print(r)
    return 0

def launch_yahoo(x):
    # data = pd.read_csv('C:/Users/SALMAN ELKABIBI/Desktop/data.csv',sep=';')
    global processes
    global browsers
    global acc, subject, n
    acc = x['accounts']
    d = x['accounts'].split('\r\n')
    for i in range(len(d)):
        d[i] = d[i].split(';')
    data = pd.DataFrame(d, columns=['Email', 'Password', 'ip', 'port', 'p_user', 'p_password'])
    print(data)
    emails = data['Email'].tolist()
    passwords = data['Password'].tolist()
    ips = data['ip'].tolist()
    ports = data['port'].tolist()
    p_users = data['p_user'].tolist()
    p_passwords = data['p_password'].tolist()

    l = len(data)
    inputs = list(x.values())
    subject = inputs[0]
    tasks = inputs[1].split(',')
    browsers = inputs[3]
    hide = inputs[5]
    n = int(inputs[2])
    if 'add_filter' in tasks :
        domains = inputs[6].readlines()
    else:
        domains = []
    processes = []

    while (len(emails) != 0):
        for i in range(n):
            p = Process(target=test, args=(
                emails[0], passwords[0], ips[0], ports[0], p_users[0], p_passwords[0], tasks, subject, browsers,
                hide,domains))
            p.start()
            time.sleep(random.uniform(1,2))
            processes.append(p)

            emails.remove(emails[0]), passwords.remove(passwords[0]), ips.remove(ips[0]), ports.remove(ports[0]), p_users.remove(p_users[0]), p_passwords.remove(p_passwords[0])

        for process in processes:
            process.join()

    time.sleep(random.uniform(2,3))

    print("[Yahoo] --- %s seconds ---" % (time.time() - start_time))
    print("[Yahoo] Script Done")

    return redirect(
        url_for('.interface_yahoo', acc=acc, subject=subject, n=n))


global sched
def launch_yahoo_schedule(y):
    try:
        print("Your task will be launch in  " + y['schedule_date'] + " at  " + y['schedule_time'])
        h = y['schedule_time'].split(':')[0]
        m = y['schedule_time'].split(':')[1]
        sched = BlockingScheduler()
        sched.add_job(func=launch_yahoo, args=[y], trigger='cron', start_date=y['schedule_date'], hour=h, minute=m)
        sched.start()
    except Exception as e:
        print('[Exception :(]',e)
        launch_yahoo(y)
    return redirect(
        url_for('.interface_yahoo', acc=acc, subject=subject, n=n))

def stop_yahoo():
    try:
        pid = os.getpid()
        for process in processes:
            p = psutil.Process(process.pid)
            print("[Yahoo] suspend")
            p.suspend()
        if browsers == 'comodo':
            subprocess.call("taskkill /F /IM icedragon.exe")
            subprocess.call("taskkill /F /IM geckodriver.exe")
        elif browsers == 'chrome':
            subprocess.call("taskkill /F /IM chrome.exe")
            subprocess.call("taskkill /F /IM chromedriver.exe")
        elif browsers == 'firefox':
            subprocess.call("taskkill /F /IM firefox.exe")
            subprocess.call("taskkill /F /IM geckodriver.exe")
    except:
        try:
            if browsers == 'comodo':
                subprocess.call("taskkill /F /IM icedragon.exe")
                subprocess.call("taskkill /F /IM geckodriver.exe")
            elif browsers == 'chrome':
                subprocess.call("taskkill /F /IM chrome.exe")
                subprocess.call("taskkill /F /IM chromedriver.exe")
            elif browsers == 'firefox':
                subprocess.call("taskkill /F /IM firefox.exe")
                subprocess.call("taskkill /F /IM geckodriver.exe")
        except:
            sched.stop()

    return redirect(url_for('.interface_yahoo', acc=acc, subject=subject, n=n))


def pause_yahoo():
    pid = os.getpid()
    for process in processes:
        p = psutil.Process(process.pid)
        print("[Yahoo] suspend")
        p.suspend()

    return render_template("pauseYahoo.html", acc=acc, subject=subject, n=n)


def resume_yahoo():
    print(acc, subject, n)
    pid = os.getpid()
    for process in processes:
        p = psutil.Process(process.pid)
        print("[Yahoo] resume it", process.is_alive())
        p.resume()

    return redirect(url_for('.interface_yahoo', acc=acc, subject=subject, n=n))
