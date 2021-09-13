from app import *
import pandas as pd
from datetime import datetime
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
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers import cron

start_time = time.time()

global PATH_chrome , PATH_firefox , PATH_comodo
username = 'SALMAN ELKABIBI'
PATH_firefox = ".\\firefox_driver\\geckodriver.exe"
PATH_chrome = ".\chrome_driver\chromedriver.exe"  

chrome_options = c_Options()
chrome_options.binary_location = ".\\binaries\\binary_chrome\\chrome.exe"

	
def login_gmail(email,password,recovery,driver,x,p_user,p_password):
    
    driver.get("https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
    #driver.get("https://myip.com")
    time.sleep(random.uniform(2,3))
    if x == 1 :
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to_alert()
        print(alert)
        alert.send_keys(p_user+Keys.TAB+p_password)
        alert.accept()
        
    e = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//input[@type='email']")))
    e.send_keys(email)
    time.sleep(random.uniform(1,2))
    e.send_keys(Keys.RETURN)
    
    time.sleep(random.uniform(2,3))
    p = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//input[@type='password']")))
    p.send_keys(password)
    time.sleep(random.uniform(1,2))
    p.send_keys(Keys.RETURN)
    
    time.sleep(random.uniform(2,3))

    
    try :
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[text()='Confirm your recovery email']|//div[text()='E-Mail-Adresse zur Kontowiederherstellung bestätigen']|//div[text()='Confirmer votre adresse e-mail de récupération']"))).click()
        r = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//input[@name='knowledgePreregisteredEmailResponse']")))
        r.send_keys(recovery)
        time.sleep(random.uniform(1,2))
        r.send_keys(Keys.RETURN)
    except :
        pass
    try :
        settings = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[@data-tooltip='Settings']")))
        time.sleep(random.uniform(1,2))
        settings.click()
        p = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH,"//label[@class='XL']")))
        c = p[1].find_element_by_xpath("//input[@aria-label='Right of inbox']")
        print(c.is_selected())
        if c.is_selected() == False :
            p[1].click()
            time.sleep(random.uniform(2,3))
            try:
                print('[Gmail] cheking reload button')
                reload = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//button[@name='save']")))
                print(reload)
                reload.click()
                time.sleep(random.uniform(4,4.5))
            except:
                close = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//button[@aria-label='Close']")))
                close.click()

        elif c.is_selected() == True :
            close = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//button[@aria-label='Close']")))
            close.click()
        time.sleep(random.uniform(3,3.5))
    except Exception as e :
        print(e)
        driver.save_screenshot(".\\screenshots\\login_errors\\"+email+".png")


def star_gmail(subject,driver,s,rep,link,domain):
    print('[Gmail] Star')
    star = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[@aria-label='Not starred']")))
    time.sleep(random.uniform(2,3))
    star.click()

def archive_gmail(subject,driver,s,rep,link,domain):
    print('[Gmail] archive')
    #archive = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[@aria-label='Archive']")))
    archive = driver.find_elements_by_xpath("//div[@class='asa']")
    time.sleep(random.uniform(2,3))
    archive[11].click()
    time.sleep(random.uniform(2,3))

def mark_as_not_spam_gmail(subject,driver,s,rep,link,domain):
    print('[Gmail] Mark as not Spam')
    to_inbox = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[@aria-label='Move to Inbox']")))
    time.sleep(random.uniform(2,3))
    to_inbox.click()

def mark_as_important_gmail(subject,driver,s,rep,link,domain):
    print('[Gmail] Mark as important')
    #important = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[contains(@class,'pH-A7')]")))
    important = driver.find_elements_by_class_name('bnj ')
    print(important[-1])
    ActionChains(driver).move_to_element(important[-1]).click(important[-1]).perform()
    time.sleep(random.uniform(2,3))

def reply_gmail(subject,driver,s,rep,link,domain):
    reply = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[@aria-label='Reply']")))
    time.sleep(random.uniform(1,2))
    reply.click()
    reply_field = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[@aria-label='Message Body']")))
    time.sleep(random.uniform(1,2))
    reply_field.send_keys(rep)
    time.sleep(random.uniform(2,3))
    reply_field.send_keys(Keys.CONTROL+Keys.RETURN)
    time.sleep(10)


def click_offer_gmail(subject,driver,s,rep,link,domain):
    print('[Gmail] Click offer : Starts')
    try :
        dom = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//a[contains(@href,'"+domain+"')]")))
        print('[Gmail] Domain found')
        print(dom)
        time.sleep(random.uniform(2,3))
        ActionChains(driver).move_to_element(dom).click(dom).perform()
        time.sleep(random.uniform(2,3))
        p = driver.window_handles[0]
        c = driver.window_handles[1]
        driver.switch_to.window(c)
        time.sleep(random.uniform(4,4.5))
        driver.close()
        driver.switch_to.window(p)
        time.sleep(random.uniform(2,3))
    except Exception as e :
        print(e)
        link = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//a[contains(text(),'"+link+"')]")))
        print('[Gmail] Link found')
        print(link)
        time.sleep(random.uniform(2,3))
        ActionChains(driver).move_to_element(link).click(link).perform()
        time.sleep(random.uniform(2,3))
        p = driver.window_handles[0]
        c = driver.window_handles[1]
        driver.switch_to.window(c)
        time.sleep(random.uniform(4,4.5))
        driver.close()
        driver.switch_to.window(p)
        time.sleep(random.uniform(2,3))


def change_password_gmail(email,password,recovery,newpassword,driver):

    e = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//input[@type='email']")))
    e.send_keys(email)
    time.sleep(random.uniform(1,2))
    e.send_keys(Keys.RETURN)

    time.sleep(random.uniform(2,3))
    p = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//input[@type='password']")))
    p.send_keys(password)
    time.sleep(random.uniform(1,2))
    p.send_keys(Keys.RETURN)

    time.sleep(random.uniform(2,3))
    try :
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//div[text()='Confirm your recovery email']|//div[text()='E-Mail-Adresse zur Kontowiederherstellung bestätigen']|//div[text()='Confirmer votre adresse e-mail de récupération']"))).click()
        r = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//input[@name='knowledgePreregisteredEmailResponse']")))
        r.send_keys(recovery)
        time.sleep(random.uniform(1,2))
        r.send_keys(Keys.RETURN)
    except :
        pass

    time.sleep(random.uniform(3,3.5))

    driver.get("https://myaccount.google.com/signinoptions/password?continue=https%3A%2F%2Fmyaccount.google.com%2Fsecurity")

    p = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//input[@type='password']")))
    p.send_keys(password)
    time.sleep(random.uniform(1,2))
    p.send_keys(Keys.RETURN)

    time.sleep(random.uniform(3,3.5))

    driver.get("https://accounts.google.com/ServiceLogin/signinchooser?service=accountsettings&passive=1209600&osid=1&continue=https%3A%2F%2Fmyaccount.google.com%2Fsigninoptions%2Frescuephone%3Frapt%3DAEjHL4PeD51hbNbk05mr8puvFQ7I5aGXTBeUD0Dd3ENGYyL-g80iSJA3NI_uHs_PVISJH39jGOtcJggwRSdKv2n3pVuwfOllWQ&followup=https%3A%2F%2Fmyaccount.google.com%2Fsigninoptions%2Frescuephone%3Frapt%3DAEjHL4PeD51hbNbk05mr8puvFQ7I5aGXTBeUD0Dd3ENGYyL-g80iSJA3NI_uHs_PVISJH39jGOtcJggwRSdKv2n3pVuwfOllWQ&emr=1&mrp=security&rart=ANgoxcf1OKwz8qKNiNpJTpvj6Gc9cZLbsPxqRtW9EfA8G4bO5UH51PQWk_y_5M51k4uZWjlpkCSQOp3-YrNMSca7FoBZlhBPtg&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
    p = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//input[@type='password']")))
    p.send_keys(password)
    time.sleep(random.uniform(1,2))
    p.send_keys(Keys.RETURN)

    time.sleep(random.uniform(3,3.5))

    url = driver.current_url
    url = url.replace('rescuephone','password')

    driver.get(url)
    p = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//input[@name='password']")))
    p.send_keys(newpassword)
    time.sleep(random.uniform(1,2))
    cp = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//input[@name='confirmation_password']")))
    cp.send_keys(newpassword)
    time.sleep(random.uniform(1,2))
    cp.send_keys(Keys.RETURN)
    time.sleep(5)

def click_on_more_actions():
    more_actions = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='More']")))
    more_actions.click()
    time.sleep(random.uniform(2,3))
    more_actions.click()

def scroll(e):
    verical_ordinate = 50
    for i in range(0, 400):
        driver.execute_script("arguments[0].scrollTop = arguments[1]", e, verical_ordinate)
        verical_ordinate += 1

def init_browser_gmail(ip,port,p_user,p_password,browsers,hide):

    print(ip,port,p_user,p_password)
    print(type(ip))
    print(type(port))


    global driver,x

    if ip == '' and port == '' and p_user == '' and p_password == '' :

        print('[Gmail] Comodo without proxy : Activated')
        comodo_options = f_Options()
        fc = open('.\\paths\\path_comodo.txt','r')
        bp_comodo = fc.readline()
        comodo_options.binary_location = bp_comodo

        desired_capabilities = DesiredCapabilities().FIREFOX
        fpc = open('.\\paths\\comodo_profile.txt','r')
        p_comodo = fpc.readline()
        path = p_comodo
        firefox_profile = FirefoxProfile(path)
        firefox_profile.set_preference("dom.webdriver.enabled", False)
        firefox_profile.set_preference('useAutomationExtension', False)
        firefox_profile.update_preferences()



        if hide == 'hide_browser' :
            comodo_options.headless = True
        driver = webdriver.Firefox(executable_path=PATH_firefox, options=comodo_options, firefox_profile=firefox_profile)
        x = 0

    elif p_user == '' and p_password == '':

        proxy_ip_port = ip+':'+port
        print('[Gmail] Comodo proxy : Activated')
        comodo_options = f_Options()
        fc = open('.\\paths\\path_comodo.txt','r')
        bp_comodo = fc.readline()
        comodo_options.binary_location = bp_comodo

        fpc = open('.\\paths\\comodo_profile.txt', 'r')
        p_comodo = fpc.readline()
        path = p_comodo
        firefox_profile = FirefoxProfile(path)
        firefox_profile.set_preference("dom.webdriver.enabled", False)
        firefox_profile.set_preference('useAutomationExtension', False)
        firefox_profile.update_preferences()

        desired_capability = webdriver.DesiredCapabilities.FIREFOX
        desired_capability['marionette'] = True
        desired_capability['proxy'] = {
            'proxyType': "manual",
            'httpProxy': proxy_ip_port,
            'ftpProxy': proxy_ip_port,
            'sslProxy': proxy_ip_port,
                }


        if hide == 'hide_browser' :
            comodo_options.headless = True
        driver = webdriver.Firefox(executable_path=PATH_firefox,capabilities=desired_capability, options=comodo_options, firefox_profile=firefox_profile)
        x = 0

    elif ip != '' and port != '' and p_user != '' and p_password != '' :

        print('[Gmail] Comodo proxy with auth : Activated')
        proxy_ip_port = ip+':'+port
        comodo_options = f_Options()
        fc = open('.\\paths\\path_comodo.txt','r')
        bp_comodo = fc.readline()

        fpc = open('.\\paths\\comodo_profile.txt', 'r')
        p_comodo = fpc.readline()
        path = p_comodo
        firefox_profile = FirefoxProfile(path)
        firefox_profile.set_preference("dom.webdriver.enabled", False)
        firefox_profile.set_preference('useAutomationExtension', False)
        firefox_profile.update_preferences()

        comodo_options.binary_location = bp_comodo
        desired_capability = webdriver.DesiredCapabilities.FIREFOX
        desired_capability['marionette'] = True
        desired_capability['proxy'] = {
            'proxyType': "manual",
            'httpProxy': proxy_ip_port,
            'ftpProxy': proxy_ip_port,
            'sslProxy': proxy_ip_port,
                }


        if hide == 'hide_browser' :
            comodo_options.headless = True
        driver = webdriver.Firefox(executable_path=PATH_firefox, options=comodo_options, firefox_profile=firefox_profile)
        x = 1

    return driver,x

def begin(email,password,subject,recovery,ip,port,p_user,p_password,tasks,browsers,s,rep,link,domain,hide,newpassword):

    if 'login' in tasks and len(tasks) == 1 :
        print(tasks)
        init_browser_gmail(ip,port,p_user,p_password,browsers,hide)
        try:
            login_gmail(email,password,recovery,driver,x,p_user,p_password)
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Gmail\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f= open(".\\Log_Gmail\\"+ date + "\\"+t+".txt","w+")
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
                os.makedirs(".\\Log_Gmail\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "w+")
            f.write(date_time + " Email : " + email + " -- task : " + tasks[0] + "-- Status : Error")
            f.close()
            time.sleep(random.uniform(2,3))

    if 'change_password' in tasks and len(tasks) == 1 :
        print(tasks)
        init_browser_gmail(ip,port,p_user,p_password,browsers,hide)
        try:
            change_password_gmail(email,password,recovery,newpassword,driver)
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Gmail\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "w+")
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
                os.makedirs(".\\Log_Gmail\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "w+")
            f.write(date_time + " Email : " + email + " -- task : " + tasks[0] + "-- Status : Success")
            f.close()
            time.sleep(random.uniform(2,3))

    if 'mark_as_not_spam' in tasks and len(tasks) == 1 :
        init_browser_gmail(ip,port,p_user,p_password,browsers,hide)
        try:
            login_gmail(email,password,recovery,driver,x,p_user,p_password)
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Gmail\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "w+")
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
                os.makedirs(".\\Log_Gmail\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "w+")
            f.write(date_time + " Email : " + email + " -- task : Login -- Status : Error")
            f.close()
            time.sleep(random.uniform(2,3))

        search = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//input[@aria-label='Search mail']")))
        search.send_keys('in:spam subject:'+subject+Keys.RETURN)
        time.sleep(random.uniform(3,3.5))
        try:
            tables = driver.find_elements_by_class_name('Cp')
            e = tables[-1].find_element_by_tag_name('tr')
            #e = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//tr[@jsmodel='nXDxbd']")))
            while(e):
                ActionChains(driver).move_to_element(e).click(e).perform()
                try:
                    eval('mark_as_not_spam_gmail(subject,driver,s,rep,link,domain)')
                    now = datetime.now()
                    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                    f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "a+")
                    time.sleep(random.uniform(1, 3))
                    f.write("\n\r" + date_time + " Email : " + email + " -- Task : Mark as not spam -- Status : Success ")
                    f.close()
                    print('[Gmail] log done')
                except Exception as e:
                    now = datetime.now()
                    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                    f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "a+")
                    time.sleep(random.uniform(2,3))
                    f.write(
                        "\n\r" + date_time + " Email : " + email + " -- Task : Mark as not spam -- Status : Error ")
                    f.close()

                time.sleep(random.uniform(2,3))
                e = tables[-1].find_element_by_tag_name('tr')
                #e = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//tr[@jsmodel='nXDxbd']")))
        except Exception as e :
            print(e)
            print('[Gmail] Spam is Empty')

    elif 'mark_as_not_spam' in tasks and len(tasks) != 1 :
        print('[Gmail] Spam to inbox Then do other tasks')

        init_browser_gmail(ip,port,p_user,p_password,browsers,hide)
        try:
            login_gmail(email,password,recovery,driver,x,p_user,p_password)
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Gmail\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "w+")
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
                os.makedirs(".\\Log_Gmail\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "w+")
            f.write(date_time + " Email : " + email + " -- task : Login -- Status : Error")
            f.close()
            time.sleep(random.uniform(2,3))
        search = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//input[@aria-label='Search mail']")))
        search.send_keys('in:spam subject:'+subject+Keys.RETURN)
        time.sleep(random.uniform(3,3.5))
        try:
            tables = driver.find_elements_by_class_name('Cp')
            e = tables[-1].find_element_by_tag_name('tr')
            try :
                tasks.remove('mark_as_not_spam')
            except:
                pass
            while(e):
                ActionChains(driver).move_to_element(e).click(e).perform()
                eval('mark_as_not_spam_gmail(subject,driver,s,rep,link,domain)')
                time.sleep(random.uniform(1, 3))
                e = tables[-1].find_element_by_tag_name('tr')
        except Exception as e :
            print(e)
            print('[Gmail] Spam is Empty')

        try :
            clear = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//button[@aria-label='Clear search']")))
            clear.click()
            search = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//input[@aria-label='Search mail']")))
            search.send_keys('in:inbox subject:'+subject+Keys.RETURN)
            time.sleep(random.uniform(3,3.5))
            tables = driver.find_elements_by_class_name('Cp')
            e = tables[-1].find_element_by_tag_name('tr')
            try:
                tasks.remove('mark_as_not_spam')
            except:
                pass
            while(e) :
                ActionChains(driver).move_to_element(e).click(e).perform()
                for task in tasks:
                    try :
                        eval(task+'_gmail(subject,driver,s,rep,link,domain)')
                        time.sleep(random.uniform(1, 3))
                        now = datetime.now()
                        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                        f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "a+")
                        time.sleep(random.uniform(2,3))
                        f.write(
                            "\n\r" + date_time + " Email : " + email + " -- Task : " + task + " -- Status : Success ")
                        f.close()
                        print('[Gmail] log done')
                    except Exception as e:
                        print(e)
                        now = datetime.now()
                        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                        f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "a+")
                        time.sleep(random.uniform(2,3))
                        f.write(
                            "\n\r" + date_time + " Email : " + email + " -- Task : " + task + " -- Status : Success ")
                        f.close()
                    e = tables[-1].find_element_by_tag_name('tr')
        except Exception as e :
            print(e)
            print("[Gmail] Done")


    elif ('mark_as_not_spam' not in tasks) and ('login' not in tasks) and ('change_password' not in tasks) :

        init_browser_gmail(ip,port,p_user,p_password,browsers,hide)
        try:
            login_gmail(email,password,recovery,driver,x,p_user,p_password)
            now = datetime.now()
            date_time = now.strftime("%d-%m-%Y %H:%M:%S")
            date = now.strftime("%d-%m-%Y")
            t = now.strftime("%H_%M_%S")
            try:
                os.makedirs(".\\Log_Gmail\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "w+")
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
                os.makedirs(".\\Log_Gmail\\" + date)
            except Exception as e:
                print(e)
                print("Not a problem, let continue the script :)")
                pass
            f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "w+")
            f.write(date_time + " Email : " + email + " -- task : Login -- Status : Error")
            f.close()
            time.sleep(random.uniform(2,3))
        try :
            search = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH,"//input[@aria-label='Search mail']")))
            search.send_keys('in:inbox subject:'+subject+Keys.RETURN)
            time.sleep(random.uniform(3,3.5))
            tables = driver.find_elements_by_class_name('Cp')
            e = tables[-1].find_element_by_tag_name('tr')
            while(e) :
                ActionChains(driver).move_to_element(e).click(e).perform()
                for task in tasks:
                    try :
                        eval(task+'_gmail(subject,driver,s,rep,link,domain)')
                        time.sleep(random.uniform(1, 3))
                        now = datetime.now()
                        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                        f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "a+")
                        time.sleep(random.uniform(2,3))
                        f.write(
                            "\n\r" + date_time + " Email : " + email + " -- Task : " + task + " -- Status : Success ")
                        f.close()
                        print('[Gmail] log done')
                    except Exception as e:
                        print(e)
                        now = datetime.now()
                        date_time = now.strftime("%d-%m-%Y %H:%M:%S")
                        f = open(".\\Log_Gmail\\" + date + "\\" + t + ".txt", "a+")
                        time.sleep(random.uniform(2,3))
                        f.write(
                            "\n\r" + date_time + " Email : " + email + " -- Task : " + task + " -- Status : Success ")
                        f.close()
                    e = tables[-1].find_element_by_tag_name('tr')
        except :
            print("[Gmail] Done")



    #driver.quit()

def hey(x):

    return x


def launch_gmail(x):
    global processes,browsers,acc,subject,n,link,domain
    #ata = pd.read_csv('C:/Users/'+username+'/Desktop/data_gmail.csv',sep=';')
    acc = x['accounts']
    d = x['accounts'].split('\r\n')
    for i in range(len(d)):
        d[i] = d[i].split(';')
    data = pd.DataFrame(d,columns = ['Email','Password','Recovery','ip','port','p_user','p_password','newpassword'])
    print(data)
    emails = data['Email'].tolist()
    passwords = data['Password'].tolist()
    recovery = data['Recovery'].tolist()
    ips = data['ip'].tolist()
    ports = data['port'].tolist()
    p_users = data['p_user'].tolist()
    p_passwords = data['p_password'].tolist()
    newpasswords = data['newpassword'].tolist()


    inputs = list(x.values())
    subject = inputs[0]
    n = int(inputs[2])
    s = 5
    browsers = inputs[3]
    tasks = inputs[1].split(',')
    rep = inputs[7]
    link = inputs[4]
    domain = inputs[8]
    hide = inputs[6]

    processes = []

    while(len(emails)!=0):
        for i in range(n):
            p= Process(target=begin, args=(emails[0],passwords[0],subject,recovery[0],ips[0],ports[0],p_users[0],p_passwords[0],tasks,browsers,s,rep,link,domain,hide,newpasswords[0]))
            p.start()
            time.sleep(random.uniform(1,2))
            processes.append(p)


            emails.remove(emails[0]) , passwords.remove(passwords[0]) , recovery.remove(recovery[0]) , ips.remove(ips[0]) , ports.remove(ports[0]) , p_users.remove(p_users[0]) , p_passwords.remove(p_passwords[0]) , newpasswords.remove(newpasswords[0])

        for process in processes:
            process.join()


    print('[Gmail] Script Done')
    
    return redirect(url_for('.interface_gmail', acc=acc,subject=subject,n=n,link=link,domain=domain))

def launch_gmail_schedule(y):
    try:
        print("Your task will be launch in  " + y['schedule_date'] + " at  " + y['schedule_time'])
        h = y['schedule_time'].split(':')[0]
        m = y['schedule_time'].split(':')[1]
        sched = BlockingScheduler()
        trigger = cron.CronTrigger(start_date=y['schedule_date'], hour=h, minute=m)
        sched.add_job(func=launch_gmail, args=[y], trigger=trigger)
        sched.start()
    except Exception as e:
        print(e)
        launch_gmail(y)
    return redirect(url_for('.interface_gmail', acc=acc, subject=subject, n=n, link=link, domain=domain))

def stop_gmail():
    print(processes)
    try:
        if browsers == 'comodo':
            for process in processes:
                p = psutil.Process(process.pid)
                print("[Gmail] terminate")
                p.terminate()
            subprocess.call('taskkill /F /IM icedragon.exe')
            subprocess.call('taskkill /F /IM geckodriver.exe')
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
        
    return redirect(url_for('.interface_gmail', acc=acc,subject=subject,n=n,link=link,domain=domain))

def pause_gmail():
    pid=os.getpid()
    for process in processes:
        p= psutil.Process(process.pid)
        print("[Gmail] suspend")
        p.suspend()
        
    return render_template("pauseGmail.html",acc=acc,subject=subject,n=n,link=link,domain=domain)
 
        
def resume_gmail():
    pid=os.getpid()
    for process in processes:
        p= psutil.Process(process.pid)
        print("[Gmail] resume it", process.is_alive())
        p.resume()
    
    
    return redirect(url_for('.interface_gmail', acc=acc,subject=subject,n=n,link=link,domain=domain))

    
    





    






