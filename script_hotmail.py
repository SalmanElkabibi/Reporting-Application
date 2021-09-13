import subprocess
from datetime import datetime
from app import *
from flask import *
import pandas as pd
import json
import threading
import zipfile
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
import sys, os
import psutil
from selenium.webdriver.firefox.options import Options as f_Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers import cron



start_time = time.time()
username = 'SALMAN ELKABIBI'
global PATH_chrome, PATH_firefox, PATH_comodo

PATH_chrome = ".\\chrome_driver\\chromedriver.exe"
PATH_firefox = ".\\firefox_driver\\geckodriver.exe"
PATH_comodo = ".\\firefox_driver\\geckodriver.exe"



def login(email, password, driver):
    try:
        print("[Hotmail] ===> logging in ")
        driver.get(
            "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1621957211&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26RpsCsrfState%3d46b8cc68-7a8f-c9f7-4988-8fda7cc04013&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015")
        # driver.get("https://myip.com")
        e = driver.find_element_by_id('i0116')
        e.send_keys(email)
        time.sleep(random.uniform(1,2))
        e.send_keys(Keys.RETURN)

        time.sleep(random.uniform(2,3))
        p = driver.find_element_by_id('i0118')
        p.send_keys(password)
        time.sleep(random.uniform(1,2))
        p.send_keys(Keys.RETURN)
    except:
        driver.save_screenshot(".\\screenshots\\login_errors\\" + email + ".png")
        
    try: 
        dont_show = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='DontShowAgain']")))
        time.sleep(random.uniform(1,2))
        dont_show.click()
        time.sleep(random.uniform(1,2))
        yes = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@value='Yes']")))
        time.sleep(random.uniform(1,2))
        yes.click()
    except Exception as e:
        print(e)

    try:
        parametres = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@id='owaSettingsButton']")))
        parametres.click()
        try:
            ckeck = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                                      "//button[@aria-checked='true'][@aria-label='Boîte de réception Prioritaire']|//button[@aria-checked='true'][@aria-label='Focused Inbox']"))).click()
            close = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//button[@title='Fermer le volet']|//button[@title='Close pane']"))).click()
            time.sleep(random.uniform(1,2))
        except:
            close = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//button[@title='Fermer le volet']|//button[@title='Close pane']"))).click()
            print('[Hotmail] Prioritaire already clicked')
            time.sleep(random.uniform(1,2))
    except:
        more = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                                 "//button[@title='Accéder à des fonctionnalités supplémentaires']|//button[@title='Access additional features']"))).click()
        parametres = WebDriverWait(driver, 15).until(EC.visibility_of_element_located(
            (By.XPATH, "//label[contains(text(),'Paramètres')]|//label[contains(text(),'Settings')]")))
        parametres.click()
        try:
            ckeck = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                                      "//button[@aria-checked='true'][@aria-label='Boîte de réception Prioritaire']|//button[@aria-checked='true'][@aria-label='Focused Inbox']"))).click()
            close = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//button[@title='Fermer le volet']|//button[@title='Close pane']"))).click()
            time.sleep(random.uniform(1,2))
        except:
            close = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//button[@title='Fermer le volet']|//button[@title='Close pane']"))).click()
            print('[Hotmail] Prioritaire already clicked')
            time.sleep(random.uniform(2,3))



def show_bloqued_content(driver):
    try:
        afficher_contenu = driver.find_element_by_link_text('Afficher le contenu bloqué').click()
        time.sleep(random.uniform(2,3))
    except:
        print('[Hotmail] ===> Bloqued content already displayed !')
        time.sleep(random.uniform(1,2))


def archive(driver, subject, link, rep):

    print('[Hotmail] ===> Archiving')
    # e.click()
    archive = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@name='Archiver']|//button[@name='Archive']")))
    archive.click()



def categorize(driver, subject, link, rep):
    categorie = ['Orange', 'Rouge', 'Bleu', 'Jaune', 'Vert', 'Violet']
    categories = ['Blue', 'Green', 'Orange', 'Purple', 'Red', 'Yellow']
    print('[Hotmail] ===> Categorizing')
    try:
        categoriser = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH, "//button[@name='Catégoriser']|//button[@name='Categorize']")))
        time.sleep(random.uniform(1,2))
        categoriser.click()
        categorize = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH,
             "//div[@title='Catégorie " + random.choice(categorie) + "']|//div[contains(@title,'" + random.choice(categories) + "')]")))
        time.sleep(random.uniform(1,2))
        categorize.click()
    except:
        more = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,
                                                                                       "//button[@aria-label='Autres actions de courrier']|//button[@aria-label='More mail actions']")))
        time.sleep(random.uniform(1,2))
        more.click()
        categorize = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH, "//button[@name='Catégoriser']|//button[@name='Categorize']")))
        time.sleep(random.uniform(1,2))
        categorize.click()
        categoriser = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@title='Catégorie " + random.choice(categorie) + "']")))
        time.sleep(random.uniform(1,2))
        categoriser.click()



def spam_to_inbox(driver, subject, link):

    time.sleep(random.uniform(2,3))
    courrier_legetime = driver.find_element_by_xpath(
        "//button[@name='Courrier légitime']|//button[@name='Not junk']")
    courrier_legetime.click()

    time.sleep(random.uniform(2,3))

    ok = driver.find_element_by_xpath(
        "//span[contains(text(),'OK')][contains(@class,'ms-Button')]")
    ok.click()

    time.sleep(random.uniform(2,3))



def add_contact(driver, subject, link, rep):
    print('[Hotmail] ===> Add contact')

    time.sleep(random.uniform(3,3.5))
    click_form = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                                   "//span[contains(@aria-label,'Ouvre la carte de visite')]|//span[contains(@aria-label,'Opens Profile Card')]")))
    # click_form = driver.find_element_by_xpath("//span[contains(@aria-label,'Ouvre la carte de visite')]")
    time.sleep(random.uniform(2,3))
    print('[Hotmail] click_form = ', click_form)
    ActionChains(driver).move_to_element(click_form).perform()
    time.sleep(5)
    more_options = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@data-log-name='SecondaryActions']")))
    print('[Hotmail] more_options = ', more_options)
    more_options.click()
    time.sleep(random.uniform(2,3))
    add_contact = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@data-log-name='AddContact']")))
    ActionChains(driver).move_to_element(add_contact).click(add_contact).perform()
    time.sleep(random.uniform(2,3))
    creer = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@data-log-name='ContactEditorSave']")))
    ActionChains(driver).move_to_element(creer).click(creer).perform()
    time.sleep(random.uniform(2,3))



def flag(driver, subject, link, rep):
    print('[Hotmail] ===> Flag')

    more = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,
                                                                            "//button[@aria-label='Autres actions de courrier']|//button[@aria-label='More mail actions']")))
    time.sleep(random.uniform(1,2))
    more.click()
    flag = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
        (By.XPATH, "//button[@name='Assurer un suivi']|//button[@name='Flag']")))
    time.sleep(random.uniform(1,2))
    flag.click()



def offer_click_inbox(driver, subject, link, rep):
    print('[Hotmail] Offer click inbox')

    offer_click = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'" + link + "')]")))
    print(offer_click)
    time.sleep(random.uniform(2,3))
    ActionChains(driver).move_to_element(offer_click).click(offer_click).perform()
    time.sleep(random.uniform(2,3))
    p = driver.window_handles[0]
    c = driver.window_handles[1]
    driver.switch_to.window(c)
    time.sleep(6)
    driver.close()
    driver.switch_to.window(p)
    time.sleep(random.uniform(2,3))



def reply(driver, subject, link, rep):

    print('[Hotmail] Reply')
    reply = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
        (By.XPATH, "//button[@aria-label='Répondre']|//button[@aria-label='Reply']")))
    time.sleep(random.uniform(1,2))
    reply.click()
    time.sleep(5)
    reply_field = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.XPATH, "//div[@aria-label='Corps du message']|//div[@aria-label='Message body']"))).send_keys(rep)
    time.sleep(5)
    send = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Envoyer']|//button[@aria-label='Send']")))
    time.sleep(random.uniform(1,2))
    send.click()
    time.sleep(5)



def when_selected(driver):
    print('[Hotmail] Mark as read : When Selected')
    try:
        parametres = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@id='owaSettingsButton']")))
        parametres.click()
        time.sleep(random.uniform(2,3))
    except:
        more = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                                 "//button[@title='Accéder à des fonctionnalités supplémentaires']|//button[@title='Access additional features']"))).click()
        parametres = WebDriverWait(driver, 15).until(EC.visibility_of_element_located(
            (By.XPATH, "//label[contains(text(),'Paramètres')]|//label[contains(text(),'Settings')]")))
        parametres.click()

    view_settings = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'View all Outlook settings')]")))
    view_settings.click()

    message_handling = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Message handling')]")))
    message_handling.click()

    selected = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//span[contains(text(),'Mark displayed items as read as soon as')]")))
    selected.click()

    try:
        save = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(),'Save')]")))
        save.click()
    except:
        pass

    close = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@aria-label='Close settings']")))
    close.click()


def when_changed(driver):
    print('[Hotmail] Mark as read : When Changed')
    try:
        parametres = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@id='owaSettingsButton']")))
        parametres.click()
        time.sleep(random.uniform(2,3))
    except:
        more = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                                 "//button[@title='Accéder à des fonctionnalités supplémentaires']|//button[@title='Access additional features']"))).click()
        parametres = WebDriverWait(driver, 15).until(EC.visibility_of_element_located(
            (By.XPATH, "//label[contains(text(),'Paramètres')]|//label[contains(text(),'Settings')]")))
        parametres.click()

    view_settings = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'View all Outlook settings')]")))
    view_settings.click()

    message_handling = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Message handling')]")))
    message_handling.click()

    selected = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//span[contains(text(),'Mark displayed items as read when the selection changes')]")))
    selected.click()

    try:
        save = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//span[contains(text(),'Save')]")))
        save.click()
    except:
        pass

    close = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@aria-label='Close settings']")))
    close.click()


def click_on_more_actions():
    more_actions = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='More mail actions']")))
    more_actions.click()
    time.sleep(random.uniform(2,3))
    more_actions.click()

def scroll(e):
    verical_ordinate = 50
    for i in range(0, 10):
        driver.execute_script("arguments[0].scrollTop = arguments[1]", e[1], verical_ordinate)
        verical_ordinate += 50

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
            print('[Hotmail] Chrome without proxy : Activated')
            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(executable_path=PATH_chrome, options=chrome_options)

    elif p_user == '' and p_password == '':

        proxy_ip_port = ip + ':' + port

        if browsers == 'comodo':
            print('[Hotmail] Firefox proxy : Activated')
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
            print('[Hotmail] Firefox proxy : Activated')
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
            print('[Hotmail] Chrome proxy : Activated')
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
            driver = webdriver.Firefox(executable_path=PATH_comodo, options=comodo_options)
        elif browsers == 'firefox':
            driver = webdriver.Firefox(executable_path=PATH_firefox, options=firefox_options)
        elif browsers == 'chrome':
            print('[Hotmail] Chrome proxy with auth : Activated')
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


def test(email, password, ip, port, p_user, p_password, tasks, subject, browsers, link, hide, rep, i, mark_as_read):
    init_browser(ip, port, p_user, p_password, browsers, hide)
    try:
        login(email, password, driver)
        now = datetime.now()
        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
        date = now.strftime("%d-%m-%Y")
        t = now.strftime("%H_%M_%S")
        try:
            os.makedirs(".\\Log_Hotmail\\" + date)
        except Exception as e:
            print(e)
            print("[Hotmail] Not a problem, let continue the script :)")
            pass
        f= open(".\\Log_hotmail\\"+ date + "\\"+t+".txt","w+")
        f.write(date_time + " Email : " + email + " -- task : Login -- Status : Success")
        f.close()
        time.sleep(random.uniform(2,3))
    except Exception as e:
        now = datetime.now()
        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
        date = now.strftime("%d-%m-%Y")
        t = now.strftime("%H_%M_%S")
        try:
            os.makedirs(".\\Log_Hotmail\\" + date)
        except Exception as e:
            print(e)
            print("[Hotmail] Not a problem, let continue the script :)")
            pass
        f = open(".\\Log_hotmail\\" + date + "\\" + t + ".txt", "w+")
        f.write(date_time + " Email : " + email + " -- task : Login -- Status : Error")
        time.sleep(random.uniform(2,3))
        driver.quit()
        print(e)
        print('[Hotmail] logging Failed')

    if mark_as_read == "when_selected":
        when_selected(driver)
        time.sleep(random.uniform(3,3.5))
    elif mark_as_read == "when_changed":
        when_changed(driver)
        time.sleep(random.uniform(3,3.5))
    try:
        try:
            # spam = driver.find_element_by_xpath("//div[@title='Courrier indésirable']|//div[@title='Junk Email']").click()
            spam = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@title='Courrier indésirable']|//div[@title='Junk Email']")))
            spam.click()
            """p = driver.find_elements_by_class_name('_24WqHp8mfxSp2QIJMkmSrM')
            print(p[0])
            e = p[0].find_element_by_xpath("//span[contains(text(),'" + subject + "')]")
            print(e)"""
            e = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'" + subject + "')]")))
        except Exception as e:
            print(e)
            driver.save_screenshot(".\\screenshots\\login_errors\\" + email + ".png")
        while (e):
            ActionChains(driver).move_to_element(e).click(e).perform()
            try:
                eval('spam_to_inbox(driver,subject,link)')
                time.sleep(random.uniform(1, 3))
                now = datetime.now()
                date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                f = open(".\\Log_hotmail\\" + date + "\\" + t + ".txt", "a+")
                time.sleep(random.uniform(2, 3))
                f.write(
                    "\n\r" + date_time + " Email : " + email + " -- Task : Spam to Inbox -- Status : Success ")
                f.close()
                print('[Hotmail] log done')
            except Exception as e:
                print(e)
                time.sleep(random.uniform(1, 3))
                now = datetime.now()
                date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                f = open(".\\Log_hotmail\\" + date + "\\" + t + ".txt", "a+")
                time.sleep(random.uniform(2, 3))
                f.write(
                    "\n\r" + date_time + " Email : " + email + " -- Task : Spam to Inbox -- Status : Error ")
                f.close()
                print('[Hotmail] log done')

            spam = driver.find_element_by_xpath(
                "//div[@title='Courrier indésirable']|//div[@title='Junk Email']").click()
            e = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'" + subject + "')]")))
        Boîte_de_réception = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@title='Boîte de réception']|//div[@title='Inbox']"))).click()
        e = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'" + subject + "')]")))
        try:
            while (e):
                e.click()
                x = bool(random.getrandbits(1))
                print('x is ', x)
                y = bool(random.getrandbits(1))
                print('y is ', y)
                if x == True:
                    eval('click_on_more_actions()')
                else:
                    pass
                time.sleep(random.uniform(1, 3))
                elements = driver.find_elements_by_xpath("//div[@data-is-scrollable='true']")
                if y == True:
                    eval('scroll(elements)')
                else:
                    pass
                eval('show_bloqued_content(driver)')
                for task in tasks:
                    try:
                        eval(task + '(driver,subject,link,rep)')
                        now = datetime.now()
                        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                        f = open(".\\Log_hotmail\\" + date + "\\" + t + ".txt", "a+")
                        time.sleep(random.uniform(2,3))
                        f.write(
                            "\n\r" + date_time + " Email : " + email + " -- Task : " + task + " -- Status : Success ")
                        f.close()
                        print('[Hotmail] log done')
                    except Exception as e:
                        print(e)
                        now = datetime.now()
                        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                        f = open(".\\Log_hotmail\\" + date + "\\" + t + ".txt", "a+")
                        time.sleep(random.uniform(2,3))
                        f.write(
                            "\n\r" + date_time + " Email : " + email + " -- Task : " + task + " -- Status : Success ")
                        f.close()
                        print('[Hotmail] log done')
                Boîte_de_réception = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                    (By.XPATH, "//div[@title='Boîte de réception']|//div[@title='Inbox']")))
                Boîte_de_réception.click()
                try:
                    e = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'" + subject + "')]")))
                except:
                    print('[Hotmail] No more emails')
                    pass
        except:
            pass



    except Exception as e:
        print(e)
        print('[Hotmail] Spam empty')
        Boîte_de_réception = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@title='Boîte de réception']|//div[@title='Inbox']")))
        Boîte_de_réception.click()
        try:
            e = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'" + subject + "')]")))
            
            while (e):
                e.click()
                x = bool(random.getrandbits(1))
                print('x is ', x)
                y = bool(random.getrandbits(1))
                print('y is ', y)
                if x == True:
                    eval('click_on_more_actions()')
                else:
                    pass
                time.sleep(random.uniform(1, 3))
                elements = driver.find_elements_by_xpath("//div[@data-is-scrollable='true']")
                if y == True :
                    eval('scroll(elements)')
                else:
                    pass
                eval('show_bloqued_content(driver)')
                for task in tasks:
                    try:
                        eval(task + '(driver,subject,link,rep)')
                        now = datetime.now()
                        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                        f = open(".\\Log_hotmail\\" + date + "\\" + t + ".txt", "a+")
                        time.sleep(random.uniform(2,3))
                        f.write("\n\r" + date_time + " Email : " + email + " -- Task : " + task + " -- Status : Success ")
                        f.close()
                        print('[Hotmail] log done')
                    except Exception as e:
                        print(e)
                        now = datetime.now()
                        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                        f = open(".\\Log_hotmail\\" + date + "\\" + t + ".txt", "a+")
                        time.sleep(random.uniform(2,3))
                        f.write("\n\r" + date_time + " Email : " + email + " -- Task : " + task + " -- Status : Error ")
                        f.close()

                Boîte_de_réception = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                    (By.XPATH, "//div[@title='Boîte de réception']|//div[@title='Inbox']")))
                Boîte_de_réception.click()
                try:
                    e = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'" + subject + "')]")))
                except:
                    print('[Hotmail] No more emails')
                    pass
        except Exception as e:
            print(e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            line_number = exception_traceback.tb_lineno
            print(line_number)
            pass

    driver.quit()
    print('[Hotmail] =======================')
    print('[Hotmail] ====== Tasks Done =====')
    print('[Hotmail] =======================')


def test2(email, password, ip, port, p_user, p_password, tasks, subject, browsers, link, hide, rep, i):
    try:
        init_browser(ip, port, p_user, p_password, browsers, hide)
        print('[Hotmail] hello')
    except Exception as e:
        print(e)


def heys(x):
    r = x["schedule_time"].split(':')
    print(r[1])
    return x


def launch(x):
    # data = pd.read_csv('C:/Users/SALMAN ELKABIBI/Desktop/data.csv',sep=';')
    global processes
    global browsers
    global acc, subject, link, n
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
    link = inputs[4]
    hide = inputs[6]
    rep = inputs[7]
    # list(inputs[1])
    n = int(inputs[2])
    mark_as_read = inputs[8]

    processes = []

    while (len(emails) != 0):
        for i in range(n):
            p = Process(target=test, args=(
                emails[0], passwords[0], ips[0], ports[0], p_users[0], p_passwords[0], tasks, subject, browsers, link,
                hide,
                rep, i, mark_as_read))
            p.start()
            time.sleep(random.uniform(1,2))
            processes.append(p)

            emails.remove(emails[0]), passwords.remove(passwords[0])

        for process in processes:
            process.join()

    time.sleep(random.uniform(2,3))

    print("[Hotmail] --- %s seconds ---" % (time.time() - start_time))
    print("[Hotmail] Script Done")


    return redirect(
        url_for('.interface', acc=acc, subject=subject, link=link, n=n))


def launch_schedule(y):
    try:
        print("Your task will be launch in  " + y['schedule_date'] + " at  " + y['schedule_time'])
        h = y['schedule_time'].split(':')[0]
        m = y['schedule_time'].split(':')[1]
        sched = BlockingScheduler()
        trigger = cron.CronTrigger(start_date=y['schedule_date'], hour=h, minute=m)
        sched.add_job(func=launch,args=[y],trigger=trigger)
        sched.start()
    except Exception as e:
        print(e)
        eval('launch(y)')
    return redirect(
        url_for('.interface', acc=acc, subject=subject, link=link, n=n))

def stop():
    print(acc, subject, link, n)
    try:
        pid = os.getpid()
        for process in processes:
            p = psutil.Process(process.pid)
            print("[Hotmail] suspend")
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
        if browsers == 'comodo':
            subprocess.call("taskkill /F /IM icedragon.exe")
            subprocess.call("taskkill /F /IM geckodriver.exe")
        elif browsers == 'chrome':
            subprocess.call("taskkill /F /IM chrome.exe")
            subprocess.call("taskkill /F /IM chromedriver.exe")
        elif browsers == 'firefox':
            subprocess.call("taskkill /F /IM firefox.exe")
            subprocess.call("taskkill /F /IM geckodriver.exe")

    return redirect(url_for(".interface", acc=acc, subject=subject, link=link, n=n))


def pause():
    pid = os.getpid()
    for process in processes:
        p = psutil.Process(process.pid)
        print("[Hotmail] suspend")
        p.suspend()

    return render_template("pauseHotmail.html", acc=acc, subject=subject, link=link, n=n)


def resume():
    print(acc, subject, link, n)
    pid = os.getpid()
    for process in processes:
        p = psutil.Process(process.pid)
        print("[Hotmail] resume it", process.is_alive())
        p.resume()

    return redirect(url_for('.interface', acc=acc, subject=subject, link=link, n=n))
