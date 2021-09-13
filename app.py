import base64
import socket
from multiprocessing import freeze_support
import threading
from flask import Flask,render_template,request,jsonify,redirect,url_for
import webbrowser
from threading import Timer
import schedule
from script_hotmail import *
from script_gmail import *
from script_yahoo import *


app = Flask(__name__)
@app.route('/', methods=["POST","GET"])
def interface():
    if request.method == "POST":

        data = {}
              
        accounts = request.form["accounts"]
        subject = request.form["subject"]
        task = request.form["tasks"]
        threads = request.form["threads"]
        browsers = request.form["Radio"]   
        link = request.form["link"]
        if request.form.get("box", False):
            hide = request.form["box"]
        elif request.form.get("box", True):
            hide = 'dont_hide_browser'
        try :
            reply = request.form["reply_msg"]
        except :
            reply = "NAN"
        mark_as_read = request.form["Radio2"]
        try:
            schedule_date = request.form["date"]
        except:
            schedule_date = "NAN"
        try:
            schedule_time = request.form["time"]
        except:
            schedule_time = "NAN"
        
        data['subject'] = subject
        data['task'] = task
        data['threads'] = threads
        data['browsers'] = browsers
        data['link'] = link
        data['accounts'] = accounts
        data['hide'] = hide
        data['reply'] = reply
        data['mark_as_read'] = mark_as_read
        data['schedule_date'] = schedule_date
        data['schedule_time'] = schedule_time


        return launch_schedule(data)
    else:
        try:
            acc = request.args['acc']
        except:
            acc = ''
        try:
            subject = request.args['subject']
        except:
            subject = ''
        try:
            link = request.args['link']
        except:
            link = ''
        try:
            n = request.args['n']
        except:
            n = ''

        return render_template("interfaceHotmail.html",acc=acc,subject=subject,link=link,n=n)
    
@app.route('/gmail', methods=["POST", "GET"])

def interface_gmail():
    if request.method == "POST":

        data = {}

        accounts = request.form["accounts"]
        subject = request.form["subject"]
        task = request.form["tasks"]
        threads = request.form["threads"]
        browsers = request.form["Radio"]
        link = request.form["link"]
        if request.form.get("box", False):
            hide = request.form["box"]
        elif request.form.get("box", True):
            hide = 'dont_hide_browser'
        try:
            reply = request.form["reply_msg"]
        except:
            reply = "NAN"
        domain = request.form['domain']
        try:
            schedule_date = request.form["date"]
        except:
            schedule_date = "NAN"
        try:
            schedule_time = request.form["time"]
        except:
            schedule_time = "NAN"

        data['subject'] = subject
        data['task'] = task
        data['threads'] = threads
        data['browsers'] = browsers
        data['link'] = link
        data['accounts'] = accounts
        data['hide'] = hide
        data['reply'] = reply
        data['domain'] = domain
        data['schedule_date'] = schedule_date
        data['schedule_time'] = schedule_time

        return launch_gmail_schedule(data)
    else:
        try:
            acc = request.args['acc']
        except:
            acc = ''
        try:
            subject = request.args['subject']
        except:
            subject = ''
        try:
            link = request.args['link']
        except:
            link = ''
        try:
            n = request.args['n']
        except:
            n = ''
        try:
            domain = request.args['domain']
        except:
            domain = ''

        return render_template("interfaceGmail.html", acc=acc, subject=subject, n=n, link=link, domain=domain)

    
@app.route('/yahoo', methods=["POST", "GET"])
def interface_yahoo():
    if request.method == "POST":

        data = {}

        accounts = request.form["accounts"]
        subject = request.form["subject"]
        task = request.form["tasks"]
        threads = request.form["threads"]
        browsers = request.form["Radio"]
        if request.form.get("box", False):
            hide = request.form["box"]
        elif request.form.get("box", True):
            hide = 'dont_hide_browser'
        try:
            domains = request.files["domains_file"]
        except:
            domains = "NAN"
        try:
            schedule_date = request.form["date"]
        except:
            schedule_date = "NAN"
        try:
            schedule_time = request.form["time"]
        except:
            schedule_time = "NAN"


        data['subject'] = subject
        data['task'] = task
        data['threads'] = threads
        data['browsers'] = browsers
        data['accounts'] = accounts
        data['hide'] = hide
        data['domains'] = domains
        data['schedule_date'] = schedule_date
        data['schedule_time'] = schedule_time


        return launch_yahoo_schedule(data)
    else:
        try:
            acc = request.args['acc']
        except:
            acc = ''
        try:
            subject = request.args['subject']
        except:
            subject = ''
        try:
            n = request.args['n']
        except:
            n = ''

        return render_template("interfaceYahoo.html", acc=acc, subject=subject, n=n)


@app.route('/resume', methods=["GET"])
def resume_script():
    return resume()

@app.route('/stop', methods=["GET"])
def stop_script():
    return stop()

@app.route('/pause', methods=["GET"])
def pause_script():
    return pause()

@app.route('/resumeGmail', methods=["GET"])
def resume_script_gmail():
    return resume_gmail()

@app.route('/stopGmail', methods=["GET"])
def stop_script_gmail():
    return stop_gmail()

@app.route('/pauseGmail', methods=["GET"])
def pause_script_gmail():
    return pause_gmail()

@app.route('/resumeYahoo', methods=["GET"])
def resume_script_yahoo():
    return resume_yahoo()

@app.route('/stopYahoo', methods=["GET"])
def stop_script_yahoo():
    return stop_yahoo()

@app.route('/pauseYahoo', methods=["GET"])
def pause_script_yahoo():
    return pause_yahoo()

if __name__ == '__main__':
    freeze_support()
    f = open('.\\security_code.txt', 'r')
    d = ''+f.readline()+''
    d1 = base64.b64decode(d)
    d2 = base64.b64decode(d1)
    d3 = base64.b64decode(d2)
    d4 = str(d3).replace("b'",'').replace("'",'')
    name = d4.split('+')[0]
    ip = d4.split('+')[1]
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    if name == "salman":
        if local_ip == ip:
            webbrowser.open_new('http://127.0.0.1:5000/')
            app.run('127.0.0.1',5000)

