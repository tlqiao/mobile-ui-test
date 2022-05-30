from time import sleep
from zapv2 import ZAPv2
import requests
import subprocess
import os

port = "8090"
zap_proxies = {"http": "http://127.0.0.1:{0}".format(port), "https": "http://127.0.0.1:{0}".format(port)}
zap = ZAPv2(proxies=zap_proxies)


def start_zap():
    cmd1 = "sh /Applications/OWASP-ZAP.app/Contents/Java/zap.sh -daemon -config api.disablekey=true -port {0}".format(port)
    subprocess.Popen(cmd1.split(" "), stdout=open(os.devnull, "w"))
    while True:
        try:
            status_req = requests.get("http://127.0.0.1:{0}".format(port))
            if status_req.status_code == 200:
                break
            else:
                print("ZAP is starting")
                sleep(1)
        except Exception:
            print("waiting ZAP to start")
            sleep(5)
            pass
    zap.core.new_session(name="demo", overwrite=True)
    zap.context.include_in_context("default context", "https://localhost:3000*")


def visit_web():
    login_url = "http://localhost:3000/#/login"
    requests.get(login_url, proxies=zap_proxies, verify=False)


def login_web(username, password):
    url = "http://localhost:3000/rest/user/login"
    login_data = {"email": username, "password": password}
    login = requests.post(url, proxies=zap_proxies, json=login_data, verify=False)
    if login.status_code == 200:
        resp_json = login.json()
        auth_token = resp_json['authentication']['token']
    else:
        print("Unable to login")
        raise Exception("Unable to login")
    return auth_token


def perform_spider(url):
    spider_id = zap.spider.scan(url, recurse=False, subtreeonly=True)
    return spider_id


def get_spider_status(url):
    status = 0
    while int(status) < 100:
        status = zap.spider.status(perform_spider(url))
        print('spider status: ' + status)


def perform_zap_active_scan(target_url):
    scan_id = zap.ascan.scan(target_url, recurse=True, inscopeonly=True)
    return scan_id


def get_active_scan_status(url):
    status = 0
    while int(status) < 100:
        status = zap.spider.status(perform_zap_active_scan(url))
        print('zap active scan status: ' + status)


def zap_alerts_summary_for(url):
    summary = zap.alert.alerts_summary(url)
    print("Alerts summary: {0}".format(summary))


def zap_alerts_summary():
    url = "http://localhost:3000"
    zap_alerts_summary_for(url)


def save_scan_report(full_filename):
    report = zap.core.htmlreport()
    with open(full_filename, 'w') as file:
        file.write(report)
        print('report save in {0}'.format(full_filename))


def close_zap():
    zap.core.shutdown()
