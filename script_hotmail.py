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




start_time = time.time()
username = 'SALMAN ELKABIBI'
global PATH_chrome, PATH_firefox, PATH_comodo

PATH_chrome = ".\\chrome_driver\\chromedriver.exe"
PATH_firefox = ".\\firefox_driver\\geckodriver.exe"
PATH_comodo = ".\\firefox_driver\\geckodriver.exe"



def login(email, password, driver):
    try:
        print("===> logging in ")
        driver.get(
            "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1621957211&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26RpsCsrfState%3d46b8cc68-7a8f-c9f7-4988-8fda7cc04013&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015")
        # driver.get("https://myip.com")
        e = driver.find_element_by_id('i0116')
        e.send_keys(email)
        time.sleep(1)
        e.send_keys(Keys.RETURN)

        time.sleep(2)
        p = driver.find_element_by_id('i0118')
        p.send_keys(password)
        time.sleep(1)
        p.send_keys(Keys.RETURN)
    except:
        driver.save_screenshot(".\\screenshots\\login_errors\\" + email + ".png")
        
    try: 
        dont_show = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='DontShowAgain']")))
        time.sleep(1)
        dont_show.click()
        time.sleep(1)
        yes = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@value='Yes']")))
        time.sleep(1)
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
            time.sleep(1)
        except:
            close = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//button[@title='Fermer le volet']|//button[@title='Close pane']"))).click()
            print('Prioritaire already clicked')
            time.sleep(1)
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
            time.sleep(1)
        except:
            close = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//button[@title='Fermer le volet']|//button[@title='Close pane']"))).click()
            print('Prioritaire already clicked')
            time.sleep(2)



def show_bloqued_content(driver):
    try:
        afficher_contenu = driver.find_element_by_link_text('Afficher le contenu bloqué').click()
        time.sleep(2)
    except:
        print('===> Bloqued content already displayed !')
        time.sleep(1)


def archive(driver, subject, link, rep):
    try:
        print('===> Archiving')
        # e.click()
        archive = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@name='Archiver']|//button[@name='Archive']")))
        archive.click()
    except Exception as e:
        print(e)
        print('===> Archiving : Error')


def categorize(driver, subject, link, rep):
    categorie = ['Orange', 'Rouge', 'Bleu', 'Jaune', 'Vert', 'Violet']
    categories = ['Blue', 'Green', 'Orange', 'Purple', 'Red', 'Yellow']
    print('===> Categorizing')
    try:
        try:
            categoriser = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
                (By.XPATH, "//button[@name='Catégoriser']|//button[@name='Categorize']")))
            time.sleep(1)
            categoriser.click()
            categorize = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
                (By.XPATH,
                 "//div[@title='Catégorie " + random.choice(categorie) + "']|//div[contains(@title,'" + random.choice(categories) + "')]")))
            time.sleep(1)
            categorize.click()
        except:
            more = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,
                                                                                           "//button[@aria-label='Autres actions de courrier']|//button[@aria-label='More mail actions']")))
            time.sleep(1)
            more.click()
            categorize = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
                (By.XPATH, "//button[@name='Catégoriser']|//button[@name='Categorize']")))
            time.sleep(1)
            categorize.click()
            categoriser = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@title='Catégorie " + random.choice(categorie) + "']")))
            time.sleep(1)
            categoriser.click()

    except Exception as e:
        print(e)


def spam_to_inbox(driver, subject, link):
    try:
        time.sleep(2)
        courrier_legetime = driver.find_element_by_xpath(
            "//button[@name='Courrier légitime']|//button[@name='Not junk']")
        courrier_legetime.click()

        time.sleep(2)

        ok = driver.find_element_by_xpath(
            "//span[contains(text(),'OK')][contains(@class,'ms-Button')]")
        ok.click()

        time.sleep(2)
    except Exception as e:
        print(e)


def add_contact(driver, subject, link, rep):
    print('===> Add contact')
    try:
        time.sleep(3)
        click_form = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                                       "//span[contains(@aria-label,'Ouvre la carte de visite')]|//span[contains(@aria-label,'Opens Profile Card')]")))
        # click_form = driver.find_element_by_xpath("//span[contains(@aria-label,'Ouvre la carte de visite')]")
        time.sleep(2)
        print('click_form = ', click_form)
        ActionChains(driver).move_to_element(click_form).perform()
        time.sleep(5)
        more_options = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@data-log-name='SecondaryActions']")))
        print('more_options = ', more_options)
        more_options.click()
        time.sleep(2)
        add_contact = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@data-log-name='AddContact']")))
        ActionChains(driver).move_to_element(add_contact).click(add_contact).perform()
        time.sleep(2)
        creer = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@data-log-name='ContactEditorSave']")))
        ActionChains(driver).move_to_element(creer).click(creer).perform()
        time.sleep(2)
    except Exception as e:
        print(e)

    print('add done')


def flag(driver, subject, link, rep):
    print('===> Flag')
    try:
        more = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,
                                                                                "//button[@aria-label='Autres actions de courrier']|//button[@aria-label='More mail actions']")))
        time.sleep(1)
        more.click()
        flag = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
            (By.XPATH, "//button[@name='Assurer un suivi']|//button[@name='Flag']")))
        time.sleep(1)
        flag.click()
    except Exception as e:
        print('===> Flag : Error')
        print(e)


def offer_click_inbox(driver, subject, link, rep):
    print('Offer click inbox')
    try:
        offer_click = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'" + link + "')]")))
        print(offer_click)
        time.sleep(2)
        ActionChains(driver).move_to_element(offer_click).click(offer_click).perform()
        time.sleep(2)
        p = driver.window_handles[0]
        c = driver.window_handles[1]
        driver.switch_to.window(c)
        time.sleep(6)
        driver.close()
        driver.switch_to.window(p)
        time.sleep(2)
    except Exception as e:
        print(e)


def reply(driver, subject, link, rep):
    try:
        print('Reply')
        reply = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, "//button[@aria-label='Répondre']|//button[@aria-label='Reply']")))
        time.sleep(1)
        reply.click()
        time.sleep(5)
        reply_field = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@aria-label='Corps du message']|//div[@aria-label='Message body']"))).send_keys(rep)
        time.sleep(5)
        send = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Envoyer']|//button[@aria-label='Send']")))
        time.sleep(1)
        send.click()
        time.sleep(5)
    except Exception as e:
        print(e)
        print('Reply : Error')


def when_selected(driver):
    print('Mark as read : When Selected')
    try:
        parametres = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@id='owaSettingsButton']")))
        parametres.click()
        time.sleep(2)
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
    print('Mark as read : When Changed')
    try:
        parametres = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@id='owaSettingsButton']")))
        parametres.click()
        time.sleep(2)
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
            print('Chrome without proxy : Activated')
            chrome_options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(executable_path=PATH_chrome, options=chrome_options)

    elif p_user == '' and p_password == '':

        proxy_ip_port = ip + ':' + port

        if browsers == 'comodo':
            print('Firefox proxy : Activated')
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
            print('Firefox proxy : Activated')
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
            print('Chrome proxy : Activated')
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
            print('Chrome proxy with auth : Activated')
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
        f= open("Log_file_hotmail.txt","w+")
        f.write(date_time + " Email : " + email + " -- task : Login -- Status : Success")
        f.close()
        time.sleep(2)
    except Exception as e:
        now = datetime.now()
        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
        f= open("Log_file.txt","w+")
        f.write(date_time + " Email : " + email + " -- task : Login -- Status : Error")
        time.sleep(2)
        driver.quit()
        print(e)
        print('logging Failed')

    if mark_as_read == "when_selected":
        when_selected(driver)
        time.sleep(3)
    elif mark_as_read == "when_changed":
        when_changed(driver)
        time.sleep(3)
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
            eval('spam_to_inbox(driver,subject,link)')
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
                eval('show_bloqued_content(driver)')
                for task in tasks:
                    try:
                        eval(task + '(driver,subject,link,rep)')
                        time.sleep(2)
                    except Exception as e:
                        print(e)
                        driver.save_screenshot(".\\screenshots\\login_errors\\tasks_errors\\" + task + ".png")
                Boîte_de_réception = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                    (By.XPATH, "//div[@title='Boîte de réception']|//div[@title='Inbox']")))
                Boîte_de_réception.click()
                try:
                    e = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'" + subject + "')]")))
                except:
                    print('No more emails')
                    pass
        except:
            pass



    except Exception as e:
        print(e)
        print('Spam empty')
        Boîte_de_réception = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@title='Boîte de réception']|//div[@title='Inbox']")))
        Boîte_de_réception.click()
        try:
            e = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'" + subject + "')]")))
            
            while (e):
                e.click()
                eval('show_bloqued_content(driver)')
                for task in tasks:
                    try:
                        eval(task + '(driver,subject,link,rep)')
                        time.sleep(2)
                        now = datetime.now()
                        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                        f= open("Log_file.txt","a+")
                        time.sleep(2)
                        f.write("\n\r" + date_time + " Email : " + email + " -- Task : " + task + " -- Status : Success ")
                        f.close()
                        print('log done')
                    except Exception as e:
                        print(e)
                        now = datetime.now()
                        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                        f= open("Log_file.txt","a+")
                        time.sleep(2)
                        f.write("\n\r" + date_time + " Email : " + email + " -- Task : " + task + " -- Status : Error ")
                        f.close()

                Boîte_de_réception = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                    (By.XPATH, "//div[@title='Boîte de réception']|//div[@title='Inbox']")))
                Boîte_de_réception.click()
                try:
                    e = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'" + subject + "')]")))
                except:
                    print('No more emails')
                    pass
        except Exception as e:
            print(e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            line_number = exception_traceback.tb_lineno
            print(line_number)
            pass

    driver.quit()
    print('=======================')
    print('====== Tasks Done =====')
    print('=======================')


def test2(email, password, ip, port, p_user, p_password, tasks, subject, browsers, link, hide, rep, i):
    try:
        init_browser(ip, port, p_user, p_password, browsers, hide)
        print('hello')
    except Exception as e:
        print(e)


def hey(x):
    inputs = list(x.values())
    print(inputs)
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
            time.sleep(1)
            processes.append(p)

            emails.remove(emails[0]), passwords.remove(passwords[0])

        for process in processes:
            process.join()

    time.sleep(2)

    print("--- %s seconds ---" % (time.time() - start_time))
    print("Script Done")


    return redirect(
        url_for('.interface', acc=acc, subject=subject, link=link, n=n))


def stop():
    print(acc, subject, link, n)
    try:
        pid = os.getpid()
        for process in processes:
            p = psutil.Process(process.pid)
            print("suspend")
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
        print("suspend")
        p.suspend()

    return render_template("pauseHotmail.html", acc=acc, subject=subject, link=link, n=n)


def resume():
    print(acc, subject, link, n)
    pid = os.getpid()
    for process in processes:
        p = psutil.Process(process.pid)
        print("resume it", process.is_alive())
        p.resume()

    return redirect(url_for('.interface', acc=acc, subject=subject, link=link, n=n))
